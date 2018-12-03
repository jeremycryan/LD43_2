##!/usr/bin/env python

import pygame
from constants import *
from sprite_tools import *
from level import fp

class Block(object):

    def __init__(self, pos):
        self.pos = pos
        self.mrd = LEFT

        self.pushable_sheet = SpriteSheet(fp("block.png"), (1, 1), (1))
        self.sink_sheet = SpriteSheet(fp("block_sink.png"), (4, 1), 4)
        self.sink_sheet.repeat = False
        self.sunk_sheet = SpriteSheet(fp("block_sunken.png"), (1, 1), 1)
        self.sprite = Sprite(12)
        self.sprite.add_animation({"idle": self.pushable_sheet,
            "sink": self.sink_sheet,
            "sunk": self.sunk_sheet})
        self.sprite.start_animation("idle")
        self.sprite.scale = TILE_WIDTH/48.0

        self.fell = 0

        self.inset_offset = 0

    def fall(self):
        self.fell = 1
        self.inset_offset = TILE_WIDTH/2
        self.sprite.start_animation("sink")

    def draw(self, surf):

        # self.sprite.x_pos = self.pos[0] * TILE_WIDTH
        # self.sprite.y_pos = self.pos[1] * TILE_WIDTH - TILE_WIDTH
        self.sprite.draw(surf)
        # pos = self.pos
        # pygame.draw.rect(surf, (130, 100, 70),
        #     (pos[0] * TILE_WIDTH+TILE_WIDTH/8,
        #     pos[1] * TILE_WIDTH+TILE_WIDTH/8,
        #     TILE_WIDTH*3/4, TILE_WIDTH*3/4))

    def update(self, dt):

        self.sprite.update(dt)

        offset = 0
        dx = self.pos[0] * TILE_WIDTH - self.sprite.x_pos
        if dx < 5:
            offset = self.inset_offset
        dy = self.pos[1] * TILE_WIDTH - self.sprite.y_pos - TILE_WIDTH + offset

        if dx+dy> TILE_WIDTH * 3 or abs(dx + dy) < 2:
            self.sprite.x_pos = self.pos[0] * TILE_WIDTH
            self.sprite.y_pos = self.pos[1] * TILE_WIDTH - TILE_WIDTH + offset
            return

        rate = 14
        self.sprite.x_pos += dx*rate*dt
        self.sprite.y_pos += dy*rate*dt


    def move_target(self, direction, force_1 = False):
        dist = 1

        if direction == UP:
            target = self.pos[0], self.pos[1] - dist
        elif direction == DOWN:
            target = self.pos[0], self.pos[1] + dist
        elif direction == LEFT:
            target = self.pos[0] - dist, self.pos[1]
        elif direction == RIGHT:
            target = self.pos[0] + dist, self.pos[1]
        return target

    def move(self, direction, force_1 = False):

        dist = 1

        self.mrd = direction

        if direction == UP:
            self.pos = self.pos[0], self.pos[1] - dist
        elif direction == DOWN:
            self.pos = self.pos[0], self.pos[1] + dist
        elif direction == LEFT:
            self.pos = self.pos[0] - dist, self.pos[1]
        elif direction == RIGHT:
            self.pos = self.pos[0] + dist, self.pos[1]
