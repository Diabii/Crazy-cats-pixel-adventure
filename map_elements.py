import pygame
import os


def load_graphic(nazwa_pliku):
    base_path = os.path.dirname(os.path.abspath(__file__))
    sciezka = os.path.join(base_path, "graphics", "Environment", f"{nazwa_pliku}.png")
    # Dodajemy obsługę błędu, gdyby pliku nie było, aby gra się nie wywaliła od razu
    try:
        return pygame.image.load(sciezka)
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku {nazwa_pliku}")


def add_background_obj(screen, nazwa_pliku, x, y, width=80, height=80):
    screen.blit(pygame.transform.scale(load_graphic(nazwa_pliku), (width, height)), (x, y))



def add_platform(screen, x, y, platform_width, block_width=80, block_height=80):
    """
    Rysuje platformę o szerokości `platform_width` (w liczbie kafelków)
    i zwraca hitbox jako pygame.Rect obejmujący całą platformę.
    """

    # 0) Obsługa przypadków brzegowych zanim załadujemy grafiki
    if platform_width <= 0:
        return None  # nic nie rysujemy i jasny zwrot

    # 1) Przygotuj hitbox (zawsze taki sam kształt dla całej platformy)
    total_width = platform_width * block_width
    off_set_x =5
    off_set_y = 10
    hitbox = pygame.Rect(x+off_set_x, y-off_set_y, total_width-2*off_set_x, block_height/2)

    # 2) Ładujemy i skalujemy grafiki tylko raz
    left_tile   = pygame.transform.scale(load_graphic("Platform_Left"),   (block_width, block_height))
    middle_tile = pygame.transform.scale(load_graphic("Platform_Middle"), (block_width, block_height))
    right_tile  = pygame.transform.scale(load_graphic("Platform_Right"),  (block_width, block_height))

    # 3) Rysowanie
    if platform_width == 1:
        # Jeden kafelek – rysujemy środkowy i ZWRACAMY hitbox
        screen.blit(middle_tile, (x, y))
        return hitbox

    # lewy
    screen.blit(left_tile, (x, y))

    # środki
    for i in range(1, platform_width - 1):
        screen.blit(middle_tile, (x + i * block_width, y))

    # prawy
    screen.blit(right_tile, (x + (platform_width - 1) * block_width, y))

    return hitbox


def add_portal(
    trigger_level, next_level, build_next_level,
    portal_dims, spawn1, spawn2, 
    p1, p2, current_level, obstacles  # ← przekazujemy aktualne przeszkody
    ):
    # Jeśli nie jesteśmy na poziomie z portalem, nic nie zmieniamy
    if current_level != trigger_level:
        return current_level, obstacles


    hb1 = p1.get_hitbox()
    hb2 = p2.get_hitbox()

    x, y, w, h = portal_dims
    portal = [pygame.Rect(x, y, w, h)]

    # Jeżeli obaj gracze są w portalu → przejście
    if p1.collision_test(hb1, portal) and p2.collision_test(hb2, portal):
        p1.x, p1.y = spawn1
        p2.x, p2.y = spawn2

        new_obstacles = build_next_level()  # budujemy TYLKO w momencie przejścia
        return next_level, new_obstacles

    # Brak przejścia → zostajemy na bieżącym poziomie i zachowujemy bieżące przeszkody
    return current_level, obstacles


def wczytaj_czcionke(rozmiar=60):
    base_path = os.path.dirname(os.path.abspath(__file__))
    # Ścieżka: graphics/PressStart2P-Regular.ttf
    font_path = os.path.join(base_path, "graphics", "PressStart2P-Regular.ttf")
    try:
        return pygame.font.Font(font_path, rozmiar)
    except:
        return pygame.font.SysFont("Arial", rozmiar)



def add_heal(screen, nazwa_prefix, x, y, width=80, height=80):
    def load_graphic(nazwa_pliku_bez_rozszerzenia):
        base_path = os.path.dirname(os.path.abspath(__file__))
        sciezka = os.path.join(base_path, "graphics", "Environment", f"{nazwa_pliku_bez_rozszerzenia}.png")
        try:
            # convert_alpha wymaga ustawionego display (set_mode) wcześniej
            return pygame.image.load(sciezka).convert_alpha()
        except (FileNotFoundError, pygame.error) as e:
            print(f"Błąd: Nie znaleziono/wczytano pliku {sciezka}: {e}")
            return None

    # Wczytaj 4 klatki animacji
    frames = []
    for i in range(1, 5):
        filename_no_ext = f"{nazwa_prefix}{i}"  # <-- bez .png (load_graphic dopisze)
        img = load_graphic(filename_no_ext)
        if img is None:
            # przezroczysty placeholder, by nie wywalać gry
            img = pygame.Surface((width, height), pygame.SRCALPHA)
        elif img.get_size() != (width, height):
            img = pygame.transform.scale(img, (width, height))
        frames.append(img)

    # Wylicz aktualną klatkę animacji (zmiana co ~150 ms)
    current_frame = (pygame.time.get_ticks() // 500) % len(frames)

    # Rysuj wybraną klatkę
    screen.blit(frames[current_frame], (x, y))







import os
import pygame

def load_graphic(nazwa_pliku_bez_rozszerzenia, width=None, height=None):
    """
    Wczytuje PNG z katalogu graphics/Environment i opcjonalnie skaluje.
    Zwraca Surface lub None.
    """
    base_path = os.path.dirname(os.path.abspath(__file__))
    sciezka = os.path.join(base_path, "graphics", "Environment", f"{nazwa_pliku_bez_rozszerzenia}.png")
    try:
        surf = pygame.image.load(sciezka).convert_alpha()
        if width is not None and height is not None and surf.get_size() != (width, height):
            surf = pygame.transform.smoothscale(surf, (width, height))
        return surf
    except (FileNotFoundError, pygame.error) as e:
        print(f"Błąd: Nie znaleziono/wczytano pliku {sciezka}: {e}")
        return None


def get_heal_hitbox(nazwa_prefix, x, y, width=80, height=80, frame_index=0, mode="rect"):
    """
    Zwraca hitbox dla obiektu heal.

    Parametry:
      - nazwa_prefix: prefix pliku np. 'heal_' -> wczyta 'heal_1.png', 'heal_2.png', ...
      - x, y: pozycja na ekranie (lewy górny róg)
      - width, height: wymiary rysowania (docelowy rozmiar sprite'a)
      - frame_index: indeks klatki (0..3) jeżeli chcesz liczyć hitbox dla konkretnej klatki
      - mode: 'rect' (szybko, prostokąt), 'tight' (ciasny prostokąt po alfa),
              'mask' (precyzyjna maska + rect)

    Zwraca:
      - dla mode='rect': pygame.Rect
      - dla mode='tight': pygame.Rect (od x,y, dopasowany do treści)
      - dla mode='mask': (pygame.mask.Mask, pygame.Rect)
    """
    mode = mode.lower()
    if mode not in ("rect", "tight", "mask"):
        raise ValueError("mode musi być jednym z: 'rect', 'tight', 'mask'")

    if mode == "rect":
        # najprostszy i najszybszy – stały prostokąt
        return pygame.Rect(x, y, width, height)

    # dla tight/mask potrzebujemy konkretnej bitmapy (np. aktualnej klatki)
    # Twoje pliki to nazwa_prefix + (1..4), więc dopasujmy frame_index do zakresu 1..4
    frame_num = (frame_index % 4) + 1
    filename_no_ext = f"{nazwa_prefix}{frame_num}"

    surf = load_graphic(filename_no_ext, width, height)
    if surf is None:
        # fallback – brak grafiki -> prawie jak tryb 'rect'
        rect = pygame.Rect(x, y, width, height)
        if mode == "mask":
            # pustą maskę też można zwrócić, ale kolizje zawsze False
            empty_mask = pygame.mask.Mask((width, height), fill=False)
            return empty_mask, rect
        return rect

    if mode == "tight":
        # obliczamy bounding box nieprzezroczystych pikseli (alfa > 0)
        mask = pygame.mask.from_surface(surf)  # domyślnie próg alfa = 127; dla 0 -> threshold=1
        bbox = mask.get_bounding_rects()
        if not bbox:
            # całkiem przezroczyste – fallback do prostego rect
            return pygame.Rect(x, y, width, height)
        # get_bounding_rects może zwrócić listę; scalmy do wspólnego bounding rect
        tight_rect_local = bbox[0].copy()
        for r in bbox[1:]:
            tight_rect_local.union_ip(r)
        # przesuwamy do pozycji na ekranie
        tight_rect_screen = tight_rect_local.move(x, y)
        return tight_rect_screen

    if mode == "mask":
        mask = pygame.mask.from_surface(surf)
        rect = pygame.Rect(x, y, width, height)
        return mask, rect


def add_heal(screen, nazwa_prefix, x, y, width=80, height=80, return_hitbox=False, hitbox_mode="rect"):
    """
    Rysuje animowany 'heal' i opcjonalnie zwraca hitbox aktualnej klatki.
    """
    # Wczytaj 4 klatki animacji
    frames = []
    for i in range(1, 5):
        filename_no_ext = f"{nazwa_prefix}{i}"  # bez .png (load_graphic dopisze)
        img = load_graphic(filename_no_ext, width, height)
        if img is None:
            # przezroczysty placeholder, by nie wywalać gry
            img = pygame.Surface((width, height), pygame.SRCALPHA)
        frames.append(img)

    # Wylicz aktualną klatkę animacji (zmiana co ~150 ms)
    current_frame = (pygame.time.get_ticks() // 150) % len(frames)

    # Rysuj wybraną klatkę
    screen.blit(frames[current_frame], (x, y))

    if return_hitbox:
        return get_heal_hitbox(
            nazwa_prefix=nazwa_prefix,
            x=x,
            y=y,
            width=width,
            height=height,
            frame_index=current_frame,
            mode=hitbox_mode
        )
    # Domyślnie nic nie zwracamy (jak wcześniej)