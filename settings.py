import pygame as pg

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (64, 128, 255)
YELLOW = (255, 255, 0)
ALPHA = (100, 1, 99)

# game settings
WIDTH = 720   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 656  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 30
FPS2 = 30
FONT_NAME = 'ariel'
SPRITESHEET = 'sf1_spritesheet.png'
TITLE = 'Shining Force'
BGCOLOR = DARKGREY

TILESIZE = 24
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE
vec = pg.math.Vector2

# Player Settings
PLAYER_SPEED = TILESIZE
