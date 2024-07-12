import pygame
from player import Player

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
FPS = 60
clock = pygame.time.Clock()
run = True
moving_left = False
moving_right = False
player = Player(500, 300, 0.1, 5)
while run:
    clock.tick(FPS)
    screen.fill((123, 4, 5))
    player.draw(screen)
    player.move(moving_left, moving_right)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
    pygame.display.update()
pygame.quit()
