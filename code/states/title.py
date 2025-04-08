from settings import *
from states.state import State
from states.menu import Menu

class Title(State):
    def __init__(self, game, user_data):
        State.__init__(self, game)
        self.user_data = user_data
        self.old_image = self.game.level_frames['menu_screen']
        self.image = pygame.transform.scale(self.old_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def update(self, dt, actions):
        if actions['start']:
            new_state = Menu(self.game, self.user_data)
            new_state.enter_state()
    
    def render(self, display):
        display.blit(self.image, (0,0))
        self.game.draw_text(display, "SHADEBREAKER", 76, WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        self.game.draw_text(display, "CLICK ENTER TO START", 24, WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 62)