from settings import *
from pytmx.util_pygame import load_pygame
from states.title import Title

from support import *

class Game:
    def __init__(self):
        pygame.init()
        #self.GAME_W, self.GAME_H = 800, 600
        #self.game_canvas = pygame.Surface((self.GAME_W, self.GAME_H))
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Shadebreaker')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.running, self.playing = True, False
        self.actions = {"left": False, "right": False, "up": False, "down": False, "back": False, "start": False, "pause": False}
        self.dt, self.prev_time = 0, 0 
        self.state_stack = []
        self.load_assets()
        self.load_states()

        self.tmx_maps = {0: load_pygame(os.path.join('..', 'shadebreaker', 'data', 'levels', '0.tmx'))}

    def import_assets(self):
        self.level_frames = {
            'door': import_sub_folders('..', 'shadebreaker', 'graphics', 'level', 'door'),
            'diamond': import_folder('..', 'shadebreaker', 'graphics', 'items', 'diamond'),
            'player': import_sub_folders('..', 'shadebreaker', 'graphics', 'player')
        }
        print(self.level_frames['player'])

    
    def run(self):
        while self.playing:
            self.get_dt()
            self.inputs()
            self.update()
            self.render()
    
    def inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.actions['back'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True
                if event.key == pygame.K_LEFT:
                    self.actions['left'] = True
                if event.key == pygame.K_RIGHT:
                    self.actions['right'] = True
                if event.key == pygame.K_UP:
                    self.actions['up'] = True
                if event.key == pygame.K_DOWN:
                    self.actions['down'] = True
                if event.key == pygame.K_ESCAPE:
                    self.actions['pause'] = True

    def reset_keys(self):
        for key in self.actions:
            self.actions[key] = False

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)
        self.reset_keys()
    
    def render(self):
        self.state_stack[-1].render(self.display_surface)
        #self.screen.blit(pygame.transform.scale(self.game_canvas, (self.DISPLAY_W, self.DISPLAY_H)), (0, 0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, size, x, y):
        self.font = pygame.font.Font(os.path.join(self.font_dir, "Krungthep.ttf"), size)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_frect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_assets(self):
        # pointers to directories
        self.graphics_dir = os.path.join("graphics")
        self.bg_dir = os.path.join(self.graphics_dir, "level", "bg")
        self.font_dir = os.path.join(self.graphics_dir, "ui", "UIfonts")
    
    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)


if __name__ == "__main__": 
    game = Game()
    while game.running:
        game.playing = True
        game.run()