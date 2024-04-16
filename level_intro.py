import os
import pygame as pg
from settings import *
from sprites import *
import time

class Level(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # self.groups = game.all_sprites
        # pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.text = ['In ages long forgotten ...',
                     ' ',
                     '... Light fought Darkness',
                     'for control of the world.',
                     'Dark Dragon led the evil',
                     'hordes of Darkness.',
                     'The Ancients fought back with',
                     'the Powers of Light.',
                     'Dark Dragon was defeated and',
                     'cast into another dimension.',
                     'The Lord of Darkness vowed to',
                     'return in 1,000 years.',
                     'Time passed and Dark Dragon',
                     'was forgotten by all.',
                     'Ten Centuries of peace ruled',
                     'the land of Rune.',
                     'Until the kingdom of Runefaust',
                     'brought war and fear to Rune.',
                     'Hordes of evil creatures',
                     'ravaged every land.',
                     'Here and there, strongholds',
                     'of Good still held out ...',
                     '... awaiting a Hero who could',
                     'wield the Powers of Light!']
        self.x = x
        self.y = y
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.count = 0
    
    def load_images(self):
        self.anim = [
                    [pg.transform.scale_by(self.game.level_intro.get_image(127, 536, 25, 33), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(154, 536, 25, 33), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(183, 536, 25, 33), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(213, 536, 34, 33), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(157, 572, 50, 34), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(145, 610, 77, 34), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(138, 653, 96, 34), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(136, 695, 100, 34), 2)],
                    [pg.transform.scale_by(self.game.level_intro.get_image(10, 36, 14, 14), 1),
                     pg.transform.scale_by(self.game.level_intro.get_image(26, 34, 16, 16), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(46, 32, 20, 20), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(68, 30, 22, 24), 4),
                     pg.transform.scale_by(self.game.level_intro.get_image(92, 28, 24, 26), 5),
                     pg.transform.scale_by(self.game.level_intro.get_image(118, 28, 28, 26), 6),
                     pg.transform.scale_by(self.game.level_intro.get_image(146, 26, 30, 30), 7),
                     pg.transform.scale_by(self.game.level_intro.get_image(118, 28, 28, 26), 6),
                     pg.transform.scale_by(self.game.level_intro.get_image(92, 28, 24, 26), 5),
                     pg.transform.scale_by(self.game.level_intro.get_image(68, 30, 22, 24), 4),
                     pg.transform.scale_by(self.game.level_intro.get_image(46, 32, 20, 20), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(26, 34, 16, 16), 2)],
                    [pg.transform.scale_by(self.game.level_intro.get_image(10, 36, 14, 14), 1),
                     pg.transform.scale_by(self.game.level_intro.get_image(26, 34, 16, 16), 2),
                     pg.transform.scale_by(self.game.level_intro.get_image(46, 32, 20, 20), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(68, 30, 22, 24), 4),
                     pg.transform.scale_by(self.game.level_intro.get_image(92, 28, 24, 26), 5),
                     pg.transform.scale_by(self.game.level_intro.get_image(118, 28, 28, 26), 6),
                     pg.transform.scale_by(self.game.level_intro.get_image(146, 26, 30, 30), 7),
                     pg.transform.scale_by(self.game.level_intro.get_image(118, 28, 28, 26), 8),
                     pg.transform.scale_by(self.game.level_intro.get_image(184, 4, 82, 82), 9),
                     pg.transform.scale_by(self.game.level_intro.get_image(276, 0, 118, 122), 10),
                     pg.transform.scale_by(self.game.level_intro.get_image(100, 106, 168, 172), 10),
                     pg.transform.scale_by(self.game.level_intro.get_image(60, 285, 256, 224), 10)],
                    [pg.transform.scale_by(self.game.level_intro.get_image(398, 299, 240, 100), 3)],
                    [pg.transform.scale_by(self.game.level_intro.get_image(389, 174, 75, 97), 2.5),
                     pg.transform.scale_by(self.game.level_intro.get_image(484, 178, 75, 97), 2.5),
                     pg.transform.scale_by(self.game.level_intro.get_image(569, 177, 75, 97), 2.5)],
                    [pg.transform.scale_by(self.game.level_intro.get_image(388, 412, 258, 111), 3)],
                    [pg.transform.scale_by(self.game.level_intro.get_image(661, 29, 258, 111), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(661, 145, 258, 111), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(661, 259, 258, 111), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(661, 376, 258, 111), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(661, 497, 258, 111), 3),
                     pg.transform.scale_by(self.game.level_intro.get_image(660, 618, 258, 111), 3)],
                    [pg.transform.scale_by(self.game.level_intro.get_image(400, 526, 238, 190), 2.5)]
                    ]
    
    def update(self, scene):
        self.animate(scene)
    
    def animate(self, scene):
        number_of_frames = len(self.anim[scene])
        now = pg.time.get_ticks()
        if now - self.last_update > 125:
            if self.current_frame > number_of_frames:
                self.current_frame = 0
            
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % number_of_frames
            
            self.image = self.anim[scene][self.current_frame]
            self.rect = self.image.get_rect()
            
            self.rect.x = self.x - self.rect.width / 2
            self.rect.y = self.y - self.rect.height / 3
    
    def draw(self):
        self.game.screen.blit(self.image, self.rect)
        
    def logo(self, scene):
        START = WIDTH + 60
        END = WIDTH // 2 - 120

        # right to left movement
        for x_motion in range(START, END, -5):
            self.game.clock.tick(FPS)
            self.game.screen.fill(BLACK)
            rect_x = 0
            rect_y = HEIGHT // 3
            
            for letter in range(4):
                # Bouncing across screen
                if x_motion >= END + 60:
                    self.image = self.anim[scene][letter]
                    self.rect = self.image.get_rect()
                    self.rect.x = x_motion + rect_x
                    self.rect.y = rect_y + self.bounce(x_motion + rect_x // 4)
                    # self.rect.y = rect_y
                # Smashing into each other
                elif x_motion < END + 15:
                    match letter:
                        case 0:
                            self.image = self.anim[scene][7]
                            self.rect = self.image.get_rect()
                            self.rect.x = END
                            self.rect.y = rect_y
                        case _:
                            pass
                elif x_motion < END + 30:
                    match letter:
                        case 0:
                            self.image = self.anim[scene][6]
                            self.rect = self.image.get_rect()
                            self.rect.x = END
                            self.rect.y = rect_y
                        case 1, 2:
                            pass
                        case _:
                            self.image = self.anim[scene][letter]
                            self.rect = self.image.get_rect()
                            self.rect.x = x_motion + rect_x
                            self.rect.y = rect_y
                elif x_motion < END + 45:
                    match letter:
                        case 0:
                            self.image = self.anim[scene][5]
                            self.rect = self.image.get_rect()
                            self.rect.x = END
                            self.rect.y = rect_y
                        case 1:
                            pass
                        case _:
                            self.image = self.anim[scene][letter]
                            self.rect = self.image.get_rect()
                            self.rect.x = x_motion + rect_x
                            self.rect.y = rect_y
                elif x_motion < END + 60:
                    match letter:
                        case 0:
                            self.image = self.anim[scene][0]
                            self.rect = self.image.get_rect()
                            self.rect.x = END
                            self.rect.y = rect_y
                        case _:
                            self.image = self.anim[scene][letter]
                            self.rect = self.image.get_rect()
                            self.rect.x = x_motion + rect_x
                            self.rect.y = rect_y
                self.draw()
                rect_x += self.rect.width
            pg.display.flip()
        time.sleep(5)
    
    def scene(self, index, start, end, is_text):
        for i in range(start, end, 2):
            frame = 0
            while frame < len(self.text[i]):
                self.game.clock.tick(FPS)
                self.game.screen.fill(BLACK)
                self.update(index)
                self.draw()
                if is_text:
                    self.game.draw_text(self.text[i][:frame], 64, WHITE, 25, HEIGHT * 3 / 4)
                frame += 1
                pg.display.flip()
            frame = 0
            while frame < len(self.text[i + 1]) + 75:
                self.game.clock.tick(FPS)
                self.game.screen.fill(BLACK)
                self.update(index)
                self.draw()
                if is_text:
                    self.game.draw_text(self.text[i], 64, WHITE, 25, HEIGHT * 3 / 4)
                    self.game.draw_text(self.text[i + 1][:frame], 64, WHITE, 25, HEIGHT * 13 / 16)
                frame += 1
                pg.display.flip()

    def bounce(self, index: int) -> int:
        y: int
        mod_limit: int = 60
        mod: int = index % mod_limit
        mod_range: int = mod_limit // 3
        mod -= mod_range
        mod = (-1 * abs(mod)) + mod_range
        mod_amp: int = 1
        y = (mod * mod_amp)
        return y

# call the "main" function if running this script
if __name__ == "__main__":
    for i in range(60):
        print(Level.bounce(Level, i))
