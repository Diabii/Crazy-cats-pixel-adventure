import pygame
import sys
import player
import maps
import map_elements
# import attack
import enemy

pygame.init()
font_lose = map_elements.wczytaj_czcionke(60)

platform_edges = []

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

current_level = "level_1"

# >>> ZMIANA: wczytanie poziomu tolerujące tuple (obstacles, heals) lub samą listę
ret = maps.level_1(screen)
if isinstance(ret, tuple):
    obstacles, current_heals = ret
else:
    obstacles = ret
    current_heals = []   # brak heal’i z mapy
# <<< ZMIANA

enemies = maps.level_1_enemies()

player1_color = (0, 255, 255)
player2_color = (255, 0, 255)

player_obj1 = player.Player(
    "Zolza",
    100, 775, 87, 72, 300, player1_color,
    hp_size=(90, 40),
    draw_hp_above_player=True,
    hp_offset=(0, -8),
    hp_hud_pos=(16, 16)
)

player_obj2 = player.Player(
    "Poki",
    1500, 775, 87, 72, 300, player2_color,
    hp_size=(90, 40),
    draw_hp_above_player=True,
    hp_offset=(0, -8),
    hp_hud_pos=(150, 16)
)

# >>> ZMIANA: helper – wymusza zwrot tylko przeszkód dla add_portal
def _only_obstacles(loader_fn):
    def _wrapped():
        r = loader_fn()
        return r[0] if isinstance(r, tuple) else r
    return _wrapped
# <<< ZMIANA

# >>> ZMIANA: helper do leczenia gracza (bez dotykania klasy Player)
def _apply_heal_to_player(p, amount):
    if getattr(p, "is_dead", False):
        return False
    if hasattr(p, "heal") and callable(getattr(p, "heal")):
        p.heal(amount)
        return True
    if hasattr(p, "hp"):
        max_hp = getattr(p, "max_hp", None)
        if max_hp is not None:
            p.hp = min(max_hp, p.hp + amount)
        else:
            p.hp += amount
        return True
    return False
# <<< ZMIANA

HEAL_AMOUNT = 1  # >>> ZMIANA: ile leczy pojedynczy heal

running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys_pressed = pygame.key.get_pressed()

    # ----- ruch gracza 1 -----
    # >>> ZMIANA: obstacles może być tuple – potrzebujemy listy do .append()
    p1_obstacles = list(obstacles)
    # <<< ZMIANA

    p1_obstacles.append(player_obj2.get_hitbox())
    if not player_obj1.is_dead:
        for e in enemies:
            p1_obstacles.append(e.get_hitbox())

    player_obj1.move(keys_pressed, dt, WIDTH, HEIGHT,
                     pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, p1_obstacles)

    # ----- ruch gracza 2 -----
    # >>> ZMIANA: jw.
    p2_obstacles = list(obstacles)
    # <<< ZMIANA

    p2_obstacles.append(player_obj1.get_hitbox())
    if not player_obj2.is_dead:
        for e in enemies:
            p2_obstacles.append(e.get_hitbox())

    player_obj2.move(keys_pressed, dt, WIDTH, HEIGHT,
                     pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, p2_obstacles)

    # ==============================================================
    #            Portale pomiędzy poziomami
    # ==============================================================

    prev_level = current_level

    # >>> ZMIANA: wrap lamd przy portalach tak, by zwracały WYŁĄCZNIE obstacles
    current_level, obstacles = map_elements.add_portal(
        "level_1",
        "level_2",
        _only_obstacles(lambda: maps.level_2(screen)),
        (1595, 0, 5, 200),
        (50, 400),
        (125, 400),
        player_obj1,
        player_obj2,
        current_level,
        obstacles
    )

    current_level, obstacles = map_elements.add_portal(
        "level_2",
        "level_3",
        _only_obstacles(lambda: maps.level_3(screen)),
        (1595, 0, 5, 200),
        (50, 100),
        (125, 100),
        player_obj1,
        player_obj2,
        current_level,
        obstacles
    )

    current_level, obstacles = map_elements.add_portal(
        "level_3",
        "level_4",
        _only_obstacles(lambda: maps.level_4(screen)),
        (1595, 650, 5, 200),
        (50, 750),
        (125, 750),
        player_obj1,
        player_obj2,
        current_level,
        obstacles
    )

    current_level, obstacles = map_elements.add_portal(
        "level_4",
        "level_5",
        _only_obstacles(lambda: maps.level_5(screen)),
        (0, 0, 5, 200),
        (1500, 750),
        (100, 750),
        player_obj1,
        player_obj2,
        current_level,
        obstacles
    )
    # <<< ZMIANA

    if prev_level != current_level:
        if current_level == "level_1":
            enemies = maps.level_1_enemies()
        elif current_level == "level_2":
            enemies = maps.level_2_enemies()
        elif current_level == "level_3":
            enemies = maps.level_3_enemies()
        elif current_level == "level_4":
            enemies = maps.level_4_enemies()
        elif current_level == "level_5":
            enemies = maps.level_5_enemies()

        # >>> ZMIANA: po zmianie poziomu pobierz też current_heals z mapy
        level_loader = getattr(maps, current_level)
        r = level_loader(screen)
        if isinstance(r, tuple):
            obstacles, current_heals = r[0], r[1]
        else:
            obstacles, current_heals = r, []
        # <<< ZMIANA

    # ==============================================================

    both_dead = player_obj1.is_dead or player_obj2.is_dead

    if both_dead:
        screen.fill((30, 30, 30))
    else:
        screen.fill((0, 60, 110))

    # Rysowanie mapy (ignorujemy zwrot — samo rysowanie tła/ozdób)
    if current_level == "level_1":
        maps.level_1(screen)
    elif current_level == "level_2":
        maps.level_2(screen)
    elif current_level == "level_3":
        maps.level_3(screen)
    elif current_level == "level_4":
        maps.level_4(screen)
    elif current_level == "level_5":
        maps.level_5(screen)

    # >>> ZMIANA: rysowanie heal’i z current_heals (jeśli mapa je zwróciła)
    for h in current_heals:
        if h.get("picked"):
            continue
        x = h.get("x"); y = h.get("y")
        w = h.get("w", 80); hgt = h.get("h", 80)
        prefix = h.get("prefix", "Heal")
        # próbujemy wywołać add_heal z rozmiarem; jeśli nie przyjmuje – fallback
        try:
            map_elements.add_heal(screen, prefix, x, y, w, hgt)
        except TypeError:
            map_elements.add_heal(screen, prefix, x, y)
    # <<< ZMIANA

    # Aktualizacja animacji graczy
    player_obj1.update_anim(dt)
    player_obj2.update_anim(dt)

    # Rysowanie graczy
    player_obj1.draw(screen)
    player_obj2.draw(screen)


    # >>> ZMIANA: wyzwalanie ataków z klawiatury (po rysowaniu — klatka ustawi się na następną iterację)
    player_obj1.attack(keys_pressed, pygame.K_c, pygame.K_v)  # zwykły / super u gracza 1
    player_obj2.attack(keys_pressed, pygame.K_o, pygame.K_p)  # zwykły / super u gracza 2
    # <<< ZMIANA


    # >>> ZMIANA: zbieranie heal’i (prosta kolizja prostokątna)
    for h in current_heals:
        if h.get("picked"):
            continue
        heal_rect = pygame.Rect(h.get("x"), h.get("y"), h.get("w", 80), h.get("h", 80))
        for p in (player_obj1, player_obj2):
            if not p.is_dead and p.get_hitbox().colliderect(heal_rect):
                if _apply_heal_to_player(p, HEAL_AMOUNT):
                    h["picked"] = True
                break
    # <<< ZMIANA

    # attack.update(...) — jak u Ciebie: Player robi to sam

    players = [player_obj1, player_obj2]

    for enemy in enemies[:]:
        enemy.update(dt, obstacles, player=players)
        enemy.draw(screen)

        enemy_hitbox = enemy.get_hitbox()

        for p in players:
            if not p.is_dead:
                if p.get_hitbox().inflate(1, 1).colliderect(enemy_hitbox):
                    p.take_damage(1)

        for p in players:
            claws_rect = p.attack_system.get_claws_hitbox()
            if claws_rect and claws_rect.colliderect(enemy_hitbox):
                enemy.take_damage(2)

            for i in range(len(p.attack_system._projectiles) - 1, -1, -1):
                proj = p.attack_system._projectiles[i]
                proj_img = proj["image"]
                proj_rect = proj_img.get_rect(topleft=(int(proj["pos"].x), int(proj["pos"].y)))
                if proj_rect.colliderect(enemy_hitbox):
                    if enemy.take_damage(1):
                        p.attack_system._projectiles.pop(i)

        # >>> ZMIANA: poprawka literówki (<= bez spacji)
        if enemy.hp <= 0:
            enemies.remove(enemy)
        # <<< ZMIANA

    if both_dead:
        temp_surface = screen.copy()
        gray_surface = pygame.transform.grayscale(temp_surface)
        screen.blit(gray_surface, (0, 0))

        import math
        r = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.005))
        g = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.005 + 2))
        b = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.005 + 4))
        
        lose_text = font_lose.render("YOU LOSE", True, (r, g, b))
        text_rect = lose_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(lose_text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()