import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, scale, speed):
        super().__init__()
        img = pygame.image.load('static/player.png')
        self.img = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.flip = False
        self.direction = 1

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = 1
        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = -1
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False),
                    self.rect)
