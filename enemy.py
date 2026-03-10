# enemy.py
import pygame
import os
import math
from typing import List, Optional, Union
from enemy_attack import Attack
from animation_tools import wczytaj_ataki
# ==================================================
#                   ŚCIEŻKI
# ==================================================
BASE_PATH = os.path.dirname(os.path.abspath(__file__))




# ==================================================
#                     ENEMY BASE
# ==================================================
class EnemyBase:
    def __init__(
        self,
        x, y,
        image_width, image_height,
        hitbox_size,
        hp_max=3,
        hp_size=(57, 15),
        hp_offset=(0, 0),
    ):
        # --- HIT COOLDOWN ---
        self.hit_cooldown = 0

        # --- POZYCJA HITBOXA ---
        self.x = x
        self.y = y

        # --- SPRITE ---
        self.image_width = image_width
        self.image_height = image_height

        # --- HITBOX ---
        self.width, self.height = hitbox_size
        self.offset_x = (self.image_width - self.width) // 2
        self.offset_y = 2  # 2 px od góry

        # --- HP ---
        self.hp_max = hp_max
        self.hp = hp_max
        self.hp_offset = hp_offset
        self.hp_images = self._load_hp_images(hp_size)

        # --- ANIMACJA ---
        self.animation_count = 0
        self.image = None
        self.mask = None
        self.is_attacking = False

        # --- RUCH / FIZYKA ---
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 1
        self.gravity = 0.6
        self.max_fall_speed = 10
        self.on_ground = False
        self.direction = -1  # -1 = lewo, 1 = prawo
        self.turn_cooldown = 0

        # --- parametry detekcji (Awokado) ---
        self.attack_radius = 175

        # --- DAMAGE FLASH ---
        self.damage_flash_time = 0.0
        self.damage_flash_duration = 0.15  # sekundy


    # =========================
    #        HITBOX
    # =========================
    def get_hitbox(self):
        top_crop = getattr(self, "hitbox_top_crop", 0)
        return pygame.Rect(self.x, self.y + top_crop, self.width, self.height - top_crop)

    # =========================
    #          HP
    # =========================
    def _load_hp_images(self, hp_size):
        images = []
        for i in range(5):
            path = os.path.join(BASE_PATH, "graphics", "Interface", f"HP_enemy{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, hp_size)
            except Exception:
                img = pygame.Surface(hp_size, pygame.SRCALPHA)
            images.append(img)
        return images[::-1]

    def set_hp(self, value):
        self.hp = max(0, min(self.hp_max, int(value)))

    # =========================
    #         DRAW
    # =========================
    def draw(self, screen):
        draw_x = self.x - self.offset_x
        draw_y = self.y - self.offset_y

        image_to_draw = pygame.transform.flip(self.image, True, False) if self.direction == 1 else self.image
        screen.blit(image_to_draw, (draw_x, draw_y))
        self.draw_hp(screen)

    def draw_hp(self, screen):
        img = self.hp_images[self.hp]
        x = int(self.x + (self.width - img.get_width()) / 2) + self.hp_offset[0]
        y = int(self.y - img.get_height()) + self.hp_offset[1]
        screen.blit(img, (x, y))

    # =========================
    #    DOSTAWANIE OBRAŻEŃ
    # =========================
    def take_damage(self, amount):
        """Zwraca True, jeśli wróg otrzymał obrażenia; False, jeśli cooldown."""
        if self.hit_cooldown > 0:
            return False

        self.hp -= amount
        self.hit_cooldown = 0.4  # 0.4 s przed następnym ciosem
        self.vel_y = -3  # odrzut
        self.damage_flash_time = self.damage_flash_duration
        return True

    # =========================
    #        FIZYKA
    # =========================
    def apply_gravity(self):
        if not self.on_ground:
            self.vel_y += self.gravity
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed

    def move(self, obstacles, window_width=None, window_height=None):
        self.x += self.vel_x
        hitbox = self.get_hitbox()

        for o in obstacles:
            if hitbox.colliderect(o):
                if self.vel_x > 0:
                    self.x = o.left - self.width
                elif self.vel_x < 0:
                    self.x = o.right
                self.vel_x = 0
                self.reverse_direction()
                break

        self.y += self.vel_y
        hitbox = self.get_hitbox()
        self.on_ground = False

        for o in obstacles:
            if hitbox.colliderect(o):
                if self.vel_y > 0:
                    self.y = o.top - self.height
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.y = o.bottom
                    self.vel_y = 0
                break

        if window_width:
            if self.x < 0:
                self.x = 0
                self.reverse_direction()
            elif self.x > window_width - self.width:
                self.x = window_width - self.width
                self.reverse_direction()

        if window_height:
            if self.y >= window_height - self.height:
                self.y = window_height - self.height
                self.vel_y = 0
                self.on_ground = True

    # ===========================
    # DETEKCJA KRAWĘDZI PLATFORMY
    # ===========================
    def check_platform_edge(self, obstacles):
        if self.direction == 1:  # idzie w prawo
            foot_x = self.x + self.width + 1
        else:  # idzie w lewo
            foot_x = self.x - 1
        foot_y = self.y + self.height + 1

        foot_point = pygame.Rect(foot_x, foot_y, 1, 1)

        if not any(foot_point.colliderect(o) for o in obstacles):
            self.reverse_direction()

    # =========================
    #      OBRÓT ZIUTKA
    # =========================
    def reverse_direction(self):
        if self.turn_cooldown <= 0:
            self.direction *= -1
            self.turn_cooldown = 10

    # =========================
    #        UPDATE
    # =========================
    def update(self, dt, obstacles, player=None, window_width=1600, window_height=900, can_move=True):
        if self.turn_cooldown > 0:
            self.turn_cooldown -= 1

        if self.hit_cooldown > 0:
            self.hit_cooldown -= dt

        if self.damage_flash_time > 0:
            self.damage_flash_time -= dt


        # --- sprawdzanie ataku względem gracza/graczy ---
        attacking = False
        if player:
            if isinstance(player, list):
                for p in player:
                    if self.check_attack_range(p):
                        attacking = True
            else:
                if self.check_attack_range(player):
                    attacking = True
        self.is_attacking = attacking

        # --- ustaw kierunek w stronę najbliższego gracza, jeśli atakuje ---
        if self.is_attacking and player:
            if isinstance(player, list):
                nearest_player = min(player, key=lambda p: math.hypot(
                    (p.x + p.width / 2) - (self.x + self.width / 2),
                    (p.y + p.height / 2) - (self.y + self.height / 2)
                ))
            else:
                nearest_player = player

            enemy_center_x = self.x + self.width / 2
            player_center_x = nearest_player.x + nearest_player.width / 2
            self.direction = 1 if player_center_x > enemy_center_x else -1

        # --- ruch w poziomie, blokada przy ataku ---
        effective_can_move = can_move and not self.is_attacking
        self.vel_x = self.speed * self.direction if effective_can_move else 0

        # --- grawitacja i ruch ---
        self.apply_gravity()
        self.move(obstacles, window_width, window_height)
        self.check_platform_edge(obstacles)

        # --- animacja ---
        sprites = self.animations["attack"] if self.is_attacking else self.animations["walk"]
        self.animation_count += self.anim_speed * dt
        index = int(self.animation_count) % len(sprites)
        self.image = sprites[index]
        self.mask = pygame.mask.from_surface(self.image)

    # =========================
    #    DETEKCJA RANGE ATAKU
    # =========================
    def check_attack_range(self, player):
        center_x = self.x + self.width / 2
        center_y = self.y + self.height
        player_center_x = player.x + player.width / 2
        player_center_y = player.y + player.height / 2
        dx = player_center_x - center_x
        dy = player_center_y - center_y
        distance = math.hypot(dx, dy)

        if distance > getattr(self, "attack_radius", 175):
            return False

        if dy < 0:
            return True
        return False


# ==================================================
#                     OGÓREK
# ==================================================
class Cucumber(EnemyBase):
    def __init__(self, x, y):
        WORLD_SCALE = 0.25
        self.animations = self._load_animations(WORLD_SCALE)
        first_img = self.animations["walk"][0]

        super().__init__(
            x, y,
            image_width=first_img.get_width(),
            image_height=first_img.get_height(),
            hitbox_size=(first_img.get_width(), first_img.get_height() - 2)
        )

        # --- Pomelo/Mandarynka ---
        self.hitbox_top_crop = 12
        self.sprite_offset_y = 10
        self.anim_speed = 4
        self.image = first_img
        self.mask = pygame.mask.from_surface(self.image)

        # --- parametry zachowania ---
        self.speed = 4
        self.attack_radius = 550 # ogórek wykrywa nieco dalej

        # --- Wczytanie grafik efektów ataku ---
        full_gfx = wczytaj_ataki(width=60, height=60)

        # --- MAPOWANIE: pickles -> fireball (pociski) ---
        mapped_gfx = {
            "fireball_right": full_gfx.get("pickles_right", []),
            "fireball_left":  full_gfx.get("pickles_left", [])
        }
        self.attack = Attack(
            owner=self,
            gfx=mapped_gfx,
            fireball_damage=1,
            fireball_speed=520.0,
            fireball_lifetime=1.4,
            fireball_frame_time=0.06,
            fireball_cooldown=1.2
        )

    def _load_animations(self, scale):
        def load(name):
            path = os.path.join(BASE_PATH, "graphics", "Enemies", name)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(
                img,
                (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            return img

        walk_frames = []
        for img_name in ["Cucumber_walk1.png", "Cucumber_walk2.png"]:
            img = load(img_name)
            walk_frames.extend([img] * 2)

        attack_frames = []
        for img_name in ["Cucumber_attack1.png", "Cucumber_attack2.png"]:
            img = load(img_name)
            attack_frames.extend([img] * 2)

        return {"walk": walk_frames, "attack": attack_frames}

    def update(self, dt, obstacles, player=None, window_width=1600, window_height=900, can_move=True):
        # najpierw standardowa logika ruchu/animacji + wyliczenie is_attacking
        super().update(dt, obstacles, player, window_width, window_height, can_move)

        # === ATTACK GATING (3. rozwiązanie) ===
        # Wybierz najbliższego gracza (jeśli lista), oblicz kierunek docelowy i
        # odpal atak dopiero, gdy w tej klatce już patrzy we właściwą stronę.
        nearest_player = None
        if player:
            if isinstance(player, list) and len(player) > 0:
                nearest_player = min(player, key=lambda p: math.hypot(
                    (p.x + p.width / 2) - (self.x + self.width / 2),
                    (p.y + p.height / 2) - (self.y + self.height / 2)
                ))
            elif not isinstance(player, list):
                nearest_player = player

        if self.is_attacking and nearest_player:
            enemy_center_x = self.x + self.width / 2
            player_center_x = nearest_player.x + nearest_player.width / 2
            desired_dir = 1 if player_center_x > enemy_center_x else -1

            if self.direction != desired_dir:
                # najpierw obróć się – bez strzału w tej klatce
                self.direction = desired_dir
            else:
                # już patrzy prawidłowo → można strzelać
                self.attack.start_fireball()

        # aktualizacja efektów ataku
        self.attack.update(
            dt,
            obstacles=obstacles,
            world_bounds=(window_width, window_height),
            targets=player
        )

    def draw(self, screen):
        draw_x = self.x - self.offset_x
        draw_y = self.y - self.offset_y + getattr(self, "sprite_offset_y", 0)
        image_to_draw = pygame.transform.flip(self.image, True, False) if self.direction == 1 else self.image
        screen.blit(image_to_draw, (draw_x, draw_y))
        self.draw_hp(screen)

        if self.damage_flash_time > 0:
            flash = image_to_draw.copy()
            flash.fill((255, 60, 60, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(flash, (draw_x, draw_y))



        # pociski (pickles)
        self.attack.draw(screen)


# ==================================================
#                     BANAN
# ==================================================
class Banana(EnemyBase):
    def __init__(self, x, y):
        WORLD_SCALE = 0.25
        self.animations = self._load_animations(WORLD_SCALE)
        first_img = self.animations["walk"][0]

        super().__init__(
            x, y,
            image_width=first_img.get_width(),
            image_height=first_img.get_height(),
            hitbox_size=(first_img.get_width(), first_img.get_height() - 2)
        )

        # --- Pomelo/Mandarynka ---
        self.hitbox_top_crop = 6
        self.sprite_offset_y = 10
        self.anim_speed = 4
        self.image = first_img
        self.mask = pygame.mask.from_surface(self.image)

        # --- parametry zachowania ---
        self.speed = 4
        self.attack_radius = 120  # bliższy zasięg dla melee

        # --- Wczytanie grafik efektów ataku ---
        full_gfx = wczytaj_ataki(width=60, height=60)

        # --- MAPOWANIE: leaves -> claws (melee) ---
        mapped_gfx = {
            "claws_right": full_gfx.get("leaves_right", []),
            "claws_left":  full_gfx.get("leaves_left", [])
        }
        self.attack = Attack(
            owner=self,
            gfx=mapped_gfx,
            claws_damage=1,
            claws_forward_pad=8,
            claws_vertical_align="center",
            claws_frame_time=0.06,
            claws_cooldown=1.2
        )

    def _load_animations(self, scale):
        def load(name):
            path = os.path.join(BASE_PATH, "graphics", "Enemies", name)
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(
                img,
                (int(img.get_width() * scale), int(img.get_height() * scale))
            )
            return img

        walk_frames = []
        for img_name in ["Banana_walk1.png", "Banana_walk2.png"]:
            img = load(img_name)
            walk_frames.extend([img] * 2)

        attack_frames = []
        for img_name in ["Banana_attack1.png", "Banana_attack2.png"]:
            img = load(img_name)
            attack_frames.extend([img] * 2)

        return {"walk": walk_frames, "attack": attack_frames}

    def update(self, dt, obstacles, player=None, window_width=1600, window_height=900, can_move=True):
        # najpierw standardowa logika ruchu/animacji + wyliczenie is_attacking
        super().update(dt, obstacles, player, window_width, window_height, can_move)

        # === ATTACK GATING (3. rozwiązanie) ===
        nearest_player = None
        if player:
            if isinstance(player, list) and len(player) > 0:
                nearest_player = min(player, key=lambda p: math.hypot(
                    (p.x + p.width / 2) - (self.x + self.width / 2),
                    (p.y + p.height / 2) - (self.y + self.height / 2)
                ))
            elif not isinstance(player, list):
                nearest_player = player

        if self.is_attacking and nearest_player:
            enemy_center_x = self.x + self.width / 2
            player_center_x = nearest_player.x + nearest_player.width / 2
            desired_dir = 1 if player_center_x > enemy_center_x else -1

            if self.direction != desired_dir:
                # najpierw obróć się – bez ciosu w tej klatce
                self.direction = desired_dir
            else:
                # już patrzy prawidłowo → można uderzyć (leaves -> claws)
                self.attack.start_claws()

        # aktualizacja efektów ataku
        self.attack.update(
            dt,
            obstacles=obstacles,
            world_bounds=(window_width, window_height),
            targets=player
        )

    def draw(self, screen):
        draw_x = self.x - self.offset_x
        draw_y = self.y - self.offset_y + getattr(self, "sprite_offset_y", 0)
        image_to_draw = pygame.transform.flip(self.image, True, False) if self.direction == 1 else self.image
        screen.blit(image_to_draw, (draw_x, draw_y))
        self.draw_hp(screen)

        if self.damage_flash_time > 0:
            flash = image_to_draw.copy()
            flash.fill((255, 60, 60, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(flash, (draw_x, draw_y))


        # pazury (leaves)
        self.attack.draw(screen)