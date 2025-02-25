from settings import *
from states.state import State
from states.playing import Playing
from states.select import Select
from states.instructions import Instructions

class Menu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.old_image = self.game.level_frames['menu_screen']
        self.image = pygame.transform.scale(self.old_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # set menu options and cursor
        self.menu_options = {0: 'CONTINUE', 1: 'SELECT LEVEL', 2: 'INSTRUCTIONS', 3: 'QUIT'}
        self.index = 0
        self.cursor_rect = pygame.Rect(0, 0, 32, 32)
        self.cursor_pos_y = WINDOW_HEIGHT/2
        self.cursor_rect.x, self.cursor_rect.y = WINDOW_WIDTH/2 - 140, self.cursor_pos_y + 4

    def update(self, delta_time, actions):
        self.update_cursor(actions)
        if actions['start']:
            self.transition_state()
        if actions['back']:
            self.exit_state()
        self.game.reset_keys()
    
    def render(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "SHADEBREAKER", 72, WINDOW_WIDTH/2, 240)
        for i, option in self.menu_options.items():
            self.game.draw_text(display, option, 32, WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + i * 42)
        self.cursor = self.game.draw_text(display, '*', 32, self.cursor_rect.x, self.cursor_rect.y)
        self.game.draw_text(display, "Press ENTER to select and DELETE to return", 20, 1050, 700)

    def update_cursor(self, actions):
        if actions['down']:
            self.index = (self.index + 1) % len(self.menu_options)
        if actions['up']:
            self.index = (self.index - 1) % len(self.menu_options)
        self.cursor_rect.y = self.cursor_pos_y + self.index * 42 + 4
    
    def transition_state(self):
        if self.menu_options[self.index] == 'CONTINUE':
            pass
            new_state = Playing(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == 'SELECT LEVEL':
            new_state = Select(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == 'INSTRUCTIONS':
            new_state = Instructions(self.game)
            new_state.enter_state()
        elif self.menu_options[self.index] == 'QUIT':
            self.game.running, self.game.playing = False, False
            pygame.quit()
            sys.exit()