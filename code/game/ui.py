from constants import *
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

        # bar
        self.bar_frames = frames['bar']
        self.bar_sprites = pygame.sprite.Group()
        self.bar_width = 2

    def create_hearts(self, max_health, health):
        for sprite in self.heart_sprites:
            sprite.kill()
        for heart in range(max_health):
            if heart < health:
                x = 10 + heart * 40
                y = 10
                Heart((x,y), self.heart_frames['full'], (self.sprites, self.heart_sprites))
            else:
                x = 10 + heart * 40
                y = 10
                Heart((x,y), self.heart_frames['empty'], (self.sprites, self.heart_sprites))

    def create_diamond(self, value):
        for sprite in self.diamond_sprites:
            sprite.kill()
        if value == True:
            Diamond((1207, 33), self.diamond_frames['full'], (self.sprites, self.diamond_sprites))
        else:
            Diamond((1207, 33), self.diamond_frames['empty'], (self.sprites, self.diamond_sprites))

    def create_bar(self, time):
        self.bg_bar = pygame.sprite.Sprite(self.sprites)
        self.bg_bar.image = self.bar_frames['bg'][0]
        self.bg_bar.rect = self.bg_bar.image.get_rect(topleft=(1070, 15))
        for sprite in self.bar_sprites:
            sprite.kill()
        Bar((1074, 15), self.bar_frames['segment'][0], (self.sprites, self.bar_sprites), time)

    def create_timer(self, time):
        self.secs = int(time / 1000) % 60
        self.mins = int(time / 60000)
        self.text_surf = self.font.render(f"{self.mins:02}:{self.secs:02}", False, (224, 236, 212))
        self.text_rect = self.text_surf.get_frect(topleft=(10, 45))

    def update(self, dt):
        self.sprites.update(dt)

    def render(self):
        self.sprites.draw(self.display_surface)
        self.display_surface.blit(self.text_surf, self.text_rect)

class Heart(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image[0]
        self.rect = self.image.get_rect(topleft=pos)

class Diamond(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image[0]
        self.rect = self.image.get_rect(topleft=pos)

class Bar(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, time):
        super().__init__(groups)
        self.sprites, self.bar_sprites = groups

        self.bar_width = time / 5000 * 192
        self.image = pygame.transform.scale(image,(self.bar_width, 32))
        self.rect = self.image.get_rect(topleft=pos)