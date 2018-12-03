##!/usr/bin/env python

import pygame
from constants import *

from sprite_tools import *
from level import fp
from math import sin, pi

class Goal(object):

    def __init__(self, pos):
        self.pos = pos

        self.idle_sheet = SpriteSheet(fp("gem.png"), (8, 2), 16)
        self.collect_sheet = SpriteSheet(fp("gem_collect.png"), (8, 2), 16)
        self.sprite = Sprite(8)
        self.sprite.add_animation({"idle": self.idle_sheet,
                                    "collect": self.collect_sheet})
        self.sprite.scale = TILE_WIDTH/48.0
        self.sprite.start_animation("idle")

        self.scale = 1.0
        self.time = 0

        

    def draw(self, surf):
        pos = self.pos
        x = pos[0] * TILE_WIDTH
        y = pos[1] * TILE_WIDTH
        
        a = pygame.Surface((int(TILE_WIDTH/3*self.scale), int(TILE_WIDTH/5*self.scale)))
        a.fill((0, 0, 0))
        a.set_alpha(50)
        surf.blit(a, (x+TILE_WIDTH/2-a.get_width()/2, y+TILE_WIDTH/2-a.get_height()/2))
                  
#        pygame.draw.rect(surf, (140, 40, 160),
#            (pos[0] * TILE_WIDTH+TILE_WIDTH/8,
#            pos[1] * TILE_WIDTH+TILE_WIDTH/8,
#            TILE_WIDTH*3/4, TILE_WIDTH*3/4))


        self.sprite.x_pos = x
        self.sprite.y_pos = y - TILE_WIDTH
        self.sprite.draw(surf)

    def update(self, dt):
        self.time += dt
        self.scale = 1.0 + 0.2*sin(2.0*pi*(self.time+0.125))
        self.sprite.update(dt)
        
