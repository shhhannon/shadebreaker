from settings import *
from game.sprites import Sprite, AnimatedSprite
from game.player import Player
from game.groups import AllSprites
from game.enemies import Goblin

class Level:
    def __init__(self, tmx_map, level_frames, game):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.goblin_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

    def setup(self, tmx_map, level_frames):
        # tiles
        for layer in ['bg', 'terrain']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'terrain': groups.append(self.collision_sprites)
                match layer:
                    case 'bg': z = Z_LAYERS['bg tiles']
                    case 'terrain': z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups, z)
            # sprite is in both all_sprites and collision_sprites
        
        # objects
        for obj in tmx_map.get_layer_by_name('objects'):
            if obj.name == 'player':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    frames = level_frames['player'])
            else:
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        # enemies
        for obj in tmx_map.get_layer_by_name('enemies'):
            if obj.name == 'goblin':
                Goblin((obj.x, obj.y), level_frames['goblin'], (self.all_sprites, self.damage_sprites, self.goblin_sprites), self.collision_sprites)

    def update(self, dt):
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)

    def render(self, display):
        self.all_sprites.draw(self.player.hitbox_rect.center)