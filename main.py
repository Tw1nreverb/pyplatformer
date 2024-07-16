import pygame
from player import Player, Coin
from functions import draw_text
import button
import inputbox
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
#input boxes
login_input_box = inputbox.InputBox(550, 300, 140, 32)
password_input_box = inputbox.InputBox(550, 350, 140, 32)
login_input_box1 = inputbox.InputBox(550, 300, 140, 32)
password_input_box1 = inputbox.InputBox(550, 350, 140, 32)
input_boxes = [login_input_box, password_input_box]
input_registration_boxes = [login_input_box1, password_input_box1]
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
                menu_state = 'login'
            if question_button.draw(screen):
                menu_state = 'question'
        if menu_state == 'question':
            draw_text(screen, 'A - влево, D - вправо, W - прыжок, Esc - пауза',
                      font, (0, 0, 0), 400, 300)
            back_button = button.Button(1000, 250, back_img, 0.2)
            if back_button.draw(screen):
                menu_state = 'main'
        if menu_state == 'login':
            draw_text(screen, "Зайдите в систему", font, (0, 0, 0), 557, 250)
            accept_img = pygame.image.load(
                "static/buttons/accept.png").convert_alpha()
            accept_button = button.Button(780, 280, accept_img, 0.2)
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw(screen)
            if accept_button.draw(screen):
                pass
            draw_text(screen, "Если у вас нет аккаунта, нажмите сюда -", font,
                      (0, 0, 0), 450, 450)
            sign_up_img = pygame.image.load(
                "static/buttons/signup.png").convert_alpha()
            sign_up_button = button.Button(865, 445, sign_up_img, 0.1)
            if sign_up_button.draw(screen):
                menu_state = 'registration'
        if menu_state == 'registration':
            draw_text(screen, "Зарегестрируйтесь", font, (0, 0, 0), 557, 250)
            accept_img = pygame.image.load(
                "static/buttons/accept.png").convert_alpha()
            accept_button = button.Button(780, 280, accept_img, 0.2)
            for box in input_registration_boxes:
                box.update()
            for box in input_registration_boxes:
                box.draw(screen)
            if accept_button.draw(screen):
                pass

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
        if menu_state == 'login':
            for box in input_boxes:
                box.handle_event(event)
        if menu_state == 'registration':
            for box in input_registration_boxes:
                box.handle_event(event)
    pygame.display.update()
pygame.quit()
