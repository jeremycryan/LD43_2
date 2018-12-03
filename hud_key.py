##!/usr/bin/env python

from level import fp
from constants import *

class HudKey(object):

    def __init__(self, key):

        self.key = key



        path_dict = {UP: "up.png",
            DOWN: "down.png",
            LEFT: "left.png",
            RIGHT: "right.png",
            JUMP: "c.png",
            DASH: "z.png",
            PUSH: "x.png"}
        self.surf = pygame.image.load(fp(path_dict[key]))
        surf_aspect = self.surf.get_height()*1.0/self.surf.get_width()
        self.surf = pygame.transform.scale(self.surf, (HUD_KEY_WIDTH, HUD_KEY_HEIGHT))

        self.y = HUD_KEY_Y
        if key == UP:
            self.y -= UP_OFFSET
        self.start_y = self.y
        self.x = -100

        self.target_x, self.target_y = self.x, self.y

        self.enabled = True
        self.hover = False

        self.width = HUD_KEY_WIDTH
        self.height = HUD_KEY_HEIGHT
        self.scale = 1.0
        self.target_scale = 1.0

    def draw(self, surf):

        if self.hover:
            color = WHITE
        else:
            color = GRAY

        scale_diff = self.scale - 1
        scale_diff_half = scale_diff/2
        scale_offset_y = scale_diff_half * HUD_KEY_HEIGHT
        scale_offset_x = scale_diff_half * HUD_KEY_WIDTH
        # pygame.draw.rect(surf, color,
        #     (self.x - scale_offset_x,
        #     self.y - scale_offset_y,
        #     self.width,
        #     self.height))
        surf_blit = pygame.transform.scale(self.surf,
            (int(self.width),
            int(self.height)))
        surf.blit(surf_blit, (self.x - scale_offset_x,
            self.y-scale_offset_y))



    def update(self, dt):

        rate = 8.0

        xdif = self.target_x - self.x
        self.x += (xdif * rate)*dt

        ydif = self.target_y - self.y
        self.y += (ydif * rate)*dt

        self.update_scale(dt)

    def update_scale(self, dt):
        scale_rate = 10.0
        ds = self.target_scale - self.scale
        self.scale += scale_rate * ds * dt

        self.width = HUD_KEY_WIDTH * self.scale
        self.height = HUD_KEY_HEIGHT * self.scale


    def mouse_over(self, mpos):
        mx, my = mpos
        if mx >= self.x and mx <= self.x + HUD_KEY_WIDTH:
            if my >= self.y and my <= self.y + HUD_KEY_HEIGHT:
                self.hover = True
                self.target_scale = 1.4
                return True
        self.target_scale = 1.0
        self.hover = False
        return False





class HudKeyArray(object):

    def __init__(self):

        reset_font = pygame.font.Font(fp("Myriad.otf"), 18)
        
        self.reset_font_render = reset_font.render("Press R to reset level. Press H for a hint.", 1, (180, 180, 180))

        self.keys = [UP, DOWN, LEFT, RIGHT, JUMP, PUSH, DASH]
        self.hud_keys = []
        for item in self.keys:
            self.hud_keys.append(HudKey(item))
        self.full_list = self.hud_keys

        self.set_xs()
        self.set_ys()

        for item in self.hud_keys:
            item.x = item.target_x
            item.y = item.target_y

        self.hud_surfs = [item.surf for item in self.hud_keys]
        self.hud_surf_poses = [(item.x, item.y) for item in self.hud_keys]

    def set_xs(self):

        priorities = [HUD_KEY_ORDER[key] for key in self.keys]
        priorities_un = list(set(priorities))

        for key in self.keys:
            priority = HUD_KEY_ORDER[key]
            x_index = priorities_un.index(priority)

            xcum = 0
            for item in self.hud_keys:
                if item.key == key:
                    item.target_x = priority * (HUD_KEY_X_SPACING + HUD_KEY_WIDTH) + HUD_KEY_X

    def set_ys(self):

        for item in self.hud_keys:
            item.target_y = item.start_y

    def draw(self, surf):

        hud_r_rect = pygame.Surface(HUD_R_RECT[2:])
        hud_r_rect.fill((0, 0, 0))
        #hud_r_rect = hud_r_rect.convert_alpha()
        hud_r_rect.set_alpha(100)
        hud_l_rect = pygame.Surface(HUD_L_RECT[2:])
        hud_l_rect.fill((0, 0, 0))
        #hud_l_rect = hud_l_rect.convert_alpha()
        hud_l_rect.set_alpha(100)

        surf.blit(hud_r_rect, HUD_R_RECT[:2])
        surf.blit(hud_l_rect, HUD_L_RECT[:2])

        for i, item in enumerate(self.hud_surfs):
            a = pygame.Surface((item.get_width(),
                item.get_height()))
            a.fill((0, 0, 0))
            a.blit(item, (0, 0))
            a.set_alpha(120)
            surf.blit(a, (self.hud_surf_poses[i]))

        for key in self.hud_keys:
            key.draw(surf)

        surf.blit(self.reset_font_render,
            (38, WINDOW_HEIGHT - 32))

    def update(self, dt):
        self.set_xs()
        self.set_ys()
        for key in self.hud_keys:
            key.update(dt)

    def select_key(self, key):

        for item in self.hud_keys:
            if item.key == key:
                self.hud_keys.remove(item)

    def return_key(self, key):

        self.hud_keys.append(key)
