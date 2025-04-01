from settings import *
from random import choice
import math
from math import sin
import random
from game.timer import Timer

# code the goblin health

class Goblin(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, data):
        super().__init__(groups)
        self.z = Z_LAYERS['main']
        self.data = data
        self.state = 'run'
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.health = 3

        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.speed = 150

        self.timers = {'reverse': Timer(300), 'hit': Timer(1000)}

    def hit(self):
        if not self.timers['hit'].active:
            self.state = 'hit'
            self.health -= 1
            self.frame_index = 0
            self.timers['hit'].activate()

    def die(self):
        self.state = 'die'
        if self.state != 'die':
            self.frame_index = 0
        if self.frame_index >= 2:
            self.kill()
            self.data.kills += 1

    def reverse(self):
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()

        if self.health <= 0:
            self.die()

        # animate
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index > len(self.frames[self.state]):
            if self.state == 'hit':
                self.frame_index = 0
                self.state = 'run'
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image

        # move
        self.rect.x += self.direction * self.speed * dt

        # reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (4, 4))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (4, 4))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1,0), (self.rect.width + 2, 1))

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
            self.direction *= -1

class Gunner(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites, player, create_bullet, data):
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
        self.timers = {'shoot': Timer(2000), 'hit': Timer(1000)}
        self.create_bullet = create_bullet
        self.data = data

        self.reversed = False
        self.has_fired = False
        self.bullet_direction = 1
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.health = 3

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

        if player_near and player_level and not self.timers['shoot'].active:
            self.state = 'attack'
            self.frame_index = 0
            self.timers['shoot'].activate()

        if self.health <= 0:
            self.die()

    def hit(self):
        if not self.timers['hit'].active:
            self.state = 'hit'
            self.health -= 1
            self.frame_index = 0
            self.timers['hit'].activate()
        if self.frame_index >= 2:
            if self.state != 'attack':
                self.state = 'attack'
                self.frame_index = 0
                self.timers['shoot'].activate()

    def die(self):
        self.state = 'die'
        if self.state != 'die':
            self.frame_index = 0
        if self.frame_index >= 2:
            self.kill()
            self.data.kills += 1

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
        self.state_management()

        # animation / attack
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # attack
            if self.state == 'attack' and int(self.frame_index) == 3 and not self.has_fired and not self.reversed:
                self.create_bullet(self.rect.center + vector(26, 20), self.bullet_direction)
                self.has_fired = True
            elif self.state == 'attack' and int(self.frame_index) == 3 and not self.has_fired and self.reversed:
                self.create_bullet(self.rect.center + vector(-26, 20), self.bullet_direction)
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
        self.timers = {'lifetime': Timer(5000), 'hit': Timer(250)}
        self.timers['lifetime'].activate()

    def reverse(self):
        if not self.timers['hit'].active:
            self.direction *= -1
            self.timers['hit'].activate()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
        
        self.rect.x += self.direction * self.speed * dt
        if not self.timers['lifetime'].active:
            self.kill()

class Crate(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, create_fly, data):
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
        self.health = 5
        self.data = data

        self.fly_timer = Timer(120000)
        self.timers = {'fly': Timer(7000), 'hit': Timer(1000)}
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

        if player_near and not self.timers['fly'].active:
            self.state = 'active'
            self.frame_index = 0
            self.timers['fly'].activate()

        if self.health <= 0:
            self.die()

    def hit(self):
        if not self.timers['hit'].active:
            self.state = 'hit'
            self.frame_index = 0
            self.health -= 1
            self.timers['hit'].activate()
        if self.frame_index >= 2:
            if self.state != 'idle':
                self.state = 'idle'
                self.frame_index = 0

    def die(self):
        self.state = 'hit'
        if self.state != 'hit':
            self.frame_index = 0
        if self.frame_index >= 1:
            self.kill()
            self.data.kills += 1

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
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
        self.state = 'die'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft = pos)
        self.z = Z_LAYERS['main']
        self.player = player
        self.health = 2
        self.collision_rects = [sprite.rect for sprite in collision_sprites]

        self.pre_attack_pos = vector(self.rect.center)
        self.offset = vector()

        self.timers = {'attack': Timer(3000), 'hit': Timer(1000)}
        self.speed = 150
        self.reversed = False

        self.retreating = False

    def flip_frames(self, frames):
        flipped_frames = {}
        for key, surfs in self.frames.items():
            flipped_frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
        return flipped_frames
    
    def random_pos(self):
        angle = random.uniform(math.pi, math.pi * 2)
        distance = random.uniform(64, 76)
        offset = vector(math.cos(angle) * distance, math.sin(angle) * distance)
        return offset
    
    def state_management(self):
        player_pos, fly_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = fly_pos.distance_to(player_pos) <= 76
        player_front = player_pos.x > fly_pos.x

        if not player_front and not self.reversed:
            self.frames = self.flipped_frames
            self.reversed = True
        elif player_front and self.reversed:
            self.frames = self.og_frames
            self.reversed = False

        if player_near and not self.timers['attack'].active and fly_pos.distance_to(player_pos + self.offset) < 2:
            if self.state != 'attack':
                self.pre_attack_pos = fly_pos
            self.state = 'attack'
            self.frame_index = 0
            self.timers['attack'].activate()
        if player_near and not self.timers['attack'].active and fly_pos.distance_to(player_pos + self.offset) >= 2:
            self.state = 'idle'
        elif not player_near:
            if self.state != 'idle':
                self.offset = self.random_pos()
                self.frame_index = 0
            self.state = 'idle'
            self.timers['attack'].deactivate()

        if self.health <= 0:
            self.die()
                
    def attack(self, dt, pre_attack_pos):
        if int(self.frame_index) == 3 :
            if not self.retreating:
                self.pre_attack_pos = pre_attack_pos
                self.player_pos, self.fly_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
                self.direction = (self.player_pos - self.fly_pos).normalize()
                self.rect.x += self.direction.x * self.speed * dt * 2
                self.rect.y += self.direction.y * self.speed * dt * 2

            if self.rect.colliderect(self.player.hitbox_rect.inflate(-2, -2)):
                self.retreating = True  # Start moving back to pre-attack position

        if self.retreating:
            direction = (self.pre_attack_pos - vector(self.rect.center))
            if direction.length() != 0:
                t = 0.1  # Interpolation factor, adjust for smoothness
                new_position = vector(self.rect.center) + (self.pre_attack_pos - vector(self.rect.center)) * t
                self.rect.center = new_position

            if vector(self.rect.center).distance_to(self.pre_attack_pos) < 1:
                self.rect.center = self.pre_attack_pos  # Snap to pre-attack position
                self.retreating = False  # Stop moving

    def idle(self, dt):
        player_pos, fly_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        move_vector = (player_pos + self.offset) - fly_pos
        if move_vector.length() != 0:
            self.direction = move_vector.normalize()
            self.rect.x += self.direction.x * self.speed * dt
            self.rect.y += self.direction.y * self.speed * dt
        
    def hit(self):
        if not self.timers['hit'].active:
            self.state = 'hit'
            self.health -= 1
            self.frame_index = 0
            self.timers['hit'].activate()
        if self.frame_index >= 2:
            if self.state != 'attack':
                self.state = 'attack'
                self.frame_index = 0
                self.timers['attack'].activate()

    def die(self):
        self.state = 'die'
        if self.state != 'die':
            self.frame_index = 0
        if self.frame_index >= 2:
            self.kill()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()
        self.state_management()

        # animate
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index) % int(len(self.frames[self.state]))]

        # move
        if self.state == 'attack':
            self.attack(dt, self.pre_attack_pos)
        if self.state == 'idle':
            self.idle(dt)
  