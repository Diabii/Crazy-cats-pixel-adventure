import pygame

class Attack:
    """
    System ataków dla jednego właściciela (owner = Player).
    - 'claws' (melee): 3 klatki animacji, wyświetlane przed graczem, nie poruszają się.
    - 'fireball' (projectile): 3 klatki animacji pętli, pocisk leci od gracza w jego kierunku.

    Wymagane grafiki w słowniku gfx:
        gfx['claws_right'],  gfx['claws_left']   -> list[Surface] (3 klatki)
        gfx['fireball_right'], gfx['fireball_left'] -> list[Surface] (3 klatki)
    """

    def __init__(self, owner, gfx: dict,
                 claws_frame_time: float = 0.06,      # czas na klatkę (claws)
                 fireball_frame_time: float = 0.06,   # czas na klatkę (fireball)
                 fireball_speed: float = 700.0,       # px/s
                 fireball_lifetime: float = 1.2,      # s
                 claws_forward_pad: int = 8,          # odsunięcie do przodu względem hitboxa
                 claws_vertical_align: str = "center" # 'center' | 'top' | 'bottom'
                 ):
        self.owner = owner
        self.gfx = gfx

        # --- Parametry zachowania ---
        self.claws_frame_time = claws_frame_time
        self.fireball_frame_time = fireball_frame_time
        self.fireball_speed = fireball_speed
        self.fireball_lifetime = fireball_lifetime
        self.claws_forward_pad = claws_forward_pad
        self.claws_vertical_align = claws_vertical_align

        # --- Stan melee (claws) ---
        self._claws_active = False
        self._claws_frames = None
        self._claws_index = 0
        self._claws_timer = 0.0
        self._claws_pos = pygame.Vector2(0, 0)  # top-left do rysowania
        self._claws_image = None

        # --- Stan pocisków (fireball) ---
        # Każdy pocisk: dict {pos: Vector2, vel: Vector2, frames: list[Surface],
        #                     idx: int, timer: float, life: float, image: Surface}
        self._projectiles = []

    # ---------- TRIGGERY ----------
    def start_claws(self):
        """Uruchom animację 3 klatek claws przed graczem (zależnie od direction)."""
        key = 'claws_right' if self.owner.direction == 'right' else 'claws_left'
        frames = self.gfx.get(key, None)
        if not frames:
            # Brak grafik — nic nie rób
            return

        self._claws_active = True
        self._claws_frames = frames
        self._claws_index = 0
        self._claws_timer = 0.0
        self._claws_image = frames[0]

        # Ustal pozycję claws względem HITBOXA gracza
        fw = self._claws_image.get_width()
        fh = self._claws_image.get_height()

        # Podstawą pozycjonowania jest hitbox (owner.x, owner.y, owner.width, owner.height)
        if self.owner.direction == 'right':
            x = self.owner.x + self.owner.width + self.claws_forward_pad
        else:
            x = self.owner.x - fw - self.claws_forward_pad

        # Wyrównanie pionowe
        if self.claws_vertical_align == "top":
            y = self.owner.y
        elif self.claws_vertical_align == "bottom":
            y = self.owner.y + self.owner.height - fh
        else:  # center
            y = self.owner.y + (self.owner.height - fh) / 2

        self._claws_pos.update(x, y)

    def start_fireball(self):
        """Wystrzel fireball w kierunku patrzenia gracza (pocisk porusza się)."""
        key = 'fireball_right' if self.owner.direction == 'right' else 'fireball_left'
        frames = self.gfx.get(key, None)
        if not frames:
            return

        # Początkowe położenie: z przodu gracza (przy krawędzi hitboxa), nie przy spricie
        first = frames[0]
        fw, fh = first.get_width(), first.get_height()

        if self.owner.direction == 'right':
            x = self.owner.x + self.owner.width
            vel = pygame.Vector2(self.fireball_speed, 0)
        else:
            x = self.owner.x - fw
            vel = pygame.Vector2(-self.fireball_speed, 0)

        # pionowo środkiem na wysokości hitboxa
        y = self.owner.y + (self.owner.height - fh) / 2

        projectile = {
            "pos": pygame.Vector2(x, y),
            "vel": vel,
            "frames": frames,
            "idx": 0,
            "timer": 0.0,
            "life": self.fireball_lifetime,
            "image": first
        }
        self._projectiles.append(projectile)

    # ---------- UPDATE / DRAW ----------
    def update(self, dt: float, obstacles=None, world_bounds=None):
        """
        Aktualizuj animacje melee i pocisków.
        obstacles: opcjonalna lista pygame.Rect dla kolizji pocisku.
        world_bounds: (W,H) — granice świata/okna do usuwania pocisków poza ekranem.
        """

        # --- Aktualizacja claws (3 klatki, jednorazowo) ---
        if self._claws_active and self._claws_frames:
            self._claws_timer += dt
            while self._claws_timer >= self.claws_frame_time:
                self._claws_timer -= self.claws_frame_time
                self._claws_index += 1
                if self._claws_index < len(self._claws_frames):
                    self._claws_image = self._claws_frames[self._claws_index]
                else:
                    # koniec animacji
                    self._claws_active = False
                    self._claws_frames = None
                    self._claws_image = None
                    break

        # --- Aktualizacja pocisków (ruch + animacja + życie + kolizje) ---
        if obstacles is None:
            obstacles = []

        to_remove = []
        for i, p in enumerate(self._projectiles):
            # Ruch
            p["pos"] += p["vel"] * dt

            # Animacja klatek pocisku (pętla)
            p["timer"] += dt
            while p["timer"] >= self.fireball_frame_time:
                p["timer"] -= self.fireball_frame_time
                p["idx"] = (p["idx"] + 1) % len(p["frames"])
                p["image"] = p["frames"][p["idx"]]

            # Życie / TTL
            p["life"] -= dt
            if p["life"] <= 0:
                to_remove.append(i)
                continue

            # Kolizje (jeśli podano przeszkody)
            img = p["image"]
            rect = img.get_rect(topleft=(int(p["pos"].x), int(p["pos"].y)))
            for obst in obstacles:
                if rect.colliderect(obst):
                    to_remove.append(i)
                    break

            # Granice świata / okna
            if world_bounds:
                W, H = world_bounds
                if rect.right < 0 or rect.left > W or rect.bottom < 0 or rect.top > H:
                    to_remove.append(i)

        # Usuwanie od końca, by indeksy się zgadzały
        for idx in reversed(to_remove):
            self._projectiles.pop(idx)

    def draw(self, screen):
        """Rysuj aktywne ataki. Rysuj to PO graczu, aby claws był na wierzchu."""
        # Najpierw pociski (mogą być i przed i za — rysujemy normalnie)
        for p in self._projectiles:
            screen.blit(p["image"], (int(p["pos"].x), int(p["pos"].y)))

        # Na końcu melee claws, żeby mieć pewność, że jest „przed graczem”
        if self._claws_active and self._claws_image:
            screen.blit(self._claws_image, (int(self._claws_pos.x), int(self._claws_pos.y)))

    def get_claws_hitbox(self):
        if not self._claws_active or not self._claws_image: # Zwraca prostokąt aktywnych pazurów (Rect) lub None
            return None
       
        return pygame.Rect(      # Tworzy Rect na podstawie aktualnej pozycji rysowania pazurów
            int(self._claws_pos.x),
            int(self._claws_pos.y),
            self._claws_image.get_width(),
            self._claws_image.get_height()
        )