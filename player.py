import pygame
import animation_tools

# >>> ZMIANA <<<: import systemu ataków (klasa Attack)
from attack import Attack


class Player:
    def __init__(self, name, x, y, width, height, speed, color,
                 # --- KONFIG PASKA HP (6 kategorii: 0..5) ---
                 hp_paths=None,                 # list[str] ścieżki do 6 grafik (0..5)
                 hp_size=(90, 45),            # docelowy rozmiar obrazka paska
                 draw_hp_above_player=True,   # True: nad graczem; False: HUD
                 hp_offset=(0, -10),           # przesunięcie gdy nad graczem (x,y)
                 hp_hud_pos=(16, 16)           # pozycja HUD (x,y)
                 ):
        self.x = x
        self.y = y

        # --- STAN ŻYCIA I ŚMIERCI
        self.is_dead = False        # Czy gracz umarł
        self.invincible_timer = 0.0 # Czas nieśmiertelności po otrzymaniu obrażeń
        self.invincible_duration = 1.0 # Jak długo miga po uderzeniu (sekundy)

        # --- STAN ATAKU (jedna klatka) ---
        self.is_attacking = False
        self.attack_timer = 0.0
        self.attack_duration = 0.18  # ile czasu wyświetla się klatka ataku

        # --- COOLDOWNY (blokady spamu) ---
        self.attack_cooldown = 0.5         # po zwykłym ataku
        self.super_attack_cooldown = 0.5   # po super ataku
        self._attack_cd_left = 0.0
        self._super_cd_left = 0.0

        # Rozmiar rysowanego sprite'a (grafiki)
        self.image_width = width
        self.image_height = height

        # Rozmiar hitboxa (mniejszy od grafiki) + offset do rysowania sprite'a
        self.width = 60   # Szerokość hitboxa
        self.height = 50  # Wysokość hitboxa
        self.offset_x = (self.image_width - self.width) // 2
        self.offset_y = (self.image_height - self.height) // 2

        self.speed = speed
        self.color = color
        self.vel_x = 0
        self.vel_y = 0
        self.acceleration_speed = speed * 10
        self.max_speed = 400
        self.friction = 0.85
        self.gravity = 1500
        self.jump_power = -800
        self.on_ground = False

        self.direction = "left"
        self.animation_count = 0
        self.current_state = "idle"


        # --- Animacja sterowana czasem ---
        self.anim_timer = 0.0
        self.anim_frame = 0
        self.anim_frame_time = 0.06  # 80 ms/klatkę (zwiększ do 0.12, gdy chcesz wolniej)
        self._last_anim_state = None  # do resetowania klatek przy zmianie stanu

        # --- Progi dla logiki animacji/ruchu ---
        self.RUN_THRESHOLD = 50.0     # px/s: poniżej tego idle zamiast run
        self.STOP_DRAG = 1500.0       # px/s^2: mocne hamowanie po odpuszczeniu
        self.DEADZONE = 6.0           # px/s: poniżej traktujemy jak 0 (natychmiast idle)


        # Pobieramy słownik z grafikami animacji
        grafiki = animation_tools.wczytaj_postacie(width, height, name)
        self.__dict__.update(grafiki)

        ataki = animation_tools.wczytaj_ataki()
        self.__dict__.update(ataki)

        # >>> ZMIANA <<<: inicjalizacja systemu ataków (claws/fireball)
        self.attack_system = Attack(self, ataki)

        # Ustawienie początkowego obrazka 
        self.image = self.idle_left[0]
        self.mask = pygame.mask.from_surface(self.image)

        # --- HP SYSTEM (0..5) ---
        self.hp_max = 5
        self.hp = 5
        self._draw_hp_above = draw_hp_above_player
        self._hp_offset = hp_offset
        self._hp_hud_pos = hp_hud_pos
        self.hp_images = self._load_hp_images(hp_paths, hp_size)

    # Tworzy prostokątny hitbox o wymiarach gracza
    def get_hitbox(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    # Test kolizji z przeszkodami
    def collision_test(self, rect, obstacles):
        collisions = []
        for obstacle in obstacles:
            if rect.colliderect(obstacle):
                collisions.append(obstacle)
        return collisions

    # Przyjmowanie obrażeń 
    def take_damage(self, amount):
        # Jeśli już martwy lub na cooldownie po poprzednim ciosie -> ignoruj
        if self.is_dead or self.invincible_timer > 0:
            return

        self.add_hp(-amount)
        self.invincible_timer = self.invincible_duration # start cooldownu

        if self.hp <= 0:
            self.die()

    # Śmierć

    def die(self):
        if self.is_dead:
            return 
        
        self.is_dead = True
        self.vel_x = 0
        
        # Obróć na plecy
        self.image = pygame.transform.rotate(self.image, 180)
        
        # Efekt szarości
        try:
            self.image = pygame.transform.grayscale(self.image)
        except AttributeError:
            tint_surf = pygame.Surface(self.image.get_size()).convert_alpha()
            tint_surf.fill((60, 60, 60, 0))  # Lekkie rozjaśnienie
            self.image.blit(tint_surf, (0,0), special_flags=pygame.BLEND_RGBA_ADD)

        self.offset_y -= 40


        

        


    # Ruch gracza + reakcja na kolizje
    def move(self, keys_pressed, dt, window_width, window_height,
             up_key, down_key, left_key, right_key, obstacles):

        if self.is_dead:
            # Jeśli martwy, nic nie jest wciśnięte
            input_left = False
            input_right = False
        else:
            # Jeśli żyje, czytamy klawisze normalnie 
            input_left = keys_pressed[left_key]
            input_right = keys_pressed[right_key]

        # Zmiana prędkości przez wejście
        if input_left:
            self.vel_x -= self.acceleration_speed * dt
        if input_right:
            self.vel_x += self.acceleration_speed * dt

        # Kierunek patrzenia wg prędkości
        if not self.is_dead:
            if self.vel_x > 0:
                self.direction = "right"
            elif self.vel_x < 0:
                self.direction = "left"
        

        # Hamowanie:
        if not input_left and not input_right:
            # silne hamowanie gdy brak wejścia
            if self.vel_x > 0:
                self.vel_x = max(0.0, self.vel_x - self.STOP_DRAG * dt)
            elif self.vel_x < 0:
                self.vel_x = min(0.0, self.vel_x + self.STOP_DRAG * dt)
        else:
            # lekkie tarcie, gdy trzymasz kierunek (miękkie prowadzenie)
            self.vel_x *= self.friction

        # Ograniczenie prędkości
        if self.vel_x > self.max_speed:
            self.vel_x = self.max_speed
        elif self.vel_x < -self.max_speed:
            self.vel_x = -self.max_speed

        # Deadzone – bardzo małe prędkości traktuj jako 0, żeby natychmiast przejść w idle
        if abs(self.vel_x) < self.DEADZONE:
            self.vel_x = 0.0

        # --- SKAKANIE I GRAWITACJA (OŚ Y) ---

        # Grawitacja
        self.vel_y += self.gravity * dt

        # Skok tylko, gdy stoimy na ziemi
        if keys_pressed[up_key] and self.on_ground and not self.is_dead:
            self.vel_y = self.jump_power
            self.on_ground = False

        # Dół przyspiesza spadanie
        if keys_pressed[down_key] and not self.is_dead:
            self.vel_y += self.gravity * dt

        # --- APLIKOWANIE RUCHU I KOLIZJE ---

        # --- RUCH W OŚ X ---
        dx = self.vel_x * dt
        self.x += dx

        player_hitbox = self.get_hitbox()
        collisions = self.collision_test(player_hitbox, obstacles)

        for obstacle in collisions:
            if dx > 0:  # Uderzenie prawym bokiem
                self.x = obstacle.left - self.width
                self.vel_x = 0  # Zerowanie prędkości po zderzeniu
            if dx < 0:  # Uderzenie lewym bokiem
                self.x = obstacle.right
                self.vel_x = 0

        # --- RUCH W OŚ Y ---

        self.on_ground = False

        dy = self.vel_y * dt
        self.y += dy

        player_rect = self.get_hitbox()
        collisions = self.collision_test(player_rect, obstacles)

        if dy > 0:
            player_rect.height += 1

        collisions = self.collision_test(player_rect, obstacles)

        for obstacle in collisions:
            if dy > 0:  # Podłoga
                self.y = obstacle.top - self.height
                self.vel_y = 0
                self.on_ground = True  # Stoi na przeszkodzie
            if dy < 0:  # Sufit
                self.y = obstacle.bottom
                self.vel_y = 0

        # Ograniczenie do okna

        # Dół ekranu to podłoga
        if self.y >= window_height - self.height:
            self.y = window_height - self.height
            self.vel_y = 0
            self.on_ground = True

        # Ściany boczne
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        elif self.x > window_width - self.width:
            self.x = window_width - self.width
            self.vel_x = 0

    def update_anim(self, dt):
        if self.is_dead:
            return
        # --- Cooldowny ---
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        if self._attack_cd_left > 0:
            self._attack_cd_left = max(0.0, self._attack_cd_left - dt)
        if self._super_cd_left > 0:
            self._super_cd_left = max(0.0, self._super_cd_left - dt)

        # --- Aktualizacja systemu ataków ---
        self.attack_system.update(dt)

        # --- W trakcie ataku nie nadpisuj klatki ciała (jak w Twojej logice) ---
        if self.is_attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_duration:
                self.is_attacking = False
                self.attack_timer = 0.0
            else:
                # Zostaw wyświetloną klatkę ataku, nie zmieniaj animacji ciała
                return

        # --- Wybór stanu animacji (idle/run/jump/fall) ---
        if not self.on_ground:
            if self.vel_y < 0:
                state = "jump_right" if self.direction == "right" else "jump_left"
                sprites = self.jump_loop_right if self.direction == "right" else self.jump_loop_left
            else:
                state = "fall_right" if self.direction == "right" else "fall_left"
                sprites = self.fall_right if self.direction == "right" else self.fall_left
        else:
            # Bieg tylko jeśli prędkość istotna (RUN_THRESHOLD)
            if abs(self.vel_x) > self.RUN_THRESHOLD:
                state = "run_right" if self.direction == "right" else "run_left"
                sprites = self.run_right if self.direction == "right" else self.run_left
            else:
                state = "idle_right" if self.direction == "right" else "idle_left"
                sprites = self.idle_right if self.direction == "right" else self.idle_left

        # --- Reset klatek po zmianie stanu (aby przejścia były natychmiastowe) ---
        if state != self._last_anim_state:
            self._last_anim_state = state
            self.anim_frame = 0
            self.anim_timer = 0.0

        # --- Sterowanie animacją czasowo ---
        self.anim_timer += dt
        if self.anim_timer >= self.anim_frame_time:
            # akumuluj nadwyżkę dla stabilności przy niższym FPS
            self.anim_timer -= self.anim_frame_time
            self.anim_frame = (self.anim_frame + 1) % len(sprites)

        # --- Ustaw klatkę i maskę ---
        self.image = sprites[self.anim_frame]
        self.mask = pygame.mask.from_surface(self.image)
    
    def attack(self, keys_pressed, attack_key, super_attack_key=None):
        """
        Super atak działa jak zwykły, ale używa super klatki.
        Priorytet: jeśli wciśnięty super_attack_key i cooldown=0 → super.
        W przeciwnym razie: jeśli wciśnięty attack_key i cooldown=0 → zwykły atak.
        """
        if self.is_dead:
            return
        
        # Nie pozwalaj zaczynać nowego ataku, gdy poprzedni jeszcze trwa
        if self.is_attacking:
            return

        # Czy można aktywować super atak teraz?
        use_super = bool(
            super_attack_key and
            keys_pressed[super_attack_key] and
            self._super_cd_left <= 0.0
        )

        if use_super:
            # Super atak start
            self.is_attacking = True
            self.attack_timer = 0.0
            self._super_cd_left = self.super_attack_cooldown  # WŁĄCZ cooldown supera

            # >>> ZMIANA <<<: wystrzel fireball (pocisk od gracza)
            self.attack_system.start_fireball()

            # Ustaw odpowiednią klatkę ciała
            if self.direction == "right":
                if hasattr(self, "super_attack_right"):
                    frame = self.super_attack_right[0]
                elif hasattr(self, "attack_right"):
                    frame = self.attack_right[0]  # fallback
                else:
                    frame = getattr(self, "idle_right", [self.image])[0]
            else:
                if hasattr(self, "super_attack_left"):
                    frame = self.super_attack_left[0]
                elif hasattr(self, "attack_left"):
                    frame = self.attack_left[0]
                elif hasattr(self, "super_attack_right"):
                    frame = pygame.transform.flip(self.super_attack_right[0], True, False)
                elif hasattr(self, "attack_right"):
                    frame = pygame.transform.flip(self.attack_right[0], True, False)
                else:
                    frame = getattr(self, "idle_left", [self.image])[0]

            self.image = frame
            self.mask = pygame.mask.from_surface(self.image)
            return

        # Jeśli super nie został wyzwolony, spróbuj zwykłego ataku
        can_normal = (keys_pressed[attack_key] and self._attack_cd_left <= 0.0)
        if can_normal:
            self.is_attacking = True
            self.attack_timer = 0.0
            self._attack_cd_left = self.attack_cooldown  # WŁĄCZ cooldown zwykłego ataku

            # >>> ZMIANA <<<: pokaż claws (3 klatki) przed graczem
            self.attack_system.start_claws()

            if self.direction == "right":
                if hasattr(self, "attack_right"):
                    frame = self.attack_right[0]
                else:
                    frame = getattr(self, "idle_right", [self.image])[0]
            else:
                if hasattr(self, "attack_left"):
                    frame = self.attack_left[0]
                elif hasattr(self, "attack_right"):
                    frame = pygame.transform.flip(self.attack_right[0], True, False)
                else:
                    frame = getattr(self, "idle_left", [self.image])[0]

            self.image = frame
            self.mask = pygame.mask.from_surface(self.image)

    # Rysowanie
    def draw(self, screen):
        # Jeśli martwy -> rysuj bez migania
        if self.is_dead:
            self._draw_body(screen)
            
        # Jeśli żywy i ma cooldown -> migaj
        elif self.invincible_timer > 0:
            # Miganie co 1/10 sekundy 
            if int(self.invincible_timer * 10) % 2 != 0:
                 self._draw_body(screen)
                 
        # Normalny stan -> rysuj
        else:
             self._draw_body(screen)

        # Rysowanie paska HP
        self.draw_hp(screen)

    def _draw_body(self, screen):
        # Aktualizacja animacji i rysowanie obrazka przesuniętego względem hitboxa
        draw_x = self.x - self.offset_x
        draw_y = self.y - self.offset_y
        screen.blit(self.image, (draw_x, draw_y))

        # >>> ZMIANA <<<: dorysuj ataki; claws pojawi się PRZED graczem
        if not self.is_dead:
            self.attack_system.draw(screen)

    # =========================
    #        HP — PASEK
    # =========================
    def _load_hp_images(self, hp_paths, hp_size):
        images = []
        if hp_paths is None:
            # UŻYWAJ forward slashy lub raw stringów
            hp_paths = [f"graphics/Interface/HP_Bar{i}.png" for i in range(6)]

        for path in hp_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
            except Exception:
                # awaryjny placeholder
                img = pygame.Surface((80, 16), pygame.SRCALPHA)
            if hp_size:
                img = pygame.transform.smoothscale(img, hp_size)
            images.append(img)

        while len(images) < 6:
            images.append(images[-1])
        return images[:6]

    def set_hp(self, category):
        """Ustaw HP jako kategorię 0..5."""
        self.hp = max(0, min(self.hp_max, int(category)))
        # Sprawdź czy po ustawieniu nie umarł
        if self.hp == 0 and not self.is_dead:
            self.die()

    def add_hp(self, delta):
        """Zmień HP o delta (np. -1 obrażenia, +1 leczenie)."""
        self.set_hp(self.hp + int(delta))

    def draw_hp(self, screen):
        """Narysuj pasek HP (nad graczem lub w HUD) — zgodnie z wcześniejszym zachowaniem."""
        # >>> ZMIANA: zabezpieczenie indeksu (eliminuje IndexError przy wyjściu poza zakres)
        if not hasattr(self, "hp_images") or not self.hp_images:
            return  # brak grafik HP -> nie rysujemy

        max_index = len(self.hp_images) - 1
        try:
            hp_index = int(self.hp)
        except (TypeError, ValueError):
            hp_index = 0
        hp_index = max(0, min(hp_index, max_index))

        img = self.hp_images[hp_index]
        # <<< ZMIANA

        if getattr(self, "_draw_hp_above", True):
            # Pozycjonowanie względem HITBOXA — wycentrowanie nad graczem jak wcześniej
            offset = getattr(self, "_hp_offset", (0, -10))
            x = int(self.x + (self.width - img.get_width()) / 2) + offset[0]
            y = int(self.y - img.get_height()) + offset[1]
            screen.blit(img, (x, y))
        else:
            # Stała pozycja HUD
            hud_pos = getattr(self, "_hp_hud_pos", (16, 16))
            screen.blit(img, hud_pos)