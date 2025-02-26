from settings import *
from random import choice
from game.timer import Timer

class Goblin(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.z = Z_LAYERS['main']

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 150

    def update(self, dt):
        # animate
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # move
        self.rect.x += self.direction * self.speed * dt

        # reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (4, 4))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (4, 4))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0:
            self.direction *= -1

class Gunner(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, player, create_bullet):
        super().__init__(groups)

        self.frames, self.frame_index = frames, 0
        self.flipped_frames = self.flip_frames(frames)
        self.og_frames = self.frames
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.player = player
        self.shoot_timer = Timer(2000)
        self.create_bullet = create_bullet

        self.reversed = False
        self.has_fired = False
        self.bullet_direction = 1
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

    def flip_frames(self, frames):
        flipped_frames = {}
        for key, surfs in self.frames.items():
            flipped_frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
        return flipped_frames

    def state_management(self):
        player_pos, gunner_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = gunner_pos.distance_to(player_pos) < 640
        player_front = player_pos.x > gunner_pos.x
        player_level = abs(gunner_pos.y - player_pos.y) < 30

        if not player_front and not self.reversed:
            self.frames = self.flipped_frames
            self.bullet_direction = -1
            self.reversed = True
        elif player_front and self.reversed:
            self.frames = self.og_frames
            self.bullet_direction = 1
            self.reversed = False

        if player_near and player_level and not self.shoot_timer.active:
            self.state = 'attack'
            self.frame_index = 0
            self.shoot_timer.activate()

    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()

        # animation / attack
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # attack
            if self.state == 'attack' and int(self.frame_index) == 3 and not self.has_fired and not self.reversed:
                self.create_bullet(self.rect.center + vector(32, 20), self.bullet_direction)
                self.has_fired = True
            elif self.state == 'attack' and int(self.frame_index) == 3 and not self.has_fired and self.reversed:
                self.create_bullet(self.rect.center + vector(-32, 20), self.bullet_direction)
                self.has_fired = True
                
        else:
            self.frame_index = 0
            if self.state == 'attack':
                self.state = 'idle'
                self.has_fired = False

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        self.bullet = True
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos + vector(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        self.timers = {'lifetime': Timer(5000)}
        self.timers['lifetime'].activate()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
        
        self.rect.x += self.direction * self.speed * dt
        if not self.timers['lifetime'].active:
            self.kill()

class Crate(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, create_fly):
        super().__init__(groups)
        
        self.frames, self.frame_index = frames, 0
        self.flipped_frames = self.flip_frames(frames)
        self.og_frames = self.frames
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.player = player

        self.fly_timer = Timer(30000)
        self.create_fly = create_fly

        self.reversed = False
        self.has_fired = False
    
    def flip_frames(self, frames):
        flipped_frames = {}
        for key, surfs in self.frames.items():
            flipped_frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
        return flipped_frames
    
    def state_management(self):
        player_pos, gunner_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = gunner_pos.distance_to(player_pos) < 640
        player_front = player_pos.x > gunner_pos.x

        if not player_front and not self.reversed:
            self.frames = self.flipped_frames
            self.reversed = True
        elif player_front and self.reversed:
            self.frames = self.og_frames
            self.reversed = False

        if player_near and not self.fly_timer.active:
            self.state = 'active'
            self.frame_index = 0
            self.fly_timer.activate()
        
    def update(self, dt):
        self.fly_timer.update()
        self.state_management()

        # animation / attack
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # attack
            if self.state == 'active' and int(self.frame_index) == 2 and not self.has_fired:
                self.create_fly(self.rect.center)
                self.has_fired = True

        else:
            self.frame_index = 0
            if self.state == 'active':
                self.state = 'idle'
                self.has_fired = False

class Fly(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, surf, collision_sprites, player):
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.flipped_frames = self.flip_frames(frames)
        self.og_frames = self.frames
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.z = Z_LAYERS['main']
        self.player = player
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        self.attack_timer = Timer(2000)
        self.has_attacked = False
        self.speed = 150
        self.reversed = False

    def flip_frames(self, frames):
        flipped_frames = {}
        for key, surfs in self.frames.items():
            flipped_frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
        return flipped_frames
    
    def attack(self, dt):
        if int(self.frame_index) == 2 and not self.has_attacked:
            self.pre_attack_pos = vector(self.rect.center)
            self.player_pos, self.fly_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
            self.direction = (self.player_pos - self.fly_pos).normalize()
            self.rect.x += self.direction.x * self.speed * dt * 2
            self.rect.y += self.direction.y * self.speed * dt * 2

            if self.rect.colliderect(self.player.hitbox_rect):
                return_vector = self.pre_attack_pos - self.fly_pos
                while return_vector.length() != 0:
                    return_vector = self.pre_attack_pos - self.fly_pos
                    self.direction = return_vector.normalize()
                    self.rect.x += self.direction.x * self.speed * dt
                    self.rect.y += self.direction.y * self.speed * dt
                    self.fly_pos = (self.rect.x, self.rect.y)
                self.has_attacked = True
                self.state = 'idle'

    
    def state_management(self):
        player_pos, fly_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = fly_pos.distance_to(player_pos) < 64
        player_front = player_pos.x > fly_pos.x

        if not player_front and not self.reversed:
            self.frames = self.flipped_frames
            self.reversed = True
        elif player_front and self.reversed:
            self.frames = self.og_frames
            self.reversed = False

        if player_near and not self.attack_timer.active:
            self.state = 'attack'
            self.frame_index = 0
            self.attack_timer.activate()
        elif not player_near:
            self.state = 'idle'
            self.frame_index = 0
            self.has_attacked = False

    def update(self, dt):
        self.attack_timer.update
        self.state_management()
        print(self.state)

        # animate
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index) % int(len(self.frames[self.state]))]

        # move
        if self.state == 'attack':
            self.attack(dt)
        else:
            player_pos = vector(self.player.hitbox_rect.center)
            fly_pos = vector(self.rect.center)
            move_vector = player_pos - fly_pos
            if move_vector.length() != 0:
                self.direction = move_vector.normalize()
                self.rect.x += self.direction.x * self.speed * dt
                self.rect.y += self.direction.y * self.speed * dt