from settings import *
from states.state import State
from game.level import Level
from states.pause import Pause

class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.old_bg_img = pygame.image.load(os.path.join(self.game.bg_dir, '0.png'))
        self.bg_img = pygame.transform.scale(self.old_bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.current_stage = Level(self.game.tmx_maps[0], self.game)
    
    def update(self, delta_time, actions):
        if actions['pause']:
            new_state = Pause(self.game)
            new_state.enter_state()
        self.current_stage.update(delta_time)

    def render(self, display):
        display.blit(self.bg_img, (0,0))
        self.current_stage.render(display)