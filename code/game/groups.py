from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE
        self.borders = {
            'left': 0,
            'right': -self.width + WINDOW_WIDTH,
            'top': 0,
            'bottom': self.height
        }

    def camera_constraint(self):
        self.offset.x = min(self.offset.x, self.borders['left'])
        self.offset.x = max(self.offset.x, self.borders['right'])

    def draw(self, target_pos):
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        self.camera_constraint()

        for sprite in sorted(self, key = lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image, offset_pos)