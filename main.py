import pygame
from player import Player

pygame.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
run = True

player = Player(500, 500, 0.1)
while run:
    screen.blit(player.img, player.rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
