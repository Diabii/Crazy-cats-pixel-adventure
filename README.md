#     Crazy Cats Pixel Adventure 🐱⚔️

A 2D platformer fighting game built with Python and Pygame, featuring two playable cat characters battling enemies across destructible environments.

## Project Overview

Cat Battle Arena is an object-oriented programming project where two players (Zolza and Poki) fight against waves of enemies on dynamic platforms. The game features a sophisticated attack system with both melee and ranged combat, health management, and collectible healing items.

<img width="1123" height="268" alt="obraz" src="https://github.com/user-attachments/assets/7639d5bc-35b6-41b7-953f-7f4b083f0b73" />

## Features

- **Two Playable Characters**: Zolza and Poki
- **Dynamic Combat System**: 
  - Melee attacks (claws) with animation frames
  - Ranged attacks (fireballs) with projectile physics
- **Enemy Variety**: Multiple enemy types (Cucumber, Banana)
- **Platformer Mechanics**: Jump, move, and navigate across multi-level platforms
- **Health System**: HP bars for players and enemies, invincibility frames after taking damage
- **Collectibles**: Healing items to restore health during gameplay
- **Visual Polish**: Animated sprites, health bar graphics, environment decorations

## Project Structure

```
├── scene.py                 # Main game loop and scene management
├── player.py               # Player class with movement, attacks, health
├── enemy.py                # Enemy base class and specific enemy types
├── attack.py               # Attack system (melee + projectile)
├── enemy_attack.py         # Enemy-specific attack logic
├── maps.py                 # Level definitions and layout
├── map_elements.py         # Platform and UI element rendering
├── animation_tools.py      # Animation frame loading and management
└── graphics/               # Game assets
    ├── Attacks/            # Attack animations (claws, fireballs)
    ├── Cats/               # Character sprites (Zolza, Poki)
    ├── Enemies/            # Enemy sprites
    ├── Environment/        # Platform and background elements
    └── Interface/          # UI graphics (health bars, etc.)
```

## Project Highlights

### Graphics Management
- Efficient sprite loading and caching
- Frame-based animation system with configurable timing
- Multi-image health bar visualization
- Directional sprite handling (left/right)
<img width="375" height="275" alt="obraz" src="https://github.com/user-attachments/assets/343aaf7c-483e-4c56-88d6-4444cc0549d0" />
<img width="375" height="265" alt="obraz" src="https://github.com/user-attachments/assets/241ac949-6bb8-48da-9665-a9be76f0cac5" />
<img width="375" height="275" alt="obraz" src="https://github.com/user-attachments/assets/a1e0d98f-1bae-4018-bcce-50dfc3f16977" />

### Physics & Collisions
- Separate visual and hitbox dimensions for better gameplay feel
- Velocity-based movement with acceleration
- Gravity simulation for platformer mechanics

<img width="737" height="435" alt="obraz" src="https://github.com/user-attachments/assets/aaaf2ec9-ecc3-46c1-96af-0a5beaf709bc" />

### Level Design
The game features multi-level platforms designed for strategic combat:
- **Many Platforms** arranged vertically and horizontally
- **Environmental Decorations**: Trees, bushes, mushrooms, signs
- **Strategic Positioning**: Platforms encourage movement and evasion
- **Healing Stations**: Item placement encourages exploration

<img width="927" height="487" alt="obraz" src="https://github.com/user-attachments/assets/e91edb9b-55b1-4bbe-90f1-92862fd972d9" />

### Game Balance

- **Attack Cooldowns**: Prevent spam and require tactical timing
- **Enemy Variety**: Different enemy types with varying behaviors
- **Health Management**: Limited healing items create resource management
- **Platform Layout**: Open areas require positioning awareness

<img width="927" height="487" alt="obraz" src="https://github.com/user-attachments/assets/10083e62-f7f6-4847-b072-fe8bdeaf27d2" />
<img width="927" height="487" alt="obraz" src="https://github.com/user-attachments/assets/0519a6b5-5a88-4581-a559-4d79b4955b6c" />

## Requirements

- Python 3.7+
- Pygame 2.0+

## Installation

1. Clone or download the project
2. Install dependencies:
   ```bash
   pip install pygame
   ```

## Running the Game

```bash
python scene.py
```

##  Authors
- Patryk Pełka
- Zuzanna Rykaczewska
- Emilia Melkowska
- Natalia Pruska
