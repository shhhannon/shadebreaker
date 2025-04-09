from settings import *
from states.state import State
from states.playing import Playing

class Select(State):
    def __init__(self, game, user_data):
        State.__init__(self, game)
        self.user_data = user_data
        self.old_image = self.game.level_frames['pause_screen']
        self.image = pygame.transform.scale(self.old_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # set menu options and cursor
        self.select_options = {0: 'LEVEL 1', 1: 'LEVEL 2', 2: 'LEVEL 3'}
        self.index = 0
        self.cursor_rect = pygame.Rect(0, 0, 32, 32)
        self.cursor_pos_x = 290
        self.cursor_rect.x, self.cursor_rect.y = self.cursor_pos_x, WINDOW_HEIGHT/2 + 46

        # graphics
        self.lock = self.game.level_frames['lock']
        self.stars = self.game.ui_frames['star']['small']

    def update(self, dt, actions):
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
            self.game.draw_text(display, option, 32, 380 + i * 250, WINDOW_HEIGHT/2 + 20)
            if self.user_data.scores[i - 1] == [0, 0, 0] and not i == 0:
                display.blit(self.lock, (318 + i * 250, WINDOW_HEIGHT/2 - 35))
            else:
                # separate scores into two groups: score = 1 and score = 0
                scores = self.user_data.scores[i]
                sorted_scores = [1] * scores.count(1) + [0] * scores.count(0)

                # draw stars with points first
                for j, score in enumerate(sorted_scores):
                    if score == 1:
                        display.blit(self.stars[0], (316 + i * 250 + j * 42, WINDOW_HEIGHT / 2 + 42))
                    else:
                        display.blit(self.stars[1], (316 + i * 250 + j * 42, WINDOW_HEIGHT / 2 + 42))
        self.cursor = self.game.draw_text(display, '*', 32, self.cursor_rect.x, self.cursor_rect.y)
        self.game.draw_text(display, "Press ENTER to select and DELETE to return", 20, 1050, 700)

    def update_cursor(self, actions):
        if actions['right']:
            self.index = (self.index + 1) % len(self.select_options)
        if actions['left']:
            self.index = (self.index - 1) % len(self.select_options)
        self.cursor_rect.x = self.cursor_pos_x + self.index * 250
    
    def transition_state(self):
        if self.user_data.scores[self.index - 1] == [0, 0, 0] and not self.index == 0:
            pass
        else:
            if self.select_options[self.index] == 'LEVEL 1':
                self.user_data.level = 0
            elif self.select_options[self.index] == 'LEVEL 2':
                self.user_data.level = 1
            elif self.select_options[self.index] == 'LEVEL 3':
                self.user_data.level = 2
            new_state = Playing(self.game, self.user_data.level, self.user_data)
            new_state.enter_state()