from settings import *
from game.sprites import Sprite
from game.player import Player

class Level:
    def __init__(self, tmx_map, game):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.setup(tmx_map)

    def setup(self, tmx_map):
        for x, y, surf in tmx_map.get_layer_by_name('terrain').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, (self.all_sprites, self.collision_sprites))
            # sprite is in both all_sprites and collision_sprites

        for obj in tmx_map.get_layer_by_name('objects'):
            if obj.name == 'player':
                Player((obj.x, obj.y), self.all_sprites, self.collision_sprites) #player only has ACCESS to
                # to collision_sprites but is IN all_sprites

    def update(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.display_surface)

    def render(self, display):
        self.all_sprites.draw(display)