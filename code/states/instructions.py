from constants import *
from states.state import State

class Instructions(State):
    def __init__(self, game): 
        State.__init__(self, game)
        self.old_bg_img = self.game.level_frames['pause_screen']
        self.bg_img = pygame.transform.scale(self.old_bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.keys_img = pygame.image.load(os.path.join('..', 'shadebreaker', 'graphics', 'ui', 'instructions', 'arrows.png'))
        self.diamond_img = pygame.image.load(os.path.join('..', 'shadebreaker', 'graphics', 'ui', 'instructions', 'diamond.png'))

    def update(self, delta_time, actions):
        if actions['back']:
            self.exit_state()
    
    def render(self, display):
        display.blit(self.bg_img, (0,0))
        self.game.draw_text(display, "INSTRUCTIONS", 72, WINDOW_WIDTH/2, 240)
        display.blit(self.keys_img, (170, 280))
        display.blit(self.diamond_img, (670, 448))
        self.game.draw_text(display, "-  MOVE", 42, 400, 370)
        self.game.draw_text(display, "X -  ATTACK", 42, 290, 460)
        self.game.draw_text(display, "C -  CHANGE WORLDS", 42, 390, 530)
        self.game.draw_text(display, "Press ENTER to select and DELETE to return", 20, 1050, 700)
        self.game.draw_text(display, "SCORE", 46, 760, 340)
        self.game.draw_text(display, "KILL ENEMIES, COLLECT", 32, 880, 390)
        self.game.draw_text(display, "COINS AND DO IT FAST", 32, 860, 430)
        self.game.draw_text(display, "-    COLLECT TO", 32, 880, 491)
        self.game.draw_text(display, "COMPLETE LEVEL", 32, 900, 531)