from settings import *
from states.state import State
import importlib


class Level_complete(State):
    def __init__(self, game, data, user_data):
        State.__init__(self, game)
        self.old_image = self.game.level_frames['pause_screen']
        self.image = pygame.transform.scale(self.old_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.options = {0: 'NEXT LEVEL', 1: 'RESTART', 2: 'MENU'}
        self.index = 0
        self.cursor_rect = pygame.Rect(0, 0, 32, 32)
        self.cursor_pos_y = WINDOW_HEIGHT/2 + 110
        self.cursor_rect.x, self.cursor_rect.y = WINDOW_WIDTH/2 - 140, self.cursor_pos_y + 4

        self.data = data
        self.user_data = user_data

        self.preview = True
        self.score = self.data.calculate_score(self.user_data.level)
        self.user_data.update_score(self.score)

        #graphics
        self.mark = self.game.ui_frames['score']
        self.star = self.game.ui_frames['star']['large']

    def update(self, dt, actions):
        self.update_cursor(actions)
        if actions['start']:
            self.transition_state()
        self.game.reset_keys()
    
    def render(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "LEVEL COMPLETE", 72, WINDOW_WIDTH/2, 240)
        self.points = 0
        for point in range(3):
            if self.score[point] == 1:
                self.points += 1
        for i in range(3):
            if self.points > 0:
                display.blit(self.star[0], ((WINDOW_WIDTH/2 - 160) + i * 110, 310))
                self.points -= 1
            else:
                display.blit(self.star[1], ((WINDOW_WIDTH/2 - 160) + i * 110, 310))
        for i, option in self.options.items():
            self.game.draw_text(display, option, 32, WINDOW_WIDTH/2, (WINDOW_HEIGHT/2 + 110) + i * 42)
        self.cursor = self.game.draw_text(display, '*', 32, self.cursor_rect.x, self.cursor_rect.y)
        if self.preview == True:
            self.preview_state(display)

    def preview_state(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "LEVEL COMPLETE", 72, WINDOW_WIDTH/2, 240)
        self.secs = int(self.data.total_time / 1000) % 60
        self.mins = int(self.data.total_time / 60000)
        self.game.draw_text(display, ("Time: " + f"{self.mins:02}:{self.secs:02}"), 34, WINDOW_WIDTH/2 - 50, 350)
        self.game.draw_text(display, ("Enemies killed: " + f"{self.data.kills}/{self.data.enemy_count}"), 34, WINDOW_WIDTH/2 - 50, 400)
        self.game.draw_text(display, ("Coins collected: " + f"{self.data.coins}/{self.data.coin_count}"), 34, WINDOW_WIDTH/2 - 50, 450)
        for i in range(3):
            if self.score[i] == 1:
                display.blit(self.mark[0], ((WINDOW_WIDTH/2 + 180), 335 + i * 50))
            else:
                display.blit(self.mark[1], ((WINDOW_WIDTH/2 + 180), 335 + i * 50))
        self.game.draw_text(display, "Press ENTER to continue", 20, 1145, 700)


    def update_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.options)
        if actions['up']:
            self.index = (self.index - 1) % len(self.options)
        self.cursor_rect.y = self.cursor_pos_y + self.index * 42 + 4

    def transition_state(self):
        if self.preview == True:
            self.preview = False
        else:
            if self.options[self.index] == 'NEXT LEVEL':
                self.user_data.level += 1
                for states in range(2):
                    self.game.state_stack.pop()
                playing_module = importlib.import_module('states.playing')
                Playing = getattr(playing_module, 'Playing')
                new_state = Playing(self.game, self.user_data.level, self.user_data)
                new_state.enter_state()
            elif self.options[self.index] == 'RESTART':
                for states in range(2):
                    self.game.state_stack.pop()
                playing_module = importlib.import_module('states.playing')
                Playing = getattr(playing_module, 'Playing')
                new_state = Playing(self.game, self.user_data.level, self.user_data)
                new_state.enter_state()
            elif self.options[self.index] == 'MENU':
                while len(self.game.state_stack) > 2:
                    self.game.state_stack.pop()