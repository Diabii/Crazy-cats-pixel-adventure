
import pygame
import os


base_path = os.path.dirname(os.path.abspath(__file__))

def wczytaj_postacie(width, height, nazwa_postaci="Zolza"):

    def load_seq(nazwa_postaci, akcja, start, end):

        def load_cat(nazwa_postaci, nazwa_pliku):
            sciezka = os.path.join(base_path, "graphics", "Cats", nazwa_postaci, nazwa_pliku)
            # Dodajemy obsługę błędu, gdyby pliku nie było, aby gra się nie wywaliła od razu
            try:
                return pygame.image.load(sciezka)
            except FileNotFoundError:
                print(f"Błąd: Nie znaleziono pliku {nazwa_pliku}")

        def skaluj(obrazek):
            return pygame.transform.scale(obrazek, (width, height))
    
        lista = []
        for i in range(start, end + 1):
            obrazek = skaluj(load_cat(nazwa_postaci, f"{nazwa_postaci}_{akcja}{i}.png"))
            lista.append(obrazek)
        return lista

    grafiki = {}
    
    # BIEGANIE
    grafiki['run_right'] = load_seq(nazwa_postaci, "Move_Right", 1, 4)
    grafiki['run_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['run_right']]

    # IDLE (Stanie)
    grafiki['idle_right'] = load_seq(nazwa_postaci, "Idle_Right", 1, 9)
    grafiki['idle_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['idle_right']]

    # SKOK (Start)
    grafiki['jump_start_right'] = load_seq(nazwa_postaci, "JumpStart_Right", 1, 3)
    grafiki['jump_start_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['jump_start_right']]

    # SKOK (Pętla)
    grafiki['jump_loop_right'] = load_seq(nazwa_postaci, "Jump_Right", 1, 3)
    grafiki['jump_loop_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['jump_loop_right']]

    # SKOK (Lądowanie)
    grafiki['jump_end_right'] = load_seq(nazwa_postaci, "JumpToFall_Right", 1, 3)
    grafiki['jump_end_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['jump_end_right']]

    # SPADANIE
    grafiki['fall_right'] = load_seq(nazwa_postaci, "Fall_Right", 1, 3)
    grafiki['fall_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['fall_right']]

    grafiki['attack_right'] = load_seq(nazwa_postaci, "Attack", 1, 1)
    grafiki['attack_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['attack_right']]

    grafiki['super_attack_right'] = load_seq(nazwa_postaci, "SuperAttack", 1, 1)
    grafiki['super_attack_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['super_attack_right']]


    return grafiki





# ==================================================
#                   ŚCIEŻKI
# ==================================================
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# ==================================================
#              ŁADOWANIE GRAFIK ATAKÓW
# ==================================================
def wczytaj_ataki(width=60, height=60):
    """
    Ładuje klatki animacji efektów ataku z katalogu:
    graphics/Attacks/
        - Claws1..3.png
        - Fireball1..3.png
        - Leaves1..3.png
        - Pickles1..3.png

    Zwraca słownik klatek (prawo/lewo) z bezpiecznym fallbackiem,
    aby gra nie wywaliła się przy braku pliku.
    """
    def load_seq_attack(nazwa_pliku, start, end):
        def load_attack(nazwa_pliku_pełna):
            sciezka = os.path.join(BASE_PATH, "graphics", "Attacks", nazwa_pliku_pełna)
            try:
                return pygame.image.load(sciezka).convert_alpha()
            except FileNotFoundError:
                print(f"Błąd: Nie znaleziono pliku {nazwa_pliku_pełna}")
                # przezroczysty placeholder, by nie wywalać gry
                return pygame.Surface((width, height), pygame.SRCALPHA)

        def skaluj(obrazek):
            return pygame.transform.scale(obrazek, (width, height))

        lista = []
        for i in range(start, end + 1):
            obrazek = skaluj(load_attack(f"{nazwa_pliku}{i}.png"))
            lista.append(obrazek)
        return lista

    grafiki = {}

    grafiki['claws_right'] = load_seq_attack("Claws", 1, 3)
    grafiki['claws_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['claws_right']]

    grafiki['fireball_right'] = load_seq_attack("Fireball", 1, 3)
    grafiki['fireball_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['fireball_right']]

    grafiki['leaves_right'] = load_seq_attack("Leaves", 1, 3)
    grafiki['leaves_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['leaves_right']]

    grafiki['pickles_right'] = load_seq_attack("Pickles", 1, 3)
    grafiki['pickles_left']  = [pygame.transform.flip(img, True, False) for img in grafiki['pickles_right']]

    return grafiki


