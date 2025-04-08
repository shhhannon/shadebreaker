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
        self.cursor_pos_y = WINDOW_HEIGHT/2 + 100
        self.cursor_rect.x, self.cursor_rect.y = WINDOW_WIDTH/2 - 140, self.cursor_pos_y + 4

        self.data = data
        self.user_data = user_data
        self.score = self.data.calculate_score()
        self.game.user_data.update_score(self.score)

    def update(self, dt, actions):
        print(self.game.user_data.scores)
        self.update_cursor(actions)
        if actions['start']:
            self.transition_state()
        self.game.reset_keys()
    
    def render(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "LEVEL COMPLETE", 72, WINDOW_WIDTH/2, 240)
        self.game.draw_text(display, (str(self.score) + "/100"), 80, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        for i, option in self.options.items():
            self.game.draw_text(display, option, 32, WINDOW_WIDTH/2, (WINDOW_HEIGHT/2 + 100) + i * 42)
        self.cursor = self.game.draw_text(display, '*', 32, self.cursor_rect.x, self.cursor_rect.y)

    def update_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.options)
        if actions['up']:
            self.index = (self.index - 1) % len(self.options)
        self.cursor_rect.y = self.cursor_pos_y + self.index * 42 + 4

    def transition_state(self):
        if self.options[self.index] == 'NEXT LEVEL':
            pass
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