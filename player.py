import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, scale):
        super().__init__()
        img = pygame.image.load('static/player.png')
        self.img = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = img.get_rect()
        self.rect.center = (x, y)
