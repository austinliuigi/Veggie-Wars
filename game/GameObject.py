"""GameObject class

The GameObject class contains attributes that are common to *all* game objects
"""
import pygame
from Spritesheet import SpriteSheet
from typing import List, Set, Dict, Tuple
from constants import *

# TODO: clean up the animation logic
class GameObject(pygame.sprite.Sprite):
    def __init__(self, shape: Tuple[int, int], pos: Tuple[int, int], vel: Tuple[int, int], team_num: int, img: str, animation_steps=[32], frame_size=(32, 32)) -> None:
        super().__init__() # initialize sprite class

        # Attribute Initialization
        self.pos_x = pos[0]                 # Initialize x position
        self.pos_y = pos[1]                 # Initialize y position
        self.vel_x = vel[0]                 # Initialize x velocity
        self.vel_y = vel[1]                 # Initialize y velocity
        self.team_num = team_num            # Initialize team number

        # Pygame sprite initialization
        # self.sprite_sheet = SpriteSheet(img)
        img = pygame.image.load(img).convert_alpha()
        self.animation_steps = animation_steps
        self.surf = pygame.Surface(shape)
        self.rect = self.surf.get_rect()
        self.rect.center = pos
        self.animation_list = SpriteSheet(img).get_animation_list(self.animation_steps, shape)

        # use in draw functions
        self.frame_col = 0 # frame
        self.frame_row = 0 # action
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 170

    @property
    def pos(self):
        return self.pos_x, self.pos_y

    @pos.setter
    def pos(self, pos: Tuple[int, int]):
        self.pos_x, self.pos_y = pos

    def draw(self, screen, action=None):
        if action != None:
            self.frame_row = action

            # Update frame
            self.current_time = pygame.time.get_ticks()
            if self.current_time - self.last_update >= self.animation_cooldown:
                self.frame_col += 1
                self.last_update = self.current_time
                if self.frame_col >= len(self.animation_list[self.frame_row]):
                    self.frame_col = 0

        # Draw frame on screen
        screen.blit(self.animation_list[self.frame_row][self.frame_col], self.rect)


    def update(self, screen, action=None):
        self.rect.center = (self.pos_x, self.pos_y)
        self.draw(screen, action)