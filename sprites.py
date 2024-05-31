import os
import pygame as pg
from settings import *
from characters import *

class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (TILESIZE, TILESIZE))
        image.set_colorkey(ALPHA)
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, character):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.character = character
        self.facing = 0
        self.vel = vec(0, 0)
        self.current_frame = 0
        self.last_update = 0
        
        self.load_images()
    
    def load_images(self):
        self.anim = [self.game.spritesheet.get_image(*self.character[0]),
                     self.game.spritesheet.get_image(*self.character[1]),
                     self.game.spritesheet.get_image(*self.character[2]),
                     self.game.spritesheet.get_image(*self.character[3]),
                     pg.transform.flip(self.game.spritesheet.get_image(*self.character[4]), True, False),
                     pg.transform.flip(self.game.spritesheet.get_image(*self.character[5]), True, False),
                     self.game.spritesheet.get_image(*self.character[6]),
                     self.game.spritesheet.get_image(*self.character[7]),
                     self.game.spritesheet.get_image(*self.character[8]),
                     self.game.spritesheet.get_image(*self.character[9])]
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.x
            self.vel.x = 0
            
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.y
            self.vel.y = 0

    def update(self):
        self.animate()
        
        self.x += self.vel.x
        self.y += self.vel.y
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.game.dt * (FPS / 0.002):
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % 2 + self.facing * 2
            self.image = self.anim[self.current_frame]
            self.rect = self.image.get_rect()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.rect = pg.Rect(x, y, w, h)
        #self.rect.x = x
        #self.rect.y = y
