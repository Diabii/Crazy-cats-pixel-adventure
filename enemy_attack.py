import pygame
import os
import math
from typing import List, Optional, Union

# ==================================================
#                    KLASA ATTACK
# ==================================================
class Attack:
    """
    System ataków dla dowolnego ownera (Player lub EnemyBase).
    - 'claws' (melee): 3 klatki, wyświetlane przed ownerem; nie poruszają się.
    - 'fireball' (projectile): 3 klatki pętli, pocisk leci od ownera w jego kierunku.

    Wymagane grafiki w słowniku gfx:
        gfx['claws_right'],  gfx['claws_left']    -> list[Surface] (3 klatki)
        gfx['fireball_right'], gfx['fireball_left'] -> list[Surface] (3 klatki)
    """

    def __init__(
        self,
        owner,
        gfx: dict,
        claws_frame_time: float = 0.06,
        fireball_frame_time: float = 0.06,
        fireball_speed: float = 700.0,
        fireball_lifetime: float = 1.2,
        claws_forward_pad: int = 8,
        claws_vertical_align: str = "center",
        claws_damage: int = 1,
        fireball_damage: int = 1,
        claws_cooldown: float = 0.35,
        fireball_cooldown: float = 0.6,
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
        self.claws_damage = claws_damage
        self.fireball_damage = fireball_damage

        # --- Cooldowny ---
        self._claws_cooldown_left = 0.0
        self._fireball_cooldown_left = 0.0
        self._claws_cooldown = 3.0 # Czas cooldownu claws żeby nie zaspamować
        self._fireball_cooldown = 4.0 # Czas cooldownu fireball żeby nie zaspamować

        # --- Stan melee (claws) ---
        self._claws_active = False
        self._claws_frames: Optional[List[pygame.Surface]] = None
        self._claws_index = 0
        self._claws_timer = 0.0
        self._claws_pos = pygame.Vector2(0, 0)  # top-left
        self._claws_image: Optional[pygame.Surface] = None
        self._claws_did_damage = False

        # --- Stan pocisków (fireball) ---
        self._projectiles: List[dict] = []

    # ---------- POMOCNICZE ----------
    def _facing_right(self) -> bool:
        d = getattr(self.owner, "direction", "right")
        if isinstance(d, str):
            return d == "right"
        try:
            return float(d) > 0
        except Exception:
            return True

    def _get_hitbox(self) -> pygame.Rect:
        if hasattr(self.owner, "get_hitbox") and callable(self.owner.get_hitbox):
            rect = self.owner.get_hitbox()
            if isinstance(rect, pygame.Rect):
                return rect
        x = int(getattr(self.owner, "x", 0))
        y = int(getattr(self.owner, "y", 0))
        w = int(getattr(self.owner, "width", 0))
        h = int(getattr(self.owner, "height", 0))
        return pygame.Rect(x, y, w, h)

    def _get_frames(self, base_key: str) -> Optional[List[pygame.Surface]]:
        key = f"{base_key}_{'right' if self._facing_right() else 'left'}"
        frames = self.gfx.get(key, None)
        return frames if frames else None

    # ---------- TRIGGERY ----------
    def start_claws(self, force=False):
        if self._claws_cooldown_left > 0 and not force:
            return
        frames = self._get_frames("claws")
        if not frames:
            return

        self._claws_active = True
        self._claws_frames = frames
        self._claws_index = 0
        self._claws_timer = 0.0
        self._claws_image = frames[0]
        self._claws_did_damage = False
        self._claws_cooldown_left = self._claws_cooldown

        hb = self._get_hitbox()
        fw = self._claws_image.get_width()
        fh = self._claws_image.get_height()

        if self._facing_right():
            x = hb.right + self.claws_forward_pad
        else:
            x = hb.left - fw - self.claws_forward_pad

        if self.claws_vertical_align == "top":
            y = hb.top
        elif self.claws_vertical_align == "bottom":
            y = hb.bottom - fh
        else:
            y = hb.top + (hb.height - fh) / 2

        self._claws_pos.update(x, y)

    def start_fireball(self, force=False):
        if self._fireball_cooldown_left > 0 and not force:
            return
        frames = self._get_frames("fireball")
        if not frames:
            return

        first = frames[0]
        fw, fh = first.get_width(), first.get_height()

        hb = self._get_hitbox()
        if self._facing_right():
            x = hb.right
            vel = pygame.Vector2(self.fireball_speed, 0)
        else:
            x = hb.left - fw
            vel = pygame.Vector2(-self.fireball_speed, 0)

        y = hb.top + (hb.height - fh) / 2

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
        self._fireball_cooldown_left = self._fireball_cooldown

    # ---------- UPDATE / DRAW ----------
    def update(
        self,
        dt: float,
        obstacles: Optional[List[pygame.Rect]] = None,
        world_bounds: Optional[tuple] = None,
        targets: Optional[Union[List[object], object]] = None,
    ):
        if self._claws_cooldown_left > 0:
            self._claws_cooldown_left -= dt
        if self._fireball_cooldown_left > 0:
            self._fireball_cooldown_left -= dt

        # --- melee claws ---
        if self._claws_active and self._claws_frames:
            self._claws_timer += dt
            while self._claws_timer >= self.claws_frame_time:
                self._claws_timer -= self.claws_frame_time
                self._claws_index += 1
                if self._claws_index < len(self._claws_frames):
                    self._claws_image = self._claws_frames[self._claws_index]
                else:
                    self._claws_active = False
                    self._claws_frames = None
                    self._claws_image = None
                    break

            # okno trafienia można tu też wprowadzić (np. tylko klatka środkowa)

            # kolizja z targets (jednorazowe obrażenia)
            if not self._claws_did_damage and targets and self._claws_image:
                claws_rect = self.get_claws_hitbox()
                if claws_rect:
                    for t in (targets if isinstance(targets, list) else [targets]):
                        tr = self._get_target_hitbox(t)
                        if claws_rect.colliderect(tr):
                            self._apply_damage(t, self.claws_damage)
                            self._claws_did_damage = True
                            break

        # --- pociski ---
        if obstacles is None:
            obstacles = []

        to_remove = []
        for i, p in enumerate(self._projectiles):
            p["pos"] += p["vel"] * dt

            p["timer"] += dt
            while p["timer"] >= self.fireball_frame_time:
                p["timer"] -= self.fireball_frame_time
                p["idx"] = (p["idx"] + 1) % len(p["frames"])
                p["image"] = p["frames"][p["idx"]]

            p["life"] -= dt
            if p["life"] <= 0:
                to_remove.append(i)
                continue

            img = p["image"]
            rect = img.get_rect(topleft=(int(p["pos"].x), int(p["pos"].y)))

            # przeszkody
            hit_obstacle = False
            for obst in obstacles:
                if rect.colliderect(obst):
                    to_remove.append(i)
                    hit_obstacle = True
                    break
            if hit_obstacle:
                continue

            # targets
            if targets:
                for t in (targets if isinstance(targets, list) else [targets]):
                    tr = self._get_target_hitbox(t)
                    if rect.colliderect(tr):
                        self._apply_damage(t, self.fireball_damage)
                        to_remove.append(i)
                        break

            # granice świata
            if world_bounds:
                W, H = world_bounds
                if rect.right < 0 or rect.left > W or rect.bottom < 0 or rect.top > H:
                    to_remove.append(i)

        for idx in reversed(to_remove):
            self._projectiles.pop(idx)

    def draw(self, screen):
        for p in self._projectiles:
            screen.blit(p["image"], (int(p["pos"].x), int(p["pos"].y)))

        if self._claws_active and self._claws_image:
            screen.blit(self._claws_image, (int(self._claws_pos.x), int(self._claws_pos.y)))

    # ---------- HITBOXY ----------
    def get_claws_hitbox(self) -> Optional[pygame.Rect]:
        if not self._claws_active or not self._claws_image:
            return None
        return pygame.Rect(
            int(self._claws_pos.x),
            int(self._claws_pos.y),
            self._claws_image.get_width(),
            self._claws_image.get_height()
        )

    def get_projectile_hitboxes(self) -> List[pygame.Rect]:
        rects = []
        for p in self._projectiles:
            img = p["image"]
            r = img.get_rect(topleft=(int(p["pos"].x), int(p["pos"].y)))
            rects.append(r)
        return rects

    # ---------- POMOCNICZE (targets/damage) ----------
    def _get_target_hitbox(self, target) -> pygame.Rect:
        if hasattr(target, "get_hitbox") and callable(target.get_hitbox):
            rect = target.get_hitbox()
            if isinstance(rect, pygame.Rect):
                return rect
        x = int(getattr(target, "x", 0))
        y = int(getattr(target, "y", 0))
        w = int(getattr(target, "width", 0))
        h = int(getattr(target, "height", 0))
        return pygame.Rect(x, y, w, h)

    def _apply_damage(self, target, amount: int):
        if hasattr(target, "take_damage") and callable(target.take_damage):
            try:
                target.take_damage(amount)
            except Exception:
                pass

