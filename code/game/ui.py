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

        # bar
        self.bar_frames = frames['bar']
        self.bar_sprites = pygame.sprite.Group()
        self.bar_rect = None # self.bar_frames['bg'][0].get_rect(topleft=(1070, 15))
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

    def create_bar(self, timer):
        self.change_timer = timer
        self.bg_bar = pygame.sprite.Sprite(self.sprites)
        self.bg_bar.image = self.bar_frames['bg'][0]
        self.bg_bar.rect = self.bg_bar.image.get_rect(topleft=(1070, 15))
        for sprite in self.bar_sprites:
            sprite.kill()
        if not self.change_timer.active:
            print('full')
            Bar((1070, 15), self.bar_frames['segment'][0], (self.sprites, self.bar_sprites), 20000)
        else:
            #Bar((1070, 15), self.bar_frames['segment'][0], (self.sprites, self.bar_sprites), timer)
            pass

    def update(self, dt):
        self.sprites.update(dt)

    def render(self):
        self.sprites.draw(self.display_surface)

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
    def __init__(self, pos, image, groups, timer):
        super().__init__(groups)
        self.image = image
        #self.change_timer = timer
        self.bar_width = timer / 20000 * 200
        self.bar = pygame.transform.scale(self.image,(self.bar_width, 32))
        self.rect = self.bar.get_rect(topleft=(560, 360))