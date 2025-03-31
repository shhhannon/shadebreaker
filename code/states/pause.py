from settings import *
import importlib
from states.state import State

class Pause(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.old_image = self.game.level_frames['pause_screen']
        self.image = pygame.transform.scale(self.old_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.pause_options = {0: 'RESUME', 1: 'RESTART', 2: 'MENU'}
        self.index = 0
        self.cursor_rect = pygame.Rect(0, 0, 32, 32)
        self.cursor_pos_y = WINDOW_HEIGHT/2
        self.cursor_rect.x, self.cursor_rect.y = WINDOW_WIDTH/2 - 140, self.cursor_pos_y + 4

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions['start']:
            self.transition_state()
        self.game.reset_keys()
    
    def render(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "PAUSED", 72, WINDOW_WIDTH/2, 240)
        for i, option in self.pause_options.items():
            self.game.draw_text(display, option, 32, WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + i * 42)
        self.cursor = self.game.draw_text(display, '*', 32, self.cursor_rect.x, self.cursor_rect.y)

    def update_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.pause_options)
        if actions['up']:
            self.index = (self.index - 1) % len(self.pause_options)
        self.cursor_rect.y = self.cursor_pos_y + self.index * 42 + 4

    def transition_state(self):
        if self.pause_options[self.index] == 'RESUME':
            self.exit_state()
        elif self.pause_options[self.index] == 'RESTART':
            for states in range(2):
                self.game.state_stack.pop()
            playing_module = importlib.import_module('states.playing')
            Playing = getattr(playing_module, 'Playing')
            new_state = Playing(self.game, self.game.level)
            new_state.enter_state()
        elif self.pause_options[self.index] == 'MENU':
            while len(self.game.state_stack) > 2:
                self.game.state_stack.pop()