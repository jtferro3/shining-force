import os
import pygame as pg
from settings import *
import pytmx

class Map():
    def __init__(self, game, filename):
        self.data = []
        with open(filename +'.txt', 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE
        
        self.image = pg.transform.scale(game.load_image(os.path.join(filename + '.png'), False), (self.width, self.height))
        self.rect = pg.Rect(0, 0, self.width, self.height)

class TiledMap():
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        #self.width = tm.width * tm.tilewidth
        #self.height = tm.height * tm.tileheight
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        
    def render(self, surface):
        #ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmxdata.get_tile_image_by_gid(gid)
                    #tile = pg.transform.scale(tile, (TILESIZE, TILESIZE))
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
        return surface
    
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.image = self.render(temp_surface)
        #return temp_surface
        self.rect = self.image.get_rect()
        return self.image

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
    
    def update(self, target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)
