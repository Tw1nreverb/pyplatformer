import pygame

gravity = 0.75


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
        self.jump = False
        self.life = True
        self.vel_y = 0
        self.in_air = False

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
        if self.jump == True and not (self.in_air):
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy += int(self.vel_y)
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False),
                    self.rect)
