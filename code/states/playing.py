from settings import *
from states.state import State
from states.pause import Pause
from states.level_complete import Level_complete

from game.level import Level
from game.data import Data
from game.ui import UI

class Playing(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.ui = UI(self.game.font, self.game.ui_frames)
        self.data = Data(self.ui)
            
        self.current_stage = Level(self.game.tmx_maps[0], self.game.level_frames, self.game, self.data)
    
    def update(self, dt, actions):
        if actions['pause']:
            new_state = Pause(self.game)
            new_state.enter_state()
        self.current_stage.update(dt)
        self.ui.update(dt)
        if self.data.level_complete:
            new_state = Level_complete(self.game, self.data)
            new_state.enter_state()
            self.data.level_complete = False

    def render(self, display):
        #display.blit(self.bg_img, (0,0))
        self.current_stage.render(display)
        self.ui.render()