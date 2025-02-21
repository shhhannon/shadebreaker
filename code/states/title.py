from settings import *
from states.state import State
from states.menu import Menu

class Title(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.old_image = pygame.image.load(os.path.join(self.game.bg_dir, 'menu.png'))
        self.image = pygame.transform.scale(self.old_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def update(self, delta_time, actions):
        if actions['start']:
            new_state = Menu(self.game)
            new_state.enter_state()
    
    def render(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "SHADEBREAKER", 76, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.game.draw_text(display, "CLICK ENTER TO START", 24, WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 62)