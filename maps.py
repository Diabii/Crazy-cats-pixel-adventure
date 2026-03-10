import map_elements
import enemy

'''
Platformy są numerowane z góry do dołu, lewo prawo - jak piksele.
Ozdoby: -75 od osi Y platformy
Drzewa: -235 od osi Y platformy
Enemy: -110 od osi Y platformy
'''


def level_1(screen):    # LEVEL 1!!!
    
    
    
    
    # Platforma 1
    map_elements.add_background_obj(screen, "Bush1", 100, 125),
    map_elements.add_background_obj(screen, "Flower", 50, 125),
    
    # Platforma 2
    map_elements.add_background_obj(screen, "Tree", 1400, 10, 128, 200),
    map_elements.add_background_obj(screen, "Bush2", 1350, 125),
    map_elements.add_background_obj(screen, "Log", 1050, 125),
    map_elements.add_background_obj(screen, "Grass", 1100, 125),
    map_elements.add_background_obj(screen, "Sign_Direction_Right", 1225, 125),

    # Platforma 3
    map_elements.add_background_obj(screen, "Grass", 375, 225),

    # Platforma 4
    map_elements.add_background_obj(screen, "Tree", 750, 165, 160, 250),
    map_elements.add_background_obj(screen, "Grass", 825, 325),

    # Platforma 5
    map_elements.add_background_obj(screen, "Tree", 1200, 255, 160, 250),
    map_elements.add_background_obj(screen, "Bush1", 1250, 415),
    map_elements.add_background_obj(screen, "Log", 1315, 415),

    # Platforma 6
    map_elements.add_background_obj(screen, "Tree", 100, 315, 160, 250),
    map_elements.add_background_obj(screen, "Bush2", 75, 475),
    map_elements.add_background_obj(screen, "Mushroom", 200, 475),

    # Platforma 7
    map_elements.add_background_obj(screen, "Grass", 490, 575),
    map_elements.add_background_obj(screen, "Tree", 550, 460, 128, 200),
    map_elements.add_background_obj(screen, "Bush1", 650, 575),
    map_elements.add_background_obj(screen, "Bush2", 715, 575),

    # Platforma 8
    map_elements.add_background_obj(screen, "Bush1", 1400, 625),
    map_elements.add_background_obj(screen, "Bush2", 1350, 625),
    map_elements.add_background_obj(screen, "Mushroom", 1475, 625),

    # 9 platforma
    map_elements.add_background_obj(screen, "Grass", 175, 775),
    map_elements.add_background_obj(screen, "Tree", 250, 615, 160, 250),
    map_elements.add_background_obj(screen, "Sign_Skull", 220, 775),
    map_elements.add_background_obj(screen, "Bush1", 350, 775),
    map_elements.add_background_obj(screen, "Grass", 615, 775),
    map_elements.add_background_obj(screen, "Flower", 590, 775),
    map_elements.add_background_obj(screen, "Bush1", 900, 775),
    map_elements.add_background_obj(screen, "Mushroom", 1000, 775),
    map_elements.add_background_obj(screen, "Grass", 1200, 775),
    map_elements.add_background_obj(screen, "Log", 1250, 775),
    map_elements.add_background_obj(screen, "Bush2", 1500, 775),
    



       
    heals = [
        {"prefix": "Heal", "x": 150,  "y": 120,  "w": 80, "h": 80, "picked": False},  # przy P1
    ]

    obstacles = [




    map_elements.add_platform(screen, 0, 850, platform_width=20),   # Platforma 9
    map_elements.add_platform(screen, 1120, 700, platform_width=6),    # Platforma 8
    map_elements.add_platform(screen, 500, 650, platform_width=5),  # Platforma 7
    map_elements.add_platform(screen, 0, 550, platform_width=6),    # Platforma 6
    map_elements.add_platform(screen, 1200, 490, platform_width=4),    # Platforma 5
    map_elements.add_platform(screen, 700, 400, platform_width=4),  # Platforma 4
    map_elements.add_platform(screen, 375, 300, platform_width=2),  # Platforma 3
    map_elements.add_platform(screen, 50, 200, platform_width=4),    # Platforma 1
    map_elements.add_platform(screen, 960, 200, platform_width=8),    # Platforma 2
    ]
       
    return obstacles, heals


def level_1_enemies():
    return [
       # enemy.Cucumber(100, 90),    # P1
       # enemy.Banana(1400, 90),     # P2
       # enemy.Banana(800, 290),     # P4
       # enemy.Cucumber(300, 440),   # P6
       # enemy.Banana(1125, 590),    # P8
    ]


def level_2(screen):    # LEVEL 2!!!
    # P1
    map_elements.add_background_obj(screen, "Bush2", 525, 25),
    map_elements.add_background_obj(screen, "Flower", 600, 25),

    # P2
    map_elements.add_background_obj(screen, "Grass", 850, 125),
    map_elements.add_background_obj(screen, "Log", 900, 125),

    # P3
    map_elements.add_background_obj(screen, "Bush2", 1225, 125),
    map_elements.add_background_obj(screen, "Flower", 1175, 125),

    # P4
    map_elements.add_background_obj(screen, "Tree", 1500, 10, 128, 200),
    map_elements.add_background_obj(screen, "Sign_Direction_Right", 1450, 125),

    # P5
    map_elements.add_background_obj(screen, "Tree", 30, 65, 160, 250),
    map_elements.add_background_obj(screen, "Bush1", 150, 225),
    map_elements.add_background_obj(screen, "Grass", 400, 225),
    map_elements.add_background_obj(screen, "Mushroom", 350, 225),

    # P6
    map_elements.add_background_obj(screen, "Bush2", 750, 325),

    # P7
    map_elements.add_background_obj(screen, "Bush1", 1150, 425),
    map_elements.add_background_obj(screen, "Mushroom", 1200, 425),
    map_elements.add_background_obj(screen, "Tree", 1300, 310, 128, 200),

    # P8
    map_elements.add_background_obj(screen, "Grass", 125, 425),

    # P9
    map_elements.add_background_obj(screen, "Grass", 800, 525),

    # P10
    map_elements.add_background_obj(screen, "Tree", 450, 465, 160, 250),
    map_elements.add_background_obj(screen, "Log", 550, 625),

    # P11
    map_elements.add_background_obj(screen, "Tree", 1450, 465, 160, 250),
    map_elements.add_background_obj(screen, "Bush2", 1400, 625),
    map_elements.add_background_obj(screen, "Grass", 1500, 625),

    # P12
    map_elements.add_background_obj(screen, "Flower", 75, 775),
    map_elements.add_background_obj(screen, "Tree", 150, 616, 160, 250),
    map_elements.add_background_obj(screen, "Bush1", 225, 775),
    map_elements.add_background_obj(screen, "Bush2", 800, 775),
    map_elements.add_background_obj(screen, "Bush1", 850, 775),
    map_elements.add_background_obj(screen, "Mushroom", 1000, 775),
    map_elements.add_background_obj(screen, "Log", 1300, 775),
    map_elements.add_background_obj(screen, "Grass", 1350, 775),

    heals = [
        {"prefix": "Heal", "x": 1450,  "y": 620,  "w": 80, "h": 80, "picked": False},  # przy P1
    ]

    obstacles = [
    map_elements.add_platform(screen, 450, 100, platform_width=3),    # P1
    map_elements.add_platform(screen, 800, 200, platform_width=3),    # P2
    map_elements.add_platform(screen, 1150, 200, platform_width=2),  # P3
    map_elements.add_platform(screen, 1400, 200, platform_width=3),    # P4
    map_elements.add_platform(screen, 50, 300, platform_width=6),    # P5
    map_elements.add_platform(screen, 700, 400, platform_width=3),  # P6
    map_elements.add_platform(screen, 1100, 500, platform_width=4),    # P7
    map_elements.add_platform(screen, 0, 500, platform_width=3),  # P8
    map_elements.add_platform(screen, 725, 600, platform_width=3),  # P9
    map_elements.add_platform(screen, 400, 700, platform_width=3),    # P10
    map_elements.add_platform(screen, 1300, 700, platform_width=4),    # P11
    map_elements.add_platform(screen, 0, 850, platform_width=20),   # P12
    ]
       
    return obstacles, heals


def level_2_enemies():
    return [
       # enemy.Cucumber(1200, 90),    # P3
       # enemy.Cucumber(300, 190),     # P5
       # enemy.Banana(700, 290),     # P5
       # enemy.Banana(500, 590),     # P10
       # enemy.Banana(1550, 590),    # P11
       # enemy.Cucumber(900, 740),    # P12
    ]



def level_3(screen):    # LEVEL 3!!!
    # P1
    map_elements.add_background_obj(screen, "Tree", 100, 12, 128, 200),
    map_elements.add_background_obj(screen, "Grass", 150, 125),

    # P2
    map_elements.add_background_obj(screen, "Mushroom", 425, 125),
    map_elements.add_background_obj(screen, "Bush2", 480, 125),

    # P3
    map_elements.add_background_obj(screen, "Flower", 1000, 75),

    # P4
    map_elements.add_background_obj(screen, "Tree", 1400, 35, 128, 200),
    map_elements.add_background_obj(screen, "Grass", 1450, 150),

    # P5
    map_elements.add_background_obj(screen, "Log", 1115, 325),
    map_elements.add_background_obj(screen, "Bush2", 1175, 325),

    # P6
    map_elements.add_background_obj(screen, "Grass", 30, 350),

    # P7
    map_elements.add_background_obj(screen, "Tree", 700, 315, 160, 250),
    map_elements.add_background_obj(screen, "Tree", 500, 360, 128, 200),
    map_elements.add_background_obj(screen, "Bush1", 800, 475),

    # P8
    map_elements.add_background_obj(screen, "Tree", 1450, 365, 160, 250),

    # P9
    map_elements.add_background_obj(screen, "Bush2", 950, 625),
    map_elements.add_background_obj(screen, "Bush1", 1000, 625),

    # P10
    map_elements.add_background_obj(screen, "Tree", 600, 615, 160, 250),
    map_elements.add_background_obj(screen, "Log", 80, 775),
    map_elements.add_background_obj(screen, "Grass", 130, 775),
    map_elements.add_background_obj(screen, "Grass", 1400, 775),
    map_elements.add_background_obj(screen, "Mushroom", 1450, 775),
    map_elements.add_background_obj(screen, "Sign_Direction_Right", 1325, 775),

    # P11
    map_elements.add_background_obj(screen, "Bush2", 200, 625),

    heals = [
        {"prefix": "Heal", "x": 600,  "y": 470,  "w": 80, "h": 80, "picked": False},  # przy P1
    ]

    obstacles = [
    map_elements.add_platform(screen, 0, 200, platform_width=4),    # P1
    map_elements.add_platform(screen, 400, 200, platform_width=3),    # P2
    map_elements.add_platform(screen, 800, 150, platform_width=4),  # P3
    map_elements.add_platform(screen, 1300, 225, platform_width=4),    # P4
    map_elements.add_platform(screen, 1050, 400, platform_width=5),    # P5
    map_elements.add_platform(screen, 0, 425, platform_width=2),  # P6
    map_elements.add_platform(screen, 350, 550, platform_width=7),    # P7
    map_elements.add_platform(screen, 1400, 600, platform_width=3),  # P8
    map_elements.add_platform(screen, 850, 700, platform_width=6),  # P9
    map_elements.add_platform(screen, 0, 850, platform_width=20),   # P10
    map_elements.add_platform(screen, 100, 700, platform_width=4),   # P11
    ]
       
    return obstacles, heals


def level_3_enemies():
    return [
      #  enemy.Cucumber(400, 90),    # P2
      #  enemy.Banana(1100, 290),     # P5
      #  enemy.Banana(350, 440),     # P7
      #  enemy.Cucumber(700, 440),     # P7
      #  enemy.Banana(950, 590),     # P9
      #  enemy.Cucumber(600, 740),    # P10
    ]



def level_4(screen):    # LEVEL 4!!!
    # P1
    map_elements.add_background_obj(screen, "Sign_Direction", 50, 75),
    map_elements.add_background_obj(screen, "Flower", 100, 75),

    # P2
    map_elements.add_background_obj(screen, "Grass", 450, 125),
    
    # P3
    map_elements.add_background_obj(screen, "Tree", 700, 30, 128, 200),

    # P4
    map_elements.add_background_obj(screen, "Tree", 1050, 115, 160, 250),
    map_elements.add_background_obj(screen, "Bush2", 1025, 275),

    # P5
    map_elements.add_background_obj(screen, "Grass", 650, 425),
    map_elements.add_background_obj(screen, "Mushroom", 700, 425),

    # P6
    map_elements.add_background_obj(screen, "Tree", 1400, 290, 160, 250),
    map_elements.add_background_obj(screen, "Bush1", 1475, 450),

    # P7
    map_elements.add_background_obj(screen, "Sign_Skull", 250, 625),
    map_elements.add_background_obj(screen, "Tree", 300, 520, 128, 200),
    map_elements.add_background_obj(screen, "Bush2", 500, 625),

    # P8
    map_elements.add_background_obj(screen, "Log", 1000, 625),
    map_elements.add_background_obj(screen, "Grass", 1050, 625),

    # P9
    map_elements.add_background_obj(screen, "Bush2", 125, 775),
    map_elements.add_background_obj(screen, "Bush1", 175, 775),
    map_elements.add_background_obj(screen, "Bush1", 175, 775),
    map_elements.add_background_obj(screen, "Grass", 950, 775),
    map_elements.add_background_obj(screen, "Flower", 1015, 775),
    map_elements.add_background_obj(screen, "Tree", 1450, 615, 160, 250),
    map_elements.add_background_obj(screen, "Bush2", 1400, 775),

    # P10
    map_elements.add_background_obj(screen, "Log", 1300, 50),
    map_elements.add_background_obj(screen, "Grass", 1415, 50),

    # P11
    map_elements.add_background_obj(screen, "Bush1", 100, 325),
    map_elements.add_background_obj(screen, "Tree", 275, 215, 128, 200),
    map_elements.add_background_obj(screen, "Grass", 250, 325),

    heals = [
        {"prefix": "Heal", "x": 200,  "y": 320,  "w": 80, "h": 80, "picked": False},  # przy P1
    ]

    obstacles = [
    map_elements.add_platform(screen, 0, 150, platform_width=4),    # P1
    map_elements.add_platform(screen, 400, 200, platform_width=2),    # P2
    map_elements.add_platform(screen, 650, 225, platform_width=2),  # P3
    map_elements.add_platform(screen, 1000, 350, platform_width=4),    # P4
    map_elements.add_platform(screen, 625, 500, platform_width=4),    # P5
    map_elements.add_platform(screen, 1400, 525, platform_width=3),  # P6
    map_elements.add_platform(screen, 200, 700, platform_width=6),  # P7
    map_elements.add_platform(screen, 900, 700, platform_width=6),    # P8
    map_elements.add_platform(screen, 0, 850, platform_width=20),   # P9
    map_elements.add_platform(screen, 1200, 125, platform_width=5),   # P10
    map_elements.add_platform(screen, 0, 400, platform_width=6),   # P11
    ]
       
    return obstacles, heals


def level_4_enemies():
    return [
      #  enemy.Banana(100, 40),    # P1
      #  enemy.Cucumber(400, 90),     # P2
      #  enemy.Banana(1050, 240),    # P4
      #  enemy.Banana(1500, 415),     # P6
      #  enemy.Cucumber(200, 590),     # P7
      #  enemy.Banana(600, 590),     # P7
      #  enemy.Cucumber(1300, 590),     # P8
      #  enemy.Banana(900, 590),     # P8
      #  enemy.Cucumber(800, 740),    # P9
      #  enemy.Cucumber(15, 290),    # P11
    ]


def level_5(screen):    # LEVEL 5 WIN!!!
    map_elements.add_background_obj(screen, "YouWin", 475, 125, 650, 650),
    
    obstacles = [
    map_elements.add_platform(screen, 0, 850, platform_width=20)
    ]
       
    return obstacles

def level_5_enemies():
    return [
    ]

