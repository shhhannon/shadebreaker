from constants import *
from game.sprites import AllSprites, Sprite, Item
from game.player import Player
from game.enemies import Goblin, Gunner, Bullet, Crate, Fly
from game.timer import Timer

class Level:
    def __init__(self, tmx_map, level_frames, game, data, user_data):
        self.display_surface = pygame.display.get_surface()
        self.tmx_map = tmx_map
        self.level_frames = level_frames
        self.game = game
        self.data = data
        self.user_data = user_data

        # level data
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_bottom = tmx_map.height * TILE_SIZE
        self.lava_height = 0

        self.old_bg_img = self.game.level_frames[str(self.user_data.level)][0]
        self.bg_img = pygame.transform.scale(self.old_bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # groups
        self.all_sprites = AllSprites(
            width = self.level_width,
            height = self.level_bottom
        )
        self.change_sprites = pygame.sprite.Group()
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
        
        # objects
        self.load_objects(tmx_map, level_frames)

    def check_world(self):
        if not self.data.light_world:
            self.old_bg_img = self.game.level_frames[str(self.user_data.level)][0]
        else:
            self.old_bg_img = self.game.level_frames[str(self.user_data.level)][1]
        self.bg_img = pygame.transform.scale(self.old_bg_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

        for sprite in self.change_sprites:
            self.all_sprites.remove(sprite)
            self.collision_sprites.remove(sprite)
        self.change_sprites.empty()

        if not self.data.light_world:
            for x, y, surf in self.tmx_map.get_layer_by_name('dark').tiles():
                groups = [self.all_sprites, self.collision_sprites, self.change_sprites]
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, Z_LAYERS['main'])
        else:
            for x, y, surf in self.tmx_map.get_layer_by_name('light').tiles():
                groups = [self.all_sprites, self.collision_sprites, self.change_sprites]
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, groups, Z_LAYERS['main'])
        
    def load_objects(self, tmx_map, level_frames):
        # objects
        for obj in tmx_map.get_layer_by_name('objects'):
            if obj.name == 'player':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    frames = level_frames['player'],
                    data = self.data)
                
        for obj in tmx_map.get_layer_by_name('objects'):
            if obj.name == 'door':
                self.door_rect = pygame.Rect((obj.x, obj.y), (obj.width, obj.height))
                Door((obj.x, obj.y), level_frames['door'], self.all_sprites, self.player, self.data, Z_LAYERS['bg tiles'])
        
        # enemies
        for obj in tmx_map.get_layer_by_name('enemies'):
            self.data.enemy_count += 1
            if obj.name == 'goblin':
                Goblin((obj.x, obj.y), level_frames['goblin'], (self.all_sprites, self.damage_sprites, self.goblin_sprites), self.collision_sprites, self.data)
            if obj.name == 'gunner':
                Gunner(
                    pos = (obj.x, obj.y), 
                    frames = level_frames['gunner'], 
                    groups = (self.all_sprites, self.gunner_sprites), 
                    collision_sprites = self.collision_sprites, 
                    player = self.player,
                    create_bullet = self.create_bullet,
                    data = self.data)
            if obj.name == 'crate':
                Crate(
                    pos = (obj.x, obj.y),
                    frames = level_frames['crate'],
                    groups = (self.all_sprites, self.collision_sprites, self.crate_sprites),
                    player = self.player,
                    create_fly = self.create_fly,
                    data = self.data)
                
        # items
        for obj in tmx_map.get_layer_by_name('items'):
            Item(obj.name, (obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), level_frames['items'][obj.name], (self.all_sprites, self.item_sprites), self.data)
            if obj.name == 'silver':
                self.data.coin_count += 1

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
                #self.player.get_damage()
                if hasattr(sprite, 'bullet'):
                    sprite.kill()
        
    def item_collision(self):
        if self.item_sprites:
            item_sprites = pygame.sprite.spritecollide(self.player, self.item_sprites, True)
            if item_sprites:
                item_sprites[0].activate()

    def attack_collision(self):
        for target in self.crate_sprites.sprites() + self.fly_sprites.sprites() + self.gunner_sprites.sprites() + self.goblin_sprites.sprites():
            facing_target = self.player.rect.centerx < target.rect.centerx and self.player.facing_right or \
                self.player.rect.centerx > target.rect.centerx and not self.player.facing_right
            if target.rect.colliderect(self.player.rect) and self.player.attacking and facing_target:
                target.hit()
                if target in self.goblin_sprites.sprites():
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
            self.player.dead = True

    def check_player(self):
        self.player_centre = self.player.hitbox_rect.center[0]
        self.door_centre = self.door_rect.center[0]
        self.distance = self.player_centre - self.door_centre
        if self.player.dead:
            self.restart_level()
        if abs(self.distance) < 20 and self.data.has_diamond:
            self.player.kill()
            self.data.level_complete = True

    def restart_level(self):
        # clear all sprites
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.damage_sprites.empty()
        self.goblin_sprites.empty()
        self.gunner_sprites.empty()
        self.bullet_sprites.empty()
        self.crate_sprites.empty()
        self.fly_sprites.empty()
        self.item_sprites.empty()

        # reset the level data
        self.player = None
        self.door = None
        self.data.health = self.data.max_health
        self.data.has_diamond = False
        self.data.kills = 0
        self.data.coins = 0
        self.data.enemy_count = 0
        self.data.coin_count = 0
        self.data.game_timer.activate()
        
        self.setup(self.tmx_map, self.level_frames)
        self.player.dead = False

    def update(self, dt):

        # updating timer
        self.time = self.data.game_timer.get_time()
        self.data.update_timer(self.time)

        self.all_sprites.update(dt)
        self.bullet_collision()
        self.hit_collision()
        self.item_collision()
        self.attack_collision()
        self.check_constraint()
        self.check_player()
        self.check_world()

    def render(self, display):
        display.blit(self.bg_img, (0,0))
        self.all_sprites.draw(self.player.hitbox_rect.center)

class Door(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, data, z):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.player = player
        self.data = data
        self.z = z

        self.opened = False
        self.was_near = False

    def state_management(self):
        player_pos, door_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = door_pos.distance_to(player_pos) < 320

        if player_near and self.data.has_diamond:
            self.state = 'opening'
            self.opened = True
            self.was_near = True
            if self.state != 'opening':
                self.frame_index = 0
        if self.was_near and not player_near:
            self.state = 'closing'
            self.opened = False
            if self.state != 'closing':
                self.frame_index = 0

        self.was_near = player_near
        
        if self.state == 'closing' and self.frame_index >= len(self.frames[self.state]):
            self.state = 'idle'
            self.frame_index = 0

    def update(self, dt):
        self.state_management()

        if self.opened and self.frame_index >= 4:
            self.frame_index = 4

        # animation
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]