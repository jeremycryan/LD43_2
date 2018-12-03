##!/usr/bin/env python
from constants import *
from level import fp
from sprite_tools import *
import pygame

class Door(object):

    def __init__(self, pos, shrine):

        self.shrine = shrine
        self.pos = pos

        self.width = TILE_WIDTH
        self.height = TILE_WIDTH

        self.active_sheet = SpriteSheet(fp("gate.png"), (2, 3), 6)
        self.inactive_sheet = SpriteSheet(fp("gate_inactive.png"), (2, 3), 6)
        self.sprite = Sprite(8)
        self.sprite.scale = TILE_WIDTH/48.0
        self.sprite.add_animation({"active": self.active_sheet,
            "inactive": self.inactive_sheet})
        self.sprite.start_animation("active")

        self.active_trigger = 0

    def draw(self, surf):
        pos = self.pos

        color = (80, 80, 160)
        if self.is_passable():
            color = (120, 160, 180)

        # pygame.draw.rect(surf, color,
        #     (pos[0] * TILE_WIDTH,
        #     pos[1] * TILE_WIDTH,
        #     self.width,
        #     self.height))

        self.sprite.x_pos = self.pos[0] * TILE_WIDTH - TILE_WIDTH
        self.sprite.y_pos = self.pos[1] * TILE_WIDTH - TILE_WIDTH
        self.sprite.draw(surf)

    def is_passable(self):

        ret = self.shrine.is_activated()
        if self.active_trigger == 0 and ret:
            self.active_trigger = 1
            self.sprite.start_animation("inactive")

        return ret

    def update(self, dt):
        self.sprite.update(dt)
