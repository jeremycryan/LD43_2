##!/usr/bin/env python

from constants import *
from sprite_tools import *
import pygame
from level import fp

class Shrine(object):

    def __init__(self, pos, num=0):
        self.pos = pos

        self.num = num

        self.width = TILE_WIDTH
        self.height = TILE_WIDTH

        self.captured_key = []

        self.inactive_sheet = SpriteSheet(fp("inactive_altar.png"), (1, 1), 1)
        self.active_sheet = SpriteSheet(fp("active_altar.png"), (8, 1), 8)
        self.sprite = Sprite(8)
        self.sprite.add_animation({"active": self.active_sheet,
            "inactive": self.inactive_sheet})
        self.sprite.start_animation("active")
        self.sprite.scale = TILE_WIDTH*1.0/48

        self.mode = "active"

    def is_activated(self):
        cond = len(self.captured_key) > 0
        if cond:
            self.mode = "inactive"
            self.sprite.start_animation("inactive")
            return True
        elif self.mode == "inactive":
            self.sprite.start_animation("active")
        return False

    def draw(self, surf):
        pos = self.pos
        x = pos[0] * TILE_WIDTH
        y = pos[1] * TILE_WIDTH
        # pygame.draw.rect(surf, (255, 0, 0),
        #     (int(x), int(y)),
        #     (self.width,
        #     self.height))

        self.sprite.x_pos, self.sprite.y_pos = x, y-TILE_WIDTH
        self.sprite.draw(surf)

        if len(self.captured_key):
            key = self.captured_key[0]
            key.x = pos[0] * TILE_WIDTH - HUD_KEY_WIDTH/2.0 + self.width/2
            key.y = pos[1] * TILE_WIDTH - key.height
            key.draw(surf)

    def update(self, dt):
        self.sprite.update(dt)

        for key in self.captured_key:
            key.update_scale(dt)
