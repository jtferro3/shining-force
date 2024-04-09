#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 12:47:35 2024

@author: jtferro3
"""

#! /usr/bin/env python

import os, pygame

#walls = [] # List to hold the walls

# Class for the orange dude
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(192, 448, 64, 64)
        
        # create the player image
        self.images = [pygame.transform.scale(load_image(os.path.join('assets', 'max', 'max_' + str(x) + '.png'), True), (64, 64)) for x in range(0,8)]
        self.facing = 0
        self.vel = 5
        self.walkcount = 0
        self.bkgd_rect = bkgd.get_rect()
    
    def move(self):
        
        # Move the player if an arrow key is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing = 1
            self.move_single_axis(-self.vel, 0)
        elif key[pygame.K_RIGHT]:
            self.facing = 2
            self.move_single_axis(self.vel, 0)
        elif key[pygame.K_UP]:
            self.facing = 3
            self.move_single_axis(0, -self.vel)
        elif key[pygame.K_DOWN]:
            self.facing = 0
            self.move_single_axis(0, self.vel)
        self.walkcount += 1
        screen.blit(bkgd, self.bkgd_rect)
        screen.blit(self.images[self.walkcount//15 + self.facing * 2], self.rect)
    
    def move_single_axis(self, dx, dy):
        
        # Move the rect
        #self.rect.x += dx
        #self.rect.y += dy
        
        self.bkgd_rect.x -= dx
        self.bkgd_rect.y -= dy
        if self.rect.x <= self.bkgd_rect.left:
             self.rect.x = self.bkgd_rect.left
        if self.rect.x >= self.bkgd_rect.right:
             self.rect.x = self.bkgd_rect.right
        if self.rect.y <= self.bkgd_rect.top:
             self.rect.y = self.bkgd_rect.top
        if self.rect.y >= self.bkgd_rect.bottom:
             self.rect.y = self.bkgd_rect.bottom
        '''
        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
        '''
# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 64, 64)

def load_image(file, alpha):
    """loads an image, prepares it for play"""
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit(f'Could not load image "{file}" {pygame.get_error()}')
    return surface.convert_alpha() if alpha else surface.convert()

def load_sound(file):
    """because pygame can be compiled without mixer."""
    if not pygame.mixer:
        return None
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print(f"Warning, unable to load, {file}")
    return None

def main():
    # setup
    screen_width = 796
    screen_height = 728
    
    # Initialise pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    pygame.mixer.init()
    
    # Set up the display
    pygame.display.set_caption("Shining Force - Chapter 1")
    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    
    # Set up game icon
    pygame_icon = load_image(os.path.join('assets', 'max', 'max_0.png'), True)
    pygame.display.set_icon(pygame_icon)

    # create the background
    global bkgd
    bkgd = pygame.transform.scale(load_image(os.path.join('assets', 'map', 'sf1_level_1.png'), False), (2579, 2361))
    
    # Set up the sound
    if pygame.mixer:
        #boom_sound = load_sound("boom.wav")
        pygame.mixer.music.load(os.path.join('assets', 'audio', 'sf1_town_1.ogg'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)

    global walls
    walls = [] # List to hold the walls
    player = Player() # Create the player
    
    # creating the event
    ENDGAME = pygame.event.Event(pygame.USEREVENT, attr1='ENDGAME')
    
    # Holds the level layout in a list of strings.
    level = [
    "WWWWWWWWWWW",
    "W   w    W",
    "W  WEW    W",
    "W  W W    W",
    "WWWW W    W",
    "W     W   W",
    "W     W   W",
    "WWWW  W   W",
    "W   WWW   W",
    "WWWWWWWWWWW",
    ]
    
    # Parse the level string above. W = wall, E = exit
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            if col == "E":
                end_rect = pygame.Rect(x, y, 64, 64)
            x += 64
        y += 64
        x = 0
    
    running = True
    FPS = 30
    
    # Game loop
    while running:
        
        clock.tick(FPS)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if e == ENDGAME:
                running = False
                print('You Win !!!')
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        
        if player.walkcount + 1 >= 30:
            player.walkcount = 0
        
        # Move the player if an arrow key is pressed
        player.move()
        
        # Just added this to make it slightly fun ;)
        if player.rect.colliderect(end_rect):
            pygame.event.post(ENDGAME)
        
        
        # Draw the scene
        #screen.blit(bkgd, (-32,-32))
        #pygame.draw.rect(screen, (255, 0, 0), end_rect)
        #screen.blit(player.images[player.walkcount//15 + player.facing * 2], player.rect)
        pygame.display.update()
    
    if pygame.mixer:
        pygame.mixer.music.fadeout(2000)
    pygame.time.wait(1000)
    pygame.quit()

# call the "main" function if running this script
if __name__ == "__main__":
    main()
