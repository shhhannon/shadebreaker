from settings import *
from game.sprites import Sprite, AnimatedSprite
from game.player import Player
from game.groups import AllSprites
from game.enemies import Goblin, Gunner, Bullet

class Level:
    def __init__(self, tmx_map, level_frames, game):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.goblin_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

        # frames
        self.bullet_surf = level_frames['bullet']

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
            if obj.name == 'gunner':
                Gunner(
                    pos = (obj.x, obj.y), 
                    frames = level_frames['gunner'], 
                    groups = (self.all_sprites, self.damage_sprites), 
                    collision_sprites = self.collision_sprites, 
                    player = self.player,
                    create_bullet = self.create_bullet)

    def create_bullet(self, pos, direction):
        Bullet(pos, (self.all_sprites, self.damage_sprites, self.bullet_sprites), self.bullet_surf, direction, 150)
    
    def bullet_collision(self):
        for sprite in self.collision_sprites:
            pygame.sprite.spritecollide(sprite, self.bullet_sprites, True)

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                print('player damage')
                if hasattr(sprite, 'bullet'):
                    sprite.kill()
        
    def update(self, dt):
        self.all_sprites.update(dt)
        self.bullet_collision()
        self.hit_collision()
        self.all_sprites.draw(self.player.hitbox_rect.center)

    def render(self, display):
        self.all_sprites.draw(self.player.hitbox_rect.center)