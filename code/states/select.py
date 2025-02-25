from settings import *
from states.state import State

class Select(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.old_image = self.game.level_frames['pause_screen']
        self.image = pygame.transform.scale(self.old_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # set menu options and cursor
        self.select_options = {0: 'LEVEL 1', 1: 'LEVEL 2', 2: 'LEVEL 3'}
        self.index = 0
        self.cursor_rect = pygame.Rect(0, 0, 32, 32)
        self.cursor_pos_x = 300
        self.cursor_rect.x, self.cursor_rect.y = self.cursor_pos_x, WINDOW_HEIGHT/2 + 54

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions['start']:
            self.transition_state()
        if actions['back']:
            self.exit_state()
        self.game.reset_keys()
    
    def render(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "SELECT A LEVEL", 72, WINDOW_WIDTH/2, 240)
        for i, option in self.select_options.items():
            self.game.draw_text(display, option, 32, 380 + i * 250, WINDOW_HEIGHT/2 + 50)
        self.cursor = self.game.draw_text(display, '*', 32, self.cursor_rect.x, self.cursor_rect.y)
        self.game.draw_text(display, "Press ENTER to select and DELETE to return", 20, 1050, 700)

    def update_cursor(self, actions):
        if actions['right']:
            self.index = (self.index + 1) % len(self.select_options)
        if actions['left']:
            self.index = (self.index - 1) % len(self.select_options)
        self.cursor_rect.x = self.cursor_pos_x + self.index * 250
    
    def transition_state(self):
        if self.select_options[self.index] == 'LEVEL 1':
            print("1")
        elif self.select_options[self.index] == 'LEVEL 2':
            print("2")
        elif self.select_options[self.index] == 'LEVEL 3':
            print("3")