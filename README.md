# Shadebreaker

A 2D platformer built in Python with Pygame as my A-Level Computer Science NEA (Non-Exam Assessment).

> **Note:** Core mechanics (movement, animation, and tilemap fundamentals) and menu/state management were built by following two YouTube tutorial series, credited below. Physics, enemy logic (including a custom-designed tracking enemy), and overall game design/content were my own work on top of that foundation. See "What I Built" below for the breakdown.

## Concept

The player moves between two parallel worlds, each with different platforms and enemies, to progress through a series of levels. Each level is scored out of three stars based on time taken, enemies defeated, and coins collected, with later levels locked until earlier ones are completed.

## Features

- **World-switching mechanic** — swap between two versions of each level, each with distinct platform layouts and enemies
- **Multi-level progression** with a 3-star scoring system (time, enemies killed, coins collected), level-gating based on completion and a pause state
- **Player abilities** — attack, wall jump, and world switching, all with cooldowns
- **Three enemy types** - a running enemy, gunner and one with flying player-tracking projectiles
- **5-life system** and health potions
- **End-goal item** — a gem must be collected before the level's exit door (animated) will open

## What I Built

The base movement, animation, tilemap, and menu/pause systems followed two YouTube tutorial series (credited below). On top of that foundation, I independently designed and implemented:

- **Physics** — collision handling and movement beyond the tutorial's base implementation to improve the smoothness of the gameplay
- **World-switching logic** - implemented the logic for managing the platforms, timers and which entities are present depending on the world
- **Pause state** - added logic to ensure all in-game timers are not updated to prevent objects and entities from moving
- **A custom tracking enemy** — an enemy with flying projectiles that track the player, which wasn't covered by the tutorial series; I built this by combining ideas from multiple separate tutorials with my own logic to get it working within the existing game structure. This included logic which made the tracking more 'random' to prevent them from clumping at one location near the player.

## Tutorials Followed

This project was built as a learning exercise, drawing on two tutorial series:
- Core platformer mechanics (movement, animation, tilemaps): [2D Platformer Tutorial](https://www.youtube.com/watch?v=WViyCAa6yLI&list=PLmW9lxNs84hkbzk26ERpev1MGd5tlcacg)
- State/menu management (pause state, level select, etc.): [Pygame Menu System Tutorial](https://www.youtube.com/playlist?list=PLVFWKkB2K-TmYDRlFFm-RkhZNNj0waXw5)

## Build

Requires Python and Pygame installed.

```bash
pip install pygame
python main.py
```
