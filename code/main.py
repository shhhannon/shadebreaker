from settings import *
from pytmx.util_pygame import load_pygame
from states.title import Title
from game.userdata import UserData

from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Shadebreaker')
        self.clock = pygame.time.Clock()
        self.import_assets()
        self.user_data = UserData()

        self.running, self.playing = True, False
        self.actions = {"left": False, "right": False, "up": False, "down": False, "back": False, "start": False, "pause": False}
        self.dt, self.prev_time = 0, 0 
        self.state_stack = []
        self.load_states()

        self.tmx_maps = {0: load_pygame(os.path.join('..', 'shadebreaker', 'data', 'levels', '0.tmx')),
                         1: load_pygame(os.path.join('..', 'shadebreaker', 'data', 'levels', '1.tmx')),
                         2: load_pygame(os.path.join('..', 'shadebreaker', 'data', 'levels', '2.tmx'))}
        
    def import_assets(self): # need to create folder for level backgrounds
        self.level_frames = {
            'menu_screen': import_image('..', 'shadebreaker', 'graphics', 'level', 'bg', 'menu'),
            'pause_screen': import_image('..', 'shadebreaker', 'graphics', 'level', 'bg', 'pause'),
            'lock': import_image('..', 'shadebreaker', 'graphics', 'ui', 'lock'),
            '0': import_folder('..', 'shadebreaker', 'graphics', 'level', 'bg', '0'),
            '1': import_folder('..', 'shadebreaker', 'graphics', 'level', 'bg', '1'),
            '2': import_folder('..', 'shadebreaker', 'graphics', 'level', 'bg', '2'),
            'door': import_sub_folders('..', 'shadebreaker', 'graphics', 'level', 'door'),
            'diamond': import_folder('..', 'shadebreaker', 'graphics', 'items', 'diamond'),
            'player': import_sub_folders('..', 'shadebreaker', 'graphics', 'player'),
            'goblin': import_sub_folders('..', 'shadebreaker', 'graphics', 'enemies', 'goblin'),
            'gunner': import_sub_folders('..', 'shadebreaker', 'graphics', 'enemies', 'gunner'),
            'bullet': import_image('..', 'shadebreaker', 'graphics', 'enemies', 'bullets', 'bullet'),
            'crate': import_sub_folders('..', 'shadebreaker', 'graphics', 'enemies', 'crate'),
            'fly': import_sub_folders('..', 'shadebreaker', 'graphics', 'enemies', 'fly'),
            'items': import_sub_folders('..', 'shadebreaker', 'graphics', 'items'),
            'lava': import_image('..', 'shadebreaker', 'graphics', 'level', 'lava', '0'),
        }

        self.ui_frames = {
            'heart': import_sub_folders('..', 'shadebreaker', 'graphics', 'ui', 'hearts'),
            'diamond': import_sub_folders('..', 'shadebreaker', 'graphics', 'ui', 'diamonds'),
            'bar': import_sub_folders('..', 'shadebreaker', 'graphics', 'ui', 'switch_bar'),
            'score': import_folder('..', 'shadebreaker', 'graphics', 'ui', 'score'),
            'star': import_sub_folders('..', 'shadebreaker', 'graphics', 'ui', 'stars'),
        }
        self.font_dir = os.path.join("graphics", "ui")
        self.font = pygame.font.Font(os.path.join(self.font_dir, "Krungthep.ttf"), 30)

    
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
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, size, x, y):
        self.menu_font = pygame.font.Font(os.path.join(self.font_dir, "Krungthep.ttf"), size)
        text_surf = self.menu_font.render(text, True, (255, 255, 255))
        text_surf.set_colorkey((0,0,0))
        text_rect = text_surf.get_frect()
        text_rect.center = (x, y)
        surface.blit(text_surf, text_rect)

    def load_states(self):
        self.title_screen = Title(self, self.user_data)
        self.state_stack.append(self.title_screen)


if __name__ == "__main__": 
    game = Game()
    
    while game.running:
        game.playing = True
        game.run()