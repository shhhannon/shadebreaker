from settings import *

#use file to edit enemies.py to make use of OOP more

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups, z = Z_LAYERS['main'], animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed/1.5

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.animate(dt)

class Item(AnimatedSprite):
    def __init__(self, item_type, pos, frames, groups, data):
        super().__init__(pos, frames, groups)
        self.rect.center = pos
        self.item_type = item_type
        self.data = data

    def activate(self):
        if self.item_type == 'potion':
            for health in range(3):
                if self.data.health < self.data.max_health:
                    self.data.health += 1
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'diamond':
            self.data.has_diamond = True