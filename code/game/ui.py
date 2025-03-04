from settings import *
from game.sprites import Sprite

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        # hearts
        self.heart_frames = frames['heart']

        # coins

    def create_hearts(self, num):
        for sprite in self.sprites:
            sprite.kill()
        for heart in range(num):
            x = 10 + heart * 40
            y = 10
            Heart((x,y), self.heart_frames['full'], self.sprites)

    def update(self, dt):
        self.sprites.update(dt)

    def render(self):
        self.sprites.draw(self.display_surface)

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frames = frames
        self.image = self.frames[0]  # Set the image to the first frame
        self.rect = self.image.get_rect(topleft=pos)  # Set the rect attribute
