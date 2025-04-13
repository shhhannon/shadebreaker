from constants import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.width, self.height = width, height
        self.borders = {
            'left': 0,
            'right': -self.width + WINDOW_WIDTH,
            'top': 0,
            'bottom': -self.height + WINDOW_HEIGHT
        }

    def camera_constraint(self):
        self.offset.x = min(self.offset.x, self.borders['left'])
        self.offset.x = max(self.offset.x, self.borders['right'])
        self.offset.y = max(self.offset.y, self.borders['bottom'])

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        self.camera_constraint()

        for sprite in sorted(self, key = lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf = pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = None, z = Z_LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()
        self.z = z


class Item(Sprite):
    def __init__(self, item_type, pos, frames, groups, data, animation_speed = ANIMATION_SPEED):
        self.frames, self.frame_index = frames, 0
        super().__init__(pos, self.frames[self.frame_index], groups, z = Z_LAYERS['main'])
        self.animation_speed = animation_speed/1.5
        self.rect.center = pos
        self.item_type = item_type
        self.data = data

    def activate(self):
        if self.item_type == 'potion':
            for health in range(2):
                if self.data.health < self.data.max_health:
                    self.data.health += 1
        if self.item_type == 'silver':
            self.data.coins += 1
        if self.item_type == 'diamond':
            self.data.has_diamond = True
    
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dt):
        self.animate(dt)