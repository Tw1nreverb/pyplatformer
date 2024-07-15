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
        self.coin = 0
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


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y, player):
        super().__init__()
        self.player = player
        self.image = pygame.image.load('static/coin.png')
        self.image = pygame.transform.scale(self.image, (int(
            self.image.get_width() * 0.1), int(self.image.get_height() * 0.1)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 50 // 2, y + (50 - self.image.get_height()))

    def update(self):
        if pygame.sprite.collide_rect(self, self.player):
            self.player.coin += 1
            self.kill()
