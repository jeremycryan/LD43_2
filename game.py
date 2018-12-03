##!/usr/bin/env python
import pygame
import time
import sys
from level import Level, fp
from constants import *
from camera_tools import Camera
from player import Player
from goal import Goal
from block import Block
from hud_key import *
from shrine import *
from door import *
import math

class Game():

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen_commit = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Master Key - LD43")
        self.screen = pygame.Surface(MAX_FRAME_SIZE)


        pygame.mixer.pre_init(44100, -16, 1, 512)
        self.mus = pygame.mixer.Sound(fp("LD43.wav"))
        self.mus.play(-1)

        self.box_slide = pygame.mixer.Sound(fp("box_slide.wav"))
        self.box_slide.set_volume(0.12)
        self.box_fall = pygame.mixer.Sound(fp("box_fall.wav"))
        self.box_fall.set_volume(0.35)
        self.prompt_continue = pygame.mixer.Sound(fp("prompt_continue.wav"))
        self.prompt_continue.set_volume(0.3)
        self.collect_gem = pygame.mixer.Sound(fp("collect_gem.wav"))
        self.collect_gem.set_volume(0.5)
        self.altar_place = pygame.mixer.Sound(fp("altar_place.wav"))
        self.altar_place.set_volume(0.4)
        self.reset_noise = pygame.mixer.Sound(fp("reset.wav"))
        self.reset_noise.set_volume(0.15)
        self.dash_sound = pygame.mixer.Sound(fp("dash.wav"))
        self.dash_sound.set_volume(0.05)
        self.key_select = pygame.mixer.Sound(fp("key_select.wav"))
        self.key_select.set_volume(0.15)

        
        self.cam = Camera(self.screen_commit)
        self.cam.set_pan_pid(6, 2, -0.2)

        self.notice_frame = pygame.image.load(fp("notice.png"))


        self.levels = [Level("level_1.txt"),
            Level("level_2.txt"),
            Level("level_3.txt"),
            Level("level_3.5.txt"),
            Level("level_4.txt"),
            Level("level_5.txt"),
            Level("level_6.txt"),
            Level("level_7.txt")]

        self.main()


    def main(self):

#        level_to_msg = {0: "Welcome to Master Key!\nUse the arrow keys to move.",
#            1: "Hold Z while moving to dash.",
#            2: "Hold X to push objects.",
#            3: "Hold C to hop up ledges.",
#            4: "Altars require you to\nsacrifice your controls!\n\nStand in front of the book, and\n drag a key onto it with the mouse.",
#            5: "You're on your own now.\n Good Luck!"}

#        level_to_hint = {0: "Move around with the arrow keys.",
#            1: "Hold Z while moving to dash.\nThis allows you to cross short gaps.",
#            2: "Hold X while moving to push.\nYou can push cubes into holes.",
#            3: "Hold C while moving to jump.\nThis lets you get up short platforms.",
#            4: "Try standing next to the book, and\n drag a key onto it with the mouse.",
#            5: "You can replace the key on an altar\nby dragging a different key onto it.",
#            6: "Don't forget you can sacrifice\nyour movement keys, too!",
#            7: "Don't forget you can sacrifice\nyour movement keys, too!",
#            8: ""}

#        for key in level_to_msg:
#            self.tooltip(level_to_msg[key])
#        for key in level_to_hint:
#            self.tooltip(level_to_hint[key])

        self.level_counter = 0
        while self.level_counter < len(self.levels):
            self.cam.zoom = 1.0
            self.cam.set_target_zoom(1.0)
            self.run_level(self.levels[self.level_counter])
            self.level_counter += 1
        self.tooltip("That's all!\nThanks for playing!")

    def set_starting_hud(self):
        if self.level_counter == 0:
            bad = []
            for key in self.hud_key_array.hud_keys:
                if key.key in [JUMP, DASH, PUSH]:
                    bad.append(key)
            for item in bad:
                self.hud_key_array.hud_keys.remove(item)

        elif self.level_counter == 1:
            bad = []
            for key in self.hud_key_array.hud_keys:
                if key.key in [JUMP, PUSH]:
                    bad.append(key)
            for item in bad:
                self.hud_key_array.hud_keys.remove(item)

        elif self.level_counter == 2:
            bad = []
            for key in self.hud_key_array.hud_keys:
                if key.key in [JUMP]:
                    bad.append(key)
            for item in bad:
                self.hud_key_array.hud_keys.remove(item)


#################################################333333

    def tooltip(self, str):
        self.mus.set_volume(0.4)
        self.press_enable = False
        frame = self.notice_frame.copy().convert_alpha()
        cur_state = self.screen_commit.copy()

        myfont = pygame.font.Font(fp("Myriad.otf"), 30)
        tsplit = str.split("\n")
        l = len(tsplit)
        any_button = pygame.font.Font(fp("Myriad.otf"), 20)
        any_button_text = any_button.render("Press any button to continue.", 1, (0, 0, 0))

        tool_shadow_alpha = 0
        tool_shadow = pygame.Surface(WINDOW_SIZE)
        tool_shadow.fill((0, 0, 0))
        tool_shadow.set_alpha(tool_shadow_alpha)
        tool_shadow_rate = 300
        tool_shadow_max = 150
        tool_shadow_multiplier = 1.0

        for i2, i in enumerate(tsplit):
            a = myfont.render(i, 1, (0, 0, 0))
            frame.blit(a, (frame.get_width()/2 - a.get_width()/2, frame.get_height()/2 - a.get_height()/2 - a.get_height()*0.6*l + a.get_height()*1.2*i2))
        frame.blit(any_button_text, (frame.get_width()/2 - any_button_text.get_width()/2, 240))

        then = time.time()
        pause_time = time.time()
        paused = True
        to_break = False

        while not to_break:
            now = time.time()
            dt = now - then
            then = now

            tsm = tool_shadow_multiplier

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if time.time() - pause_time > 0.5:
                        if paused:
                            self.prompt_continue.play()
                            self.mus.set_volume(1.0)
                        paused = False

            tool_shadow_alpha = min(tool_shadow_max, int((time.time()-pause_time)*tool_shadow_rate))
            tool_shadow.set_alpha(tool_shadow_alpha*tool_shadow_multiplier)

            self.screen_commit.fill((0, 0, 0))
            self.screen_commit.blit(cur_state, (0, 0))
            self.screen_commit.blit(tool_shadow, (0, 0))
            x = WINDOW_WIDTH/2 - self.notice_frame.get_width()/2
            y = WINDOW_HEIGHT/2 - self.notice_frame.get_height()/2
            self.screen_commit.blit(frame,(x, int(y*(3 * tsm-2) - 200*math.sin(2*math.pi*tsm))))
            pygame.display.flip()

            if paused == False:
                tool_shadow_multiplier -= dt*3
                if tool_shadow_multiplier < 0:
                    to_break = True



        pass


    def run_level(self, level_obj):



        self.press_en = True
        
        self.mrd = DOWN


        self.hud_key_array = HudKeyArray()


        self.clicked = 0
        self.selected_key = []
        self.hovered_shrine = []
        self.last_hover = []

        self.cur_level = level_obj

        self.then = time.time()


        self.player_pos = level_obj.player_start_pos()
        self.cam.set_center((self.player_pos[0] * TILE_WIDTH,
            self.player_pos[1] * TILE_WIDTH - TILE_WIDTH))

        self.player = Player(self.player_pos)


        self.goal = Goal(level_obj.goal_pos())
        self.blocks = []
        for item in level_obj.block_pos():
            self.blocks.append(Block(item))

        self.set_starting_hud()


        self.shrines = []
        self.doors = []
        if self.cur_level.shrine_count() > 0:
            self.shrine_0 = Shrine(self.cur_level.shrine_0_pos(), num=0)
            self.door_0 = Door(self.cur_level.door_0_pos(), self.shrine_0)
            self.shrines.append(self.shrine_0)
            self.doors.append(self.door_0)

        shadow = pygame.Surface(WINDOW_SIZE)
        shadow.fill((0, 0, 0))
        shadow_opacity = 255.0
        shadow_fade_rate = 255.0
        self.shadow_dir = 1
        self.level_start = time.time()
        msg_not_said_yet = 1

        while True:

            now = time.time()
            dt = now - self.then
            self.then = now
            dt = self.cam.time_step(dt)

            if msg_not_said_yet and self.level_counter <= 5:
                self.press_en = 0

            if shadow_opacity < 80 and self.shadow_dir == 1:
                self.test_keydowns()
            else:
                pygame.event.get()

            self.screen.fill((0, 0, 0))

            pypos = self.player.pos[1]

            items_to_draw = self.blocks + self.shrines + self.doors + [self.player] + [self.goal]
            self.draw_items(items_to_draw)

            self.cam.capture(self.screen)

            self.draw_tools(self.screen_commit)

            self.update_objects(dt)
            self.mouse_triggers()

            if shadow_opacity > 0 or self.shadow_dir == -1:
                shadow_opacity = max(0, shadow_opacity - self.shadow_dir * shadow_fade_rate * dt)
                shadow.set_alpha(shadow_opacity)
                self.screen_commit.blit(shadow, (0, 0))
            pygame.display.flip()

            if self.player_hit_goal(level_obj) and self.shadow_dir==1:
                self.collect_gem.play()
                self.cam.set_zoom_pid(5, 1, -0.2)
                self.cam.set_target_zoom(1.5)
                self.goal.sprite.start_animation("collect")
                self.shadow_dir = -1

            if shadow_opacity > 255 and self.shadow_dir == -1:
                break

            level_to_msg = {0: "Welcome to Master Key!\nUse the arrow keys to move.",
                1: "Hold Z while moving to dash.",
                2: "Hold X to push objects.",
                3: "Hold C to hop up ledges.",
                4: "Altars require you to\nsacrifice your controls!\n\nStand in front of the book, and\n drag a key onto it with the mouse.",
                5: "You're on your own now.\n Good Luck!"}

            self.level_to_hint = {0: "Move around with the arrow keys.",
                1: "Hold Z while moving to dash.\nThis allows you to cross short gaps.",
                2: "Hold X while moving to push.\nYou can push cubes into holes.",
                3: "Hold C while moving to jump.\nThis lets you get up short platforms.",
                4: "Try standing next to the book, and\n drag a key onto it with the mouse.",
                5: "You can replace the key on an altar\nby dragging a different key onto it.",
                6: "Don't forget you can sacrifice\nyour movement keys, too!",
                7: "Don't forget you can sacrifice\nyour movement keys, too!",
                8: ""}

            if time.time() - self.level_start > 0.75 and msg_not_said_yet and self.level_counter in level_to_msg and self.shadow_dir != -1:
                self.tooltip(level_to_msg[self.level_counter])
                self.then = time.time()
                msg_not_said_yet = 0
                self.press_en = True

    def draw_items(self, items):
        self.player.pos = self.player.pos[0], self.player.pos[1] + 0.001

        bump_these = []
        for thing in items:
            if thing in self.blocks:
                if thing.mrd == UP and not thing.fell:
                    thing.pos = thing.pos[0], thing.pos[1] + 1
                    bump_these.append(thing)
                    
        if self.mrd == UP:
            self.player.pos = self.player.pos[0], self.player.pos[1] + 1 + self.player.dash_mode
        items.sort(key=lambda x: x.pos[1])
        self.player.pos = self.player.pos[0], int(self.player.pos[1])
        y = 0
        while y <= self.cur_level.height:
            self.cur_level.draw_level(self.screen, y_range = (y, y))
            if not len(items):
                y += 1
                continue
            while items[0].pos[1] == y:
                items[0].draw(self.screen)
                items = items[1:]
                if items == []:
                    break
            y += 1
        if self.mrd == UP:
            self.player.pos = self.player.pos[0], self.player.pos[1] - 1 - self.player.dash_mode

        for block in bump_these:
            block.pos = block.pos[0], block.pos[1] - 1


    def can_move_here(self, pos, block=False, prev_pos = (0, 0), hop = False):

        if self.unpassable_door_here(pos):
            return False

        block_poses = [item.pos for item in self.blocks]

        if self.cur_level.can_move_here(pos, block=block, prev_pos = prev_pos, hop=hop):
            if pos not in block_poses:
                return True

        if self.cur_level.pit_here(pos) and pos in block_poses:
            return True

        return False

    def unpassable_door_here(self, pos):
        for item in self.doors:
            if item.pos == pos:
                if not item.is_passable():
                    return True
        if self.cur_level.unpassable_here(pos):
            return True
        if self.cur_level.shrine_here(pos):
            return True
        return False


    def block_here(self, pos):
        block_poses = [item.pos for item in self.blocks]
        for item in block_poses:
            if item == pos:
                if not self.cur_level.pit_here(pos):
                    return True

        return False

    def test_keydowns(self):

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not self.press_en:
            return

        keydowns = self.player.get_keydowns(events)
        keyups = self.player.get_keyups(events)
        bad_keydowns = self.player.get_bad_keydowns(events)



        for item in keydowns:
            if item in [UP, DOWN, RIGHT, LEFT]:

                if not self.unpassable_door_here(self.player.move_target(item, force_1 = True)):
                    if not self.block_here(self.player.move_target(item, force_1=True)):
                        if self.can_move_here(self.player.move_target(item),
                            prev_pos = self.player.pos,
                            hop=self.player.jump_mode):
                            if self.player.dash_mode:
                                self.dash_sound.play()
                            self.player.move(item)
                            self.mrd = item
                            if self.player.jump_mode:
                                self.player.hop()

                        elif self.can_move_here(self.player.move_target(item, force_1=True),
                            prev_pos = self.player.pos,
                            hop=self.player.jump_mode):
                            if self.player.dash_mode:
                                self.dash_sound.play()
                            self.player.move(item, force_1=True)
                            self.mrd = item
                            if self.player.jump_mode:
                                self.player.hop()

                    elif self.player.push_mode:
                        for block in self.blocks:
                            if block.pos == self.player.move_target(item):
                                target = block.move_target(item)
                                if self.can_move_here((target), block=True):
                                    self.box_slide.play()
                                    block.move(item)
                                    self.player.move(item)
                                    self.mrd = item
                                # elif self.cur_level.

            if item == DASH:
                self.player.dash_mode = 1
            if item == JUMP:
                self.player.jump_mode = 1
            if item == PUSH:
                self.player.push_mode = 1

            if item == RESET:
                self.reset_noise.play()
                self.shadow_dir = -1
                level_index = self.levels.index(self.cur_level)
                self.level_counter -= 1

            if item == HINT:
                self.tooltip(self.level_to_hint[self.level_counter])
                self.then = time.time()

        for item in keyups:
            if item == DASH:
                self.player.dash_mode = 0
            if item == JUMP:
                self.player.jump_mode = 0
            if item == PUSH:
                self.player.push_mode = 0


    def update_objects(self, dt):
        self.hud_key_array.update(dt)
        if len(self.selected_key):
            self.selected_key[0].update(dt)
        for shrine in self.shrines:
            shrine.update(dt)
        for door in self.doors:
            door.update(dt)
        for block in self.blocks:
            block.update(dt)
            if self.cur_level.pit_here(block.pos):
                if block.fell == 0:
                    self.box_fall.play()
                    block.fall()

        self.goal.update(dt)
        

        self.player.update(dt)

        cam_x = self.player.pos[0]*TILE_WIDTH
        cam_y = self.player.pos[1]*TILE_WIDTH
        self.cam.set_target_center((cam_x, cam_y))

    def player_hit_goal(self, level_obj):
        if self.player.pos == level_obj.goal_pos():
            return True


    def draw_tools(self, surf):
        enabled = self.player.control_enables

        self.hud_key_array.draw(surf)
        if len(self.selected_key):
            self.selected_key[0].draw(surf)

    def check_adjacency_to_shrine(self, shrine):
        dist = abs(shrine.pos[0] - self.player.pos[0]) + abs(shrine.pos[1] - self.player.pos[1])
        if dist <= 1:
            return True
        else:
            return False

    def mouse_triggers(self):
        clicked = pygame.mouse.get_pressed()[0]

        if not clicked and len(self.selected_key):
            if len(self.hovered_shrine):
                if self.check_adjacency_to_shrine(self.hovered_shrine[0]):
                    cap_key = self.hovered_shrine[0].captured_key
                    if len(cap_key):
                        cap_key[0].x, cap_key[0].y = (cap_key[0].x - self.cam.pos[0] + WINDOW_WIDTH/2 - HUD_KEY_WIDTH,
                            cap_key[0].y - self.cam.pos[1] + WINDOW_WIDTH/2 - HUD_KEY_HEIGHT - TILE_WIDTH*2)
                        self.hud_key_array.hud_keys.append(cap_key[0])
                    self.selected_key[0].scale = 0.8
                    self.altar_place.play()
                    self.hovered_shrine[0].captured_key = [self.selected_key.pop()]
                else:
                    self.hud_key_array.return_key(self.selected_key[0])
            else:
                self.hud_key_array.return_key(self.selected_key[0])
            self.selected_key = []

        self.hovered_shrine = []

        mpos = pygame.mouse.get_pos()
        mx = mpos[0]
        my = mpos[1]

        for key in self.hud_key_array.hud_keys:
            if key.mouse_over(mpos):
                if key not in self.last_hover:
                    self.last_hover = [key]
                    self.key_select.play()
                if clicked:
                    if len(self.selected_key):
                        self.hud_key_array.return_key(self.selected_key[0])
                    self.hud_key_array.select_key(key.key)
                    self.selected_key = [key]

        if len(self.selected_key):
            key = self.selected_key[0]
            key.target_x = mx - HUD_KEY_WIDTH/2
            key.target_y = my - HUD_KEY_HEIGHT/2

            for item in self.shrines:
                x = item.pos[0] * TILE_WIDTH + -self.cam.pos[0] + WINDOW_WIDTH/2
                y = item.pos[1] * TILE_WIDTH + -self.cam.pos[1] + WINDOW_HEIGHT/2
                key.target_scale = 1.2
                margin = TILE_WIDTH/2
                if mx > x - margin and mx < x + item.width + margin:
                    if my > y - margin and my < y + item.height + margin:
                        key.target_scale = 0.5
                        self.hovered_shrine = [item]

        self.set_control_enables()

    def set_control_enables(self):
        self.player.reset_control_enables()

        for item in self.hud_key_array.hud_keys:
            for k in CONTROLS:
                if CONTROLS[k] == item.key:
                    self.player.control_enables[k] = 1





if __name__ == '__main__':
    a = Game()
