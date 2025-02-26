from settings import *
from states.state import State

class Instructions(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.old_bg_img = self.game.level_frames['menu_screen']
        self.bg_img = pygame.transform.scale(self.old_bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.keys_img = pygame.image.load(os.path.join('..', 'shadebreaker', 'graphics', 'ui', 'instructions', 'arrows.png'))
        self.diamond_img = pygame.image.load(os.path.join('..', 'shadebreaker', 'graphics', 'ui', 'instructions', 'diamond.png'))

    def update(self, delta_time, actions):
        if actions['back']:
            self.exit_state()
    
    def render(self, display):
        display.blit(self.bg_img, (0,0))
        self.game.draw_text(display, "CONTROLS", 72, WINDOW_WIDTH/2, 240)
        display.blit(self.keys_img, (200, 350))
        self.game.draw_text(display, "Press ENTER to select and DELETE to return", 20, 1050, 700)