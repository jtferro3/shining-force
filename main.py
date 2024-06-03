#!/usr/bin/env python
""" Shining Force

@author: John T. Ferro, III
@Created on Mon Jan 15 2024 12:47:35

Description
-----------
Play the Sega Genesis game Shining Force re-imagined with Python.

Controls
--------
* Left, Right, Up, and Down arrows to move and select.
* Space to interact.

"""
import pygame as pg
import sys
import os
import pytmx
from settings import *
from sprites import *
from characters import *
from tilemap import *
from level_intro import *

class Game:
    def __init__(self):
        pg.init()
        
        # Set up display
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 500)
        self.load_data()
        self.font_name = pg.font.match_font(FONT_NAME)
        
        # Set up game icon
        pg_icon = self.load_image(os.path.join('assets', 'max', 'max_0.png'), True)
        pg.display.set_icon(pg_icon)
        
        self.running = True
    
    def load_data(self):
        self.dir = os.path.dirname(__file__)
        # load spritesheet image
        self.spritesheet = Spritesheet(os.path.join(self.dir, 'assets', 'characters', SPRITESHEET))
    
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        
        self.map = TiledMap(os.path.join('assets', 'map', 'sf1_level_1.tmx'))
        self.map.image = self.map.make_map()
        
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y, pc_max_n)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.facing = 1
                    self.player.vel.x = -PLAYER_SPEED
                elif event.key == pg.K_RIGHT:
                    self.player.facing = 2
                    self.player.vel.x = PLAYER_SPEED
                elif event.key == pg.K_UP:
                    self.player.facing = 3
                    self.player.vel.y = -PLAYER_SPEED
                elif event.key == pg.K_DOWN:
                    self.player.facing = 0
                    self.player.vel.y = PLAYER_SPEED

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
    
    def draw(self):
        # Draw background
        self.screen.blit(self.map.image, self.camera.apply_rect(self.map.rect))
        
        # Draw grid
        self.draw_grid()
        
        # Draw sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        
        pg.display.flip()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def quit(self):
        pg.quit()
        sys.exit()

    def draw_text(self, text, size, color, x, y) :
        font = pg.font.Font(self. font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        # text_rect.midtop = (x, y)
        text_rect.left = x
        text_rect.top = y
        self.screen.blit(text_surface, text_rect)

    def wait_for_keys(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        # self.dir = os.path.dirname(__file__)
        self.level_intro = Spritesheet(os.path.join(self.dir, 'assets', 'map', 'sf1_spritesheet_intro.png'))
        self.level = Level(self, WIDTH // 2, HEIGHT // 3)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                self.running = False
                self.quit()
            if event.type == pg.KEYUP:
                waiting = False

        self.level.logo(0)

        # self.level.scene(1, 0, 6, True)
        # self.level.scene(2, 0, 1, False)
        # self.level.scene(3, 6, 10, True)
        # self.level.scene(4, 10, 12, True)
        # self.level.scene(5, 12, 16, True)
        # self.level.scene(6, 16, 24, True)
        
        self.level.press_start(7)

    def show_gameover_screen(self):
        pass

# call the "main" function if running this script
if __name__ == "__main__":
    # create the game object
    g = Game()
    g.show_start_screen()
    while True:
        g.new()
        g.run()
        g.show_gameover_screen()
