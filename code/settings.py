import pygame, sys, os, time
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6

# layers
Z_LAYERS = {
    'bg tiles': 0,
    'main': 1,
    'lava': 2,
}