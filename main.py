import pygame
from player import Player, Coin
from functions import draw_text
import button
#Constans
pygame.init()
screen_width = 1280
screen_height = 720
font = pygame.font.SysFont('Futura', 30)
screen = pygame.display.set_mode((screen_width, screen_height))
FPS = 60
clock = pygame.time.Clock()
#States
run = True
moving_left = False
moving_right = False
game_paused = True
menu_state = 'main'
#Buttons
play_img = pygame.image.load("static/buttons/play.png").convert_alpha()
user_img = pygame.image.load("static/buttons/user.png").convert_alpha()
question_img = pygame.image.load("static/buttons/question.png").convert_alpha()
quit_img = pygame.image.load("static/buttons/quit.png").convert_alpha()
back_img = pygame.image.load("static/buttons/back.png").convert_alpha()
play_button = button.Button(250, 270, play_img, 0.25)
user_button = button.Button(450, 270, user_img, 0.25)
question_button = button.Button(650, 270, question_img, 0.25)
quit_button = button.Button(850, 270, quit_img, 0.25)
#Game stf
player = Player(500, 300, 0.1, 5)
coin = Coin(400, 200, player)
coin_group = pygame.sprite.Group()
coin_group.add(coin)
while run:
    clock.tick(FPS)
    screen.fill((123, 4, 5))
    player.draw(screen)
    player.move(moving_left, moving_right)
    coin_group.draw(screen)
    coin_group.update()
    draw_text(screen, 'COIN: ', font, (255, 255, 255), 10, 35)
    draw_text(screen, str(player.coin), font, (255, 255, 255), 100, 35)
    if game_paused == True:
        screen.fill((117, 214, 255))
        if menu_state == 'main':
            if play_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                run = False
            if user_button.draw(screen):
                menu_state = 'user'
            if question_button.draw(screen):
                menu_state = 'question'
        if menu_state == 'question':
            draw_text(screen, 'A - влево, D - вправо, W - прыжок, Esc - пауза',
                      font, (0, 0, 0), 400, 300)
            back_button = button.Button(900, 250, back_img, 0.2)
            if back_button.draw(screen):
                menu_state = 'main'

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                game_paused = True
                menu_state = 'main'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
    pygame.display.update()
pygame.quit()
