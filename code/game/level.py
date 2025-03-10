from settings import *
from game.sprites import Sprite, AnimatedSprite, Item
from game.player import Player
from game.groups import AllSprites
from game.enemies import Goblin, Gunner, Bullet, Crate, Fly

class Level:
    def __init__(self, tmx_map, level_frames, game, data):
        self.display_surface = pygame.display.get_surface()
        self.tmx_map = tmx_map
        self.level_frames = level_frames
        self.game = game
        self.data = data

        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        self.lava_height = 0

        # groups
        self.all_sprites = AllSprites(
            width = self.level_width,
            height = self.level_bottom
        )
        self.collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.goblin_sprites = pygame.sprite.Group()
        self.gunner_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.crate_sprites = pygame.sprite.Group()
        self.fly_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)

        # frames
        self.bullet_surf = level_frames['bullet']
        self.fly_surf = level_frames['fly']['idle'][0]

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
                    frames = level_frames['player'],
                    data = self.data)
            elif obj.name == 'door':
                self.door_rect = pygame.Rect((obj.x, obj.y), (obj.width, obj.height))
                Sprite((obj.x, obj.y), obj.image, (self.all_sprites), Z_LAYERS['bg tiles'])
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
                    groups = (self.all_sprites, self.gunner_sprites), 
                    collision_sprites = self.collision_sprites, 
                    player = self.player,
                    create_bullet = self.create_bullet)
            if obj.name == 'crate':
                Crate(
                    pos = (obj.x, obj.y),
                    frames = level_frames['crate'],
                    groups = (self.all_sprites, self.collision_sprites, self.crate_sprites),
                    player = self.player,
                    create_fly = self.create_fly)
                
        # items
        for obj in tmx_map.get_layer_by_name('items'):
            Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)

        # lava
        for obj in tmx_map.get_layer_by_name('lava'):
            self.lava_height = obj.y
            rows = int(obj.height // TILE_SIZE)
            cols = int(obj.width // TILE_SIZE)
            for row in range(rows):
                for col in range(cols):
                    x = obj.x + col * TILE_SIZE
                    y = obj.y + row * TILE_SIZE
                    Sprite((x, y), level_frames['lava'], self.all_sprites, Z_LAYERS['lava'])
         
    def create_bullet(self, pos, direction):
        Bullet(pos, (self.all_sprites, self.damage_sprites, self.bullet_sprites), self.bullet_surf, direction, 150)
    
    def bullet_collision(self):
        for sprite in self.collision_sprites:
            pygame.sprite.spritecollide(sprite, self.bullet_sprites, True)

    def create_fly(self, pos):
        Fly(
            pos = pos,
            frames = self.game.level_frames['fly'],
            groups = (self.all_sprites, self.damage_sprites, self.fly_sprites),
            surf = self.fly_surf,
            collision_sprites = self.collision_sprites,
            player = self.player
        )

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                self.player.get_damage()
                if hasattr(sprite, 'bullet'):
                    sprite.kill()
        
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            if item_sprites:
                item_sprites[0].activate()

    def attack_collision(self):
        for target in self.crate_sprites.sprites() + self.fly_sprites.sprites() + self.gunner_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
                self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.hit()

        for target in self.goblin_sprites.sprites() + self.bullet_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
                self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.reverse()

    def check_constraint(self):
        # left right
        if self.player.hitbox_rect.left <= 0:
            self.player.hitbox_rect.left = 0
        if self.player.hitbox_rect.right >= self.level_width:
            self.player.hitbox_rect.right = self.level_width

        # bottom
        if self.player.hitbox_rect.bottom >= self.lava_height:
            for health in range(self.data.health):
                self.player.get_damage()
        if self.player.hitbox_rect.bottom >= self.level_bottom:
            self.dead = True

        if self.player.hitbox_rect.colliderect(self.door_rect) and self.data.has_diamond:
            print('win')

    def check_player(self):
        if self.player.dead:
            self.restart_level()

    def restart_level(self):
        # Reinitialize the level
        self.data.health = self.data.max_health
        self.data.has_diamond = False
        self.__init__(self.tmx_map, self.level_frames, self.game, self.data)
        self.player.dead = False

    def update(self, dt):
        self.all_sprites.update(dt)
        self.bullet_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        self.check_constraint()
        self.check_player()

        self.all_sprites.draw(self.player.hitbox_rect.center)

    def render(self, display):
        self.all_sprites.draw(self.player.hitbox_rect.center)