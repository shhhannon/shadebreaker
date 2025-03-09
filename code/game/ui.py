from settings import *
from game.sprites import Sprite

class UI:
    def __init__(self, font, frames):
        self.display_surface = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font

        # hearts
        self.heart_frames = frames['heart']
        self.heart_sprites = pygame.sprite.Group()

        # diamonds
        self.diamond_frames = frames['diamond']
        self.diamond_sprites = pygame.sprite.Group()

        # coins ???

    def create_hearts(self, max_health, health):
        for sprite in self.heart_sprites:
            sprite.kill()
        for heart in range(max_health):
            if heart < health:
                x = 10 + heart * 40
                y = 10
                Heart((x,y), self.heart_frames['full'], (self.sprites, self.heart_sprites))
            else:
                x = x = 10 + heart * 40
                y = 10
                Heart((x,y), self.heart_frames['empty'], (self.sprites, self.heart_sprites))

    def create_diamond(self, value):
        for sprite in self.diamond_sprites:
            sprite.kill()
        if value == True:
            Diamond((1205, -12), self.diamond_frames['full'], (self.sprites, self.diamond_sprites))
        else:
            Diamond((1205, -12), self.diamond_frames['empty'], (self.sprites, self.diamond_sprites))
              

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

class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(*groups)
        self.frames = frames
        self.image = self.frames[1]  # Set the image to the first frame
        self.rect = self.image.get_rect(topleft=pos)  # Set the rect attribute