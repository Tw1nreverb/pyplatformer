import pygame
from functions import draw_text
import button
import inputbox
from database.db import add_stats, check_coins, register_user, login_user
import csv
#Constans
pygame.init()
gravity = 0.45
scroll_thresh = 200
screen_scroll = 0
bg_scroll = 0
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
game_paused = True
menu_state = 'main'
level = 0
max_levels = 1


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
        self.level_complete = False
        self.vel_y = 0
        self.in_air = False
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def move(self, moving_left, moving_right):
        screen_scroll = 0
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
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width,
                                   self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width,
                                   self.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.right > screen_width - scroll_thresh or self.rect.left < scroll_thresh:
            self.rect.x -= dx
            screen_scroll = -dx
        return screen_scroll

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.img, self.flip, False),
                    self.rect)


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y, player):
        super().__init__()
        self.player = player
        self.image = pygame.image.load('static/coin.png')
        self.image = pygame.transform.scale(self.image, (int(
            self.image.get_width() * 1), int(self.image.get_height() * 1)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 50 // 2, y + (50 - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, self.player):
            self.player.coin += 1
            self.kill()


pygame.display.set_caption("Summer Practice platformer")
ROWS = 16
COLS = 150
TILE_TYPES = 18
TILE_SIZE = screen_height // ROWS
font = pygame.font.SysFont('Futura', 30)
FPS = 60
pine1_img = pygame.image.load('static/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('static/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load(
    'static/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('static/background/sky_cloud.png').convert_alpha()


def draw_bg():
    screen.fill((117, 214, 255))
    screen.blit(sky_img, (0, 0))
    screen.blit(mountain_img,
                (0, screen_height - mountain_img.get_height() - 300))
    screen.blit(pine1_img, (0, screen_height - pine1_img.get_height() - 150))
    screen.blit(pine2_img, (0, screen_height - pine2_img.get_height()))


clock = pygame.time.Clock()
#tile list
tile_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'static/tile/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tile_list.append(img)
#States
run = True
moving_left = False
moving_right = False
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
game_id = 1


class World:

    def __init__(self) -> None:
        self.obstacle_list = []

    def process_data(self, data):
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = tile_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile > 11 and tile <= 14:
                        decoration = Decoration(img, x * TILE_SIZE,
                                                y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        coin = Coin(x * TILE_SIZE, y * TILE_SIZE, player)
                        coin_group.add(coin)
                    elif tile == 16:
                        pass
                    elif tile == 17:
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

    def clear(self):
        self.obstacle_list = []

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])


class Water(pygame.sprite.Sprite):

    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2,
                            y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Decoration(pygame.sprite.Sprite):

    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2,
                            y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Exit(pygame.sprite.Sprite):

    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2,
                            y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(player, self):
            player.level_complete = True


decoration_group = pygame.sprite.Group()
player = Player(500, 300, 1.5, 5)
coin_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
#input boxes
login_input_box = inputbox.InputBox(550, 300, 140, 32)
password_input_box = inputbox.InputBox(550, 350, 140, 32)
login_input_box1 = inputbox.InputBox(550, 300, 140, 32)
password_input_box1 = inputbox.InputBox(550, 350, 140, 32)
input_boxes = [login_input_box, password_input_box]
input_registration_boxes = [login_input_box1, password_input_box1]
#login
is_login = False
#world data
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
world.process_data(world_data)


def reset_level():
    coin_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    #create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


while run:
    clock.tick(FPS)
    draw_bg()
    if level > max_levels:
        game_paused = True
        menu_state = 'End'
    exit_group.update()
    exit_group.draw(screen)
    if player.level_complete:
        level += 1
        world_data = reset_level()
        if level <= max_levels:
            with open(f'level{1}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            world.process_data(world_data)
            player.rect.x = 100
            screen_scroll = 0
            player.level_complete = False
    if player.rect.y > 1000:
        world_data = reset_level()
        if is_login:
            add_stats(input_boxes[0].text, player.coin, game_id)
            game_id = game_id + 1
        else:
            pass
        if level <= max_levels:
            with open(f'level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            world.process_data(world_data)
            player.rect.y = 300
            menu_state = 'main'
            game_paused = True
    world.draw()
    player.draw(screen)
    screen_scroll = player.move(moving_left, moving_right)
    coin_group.draw(screen)
    coin_group.update()
    water_group.draw(screen)
    water_group.update()
    decoration_group.draw(screen)
    decoration_group.update()
    draw_text(screen, 'COIN: ', font, (255, 255, 255), 10, 35)
    draw_text(screen, str(player.coin), font, (255, 255, 255), 100, 35)

    if game_paused == True:
        screen.fill((117, 214, 255))
        if menu_state == 'main':
            if play_button.draw(screen):
                player.rect.x = 500
                player.rect.y = 300
                player.coin = 0
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
        if menu_state == 'login' and not (is_login):
            draw_text(screen, "Зайдите в систему", font, (0, 0, 0), 557, 250)
            accept_img = pygame.image.load(
                "static/buttons/accept.png").convert_alpha()
            accept_button = button.Button(780, 280, accept_img, 0.2)
            for box in input_boxes:
                box.update()
            for box in input_boxes:
                box.draw(screen)
            if accept_button.draw(screen):
                if login_user(input_boxes[0].text, input_boxes[1].text):
                    menu_state = 'main'
                    is_login = True
            draw_text(screen, "Если у вас нет аккаунта, нажмите сюда -", font,
                      (0, 0, 0), 450, 450)
            sign_up_img = pygame.image.load(
                "static/buttons/signup.png").convert_alpha()
            sign_up_button = button.Button(865, 445, sign_up_img, 0.1)
            if sign_up_button.draw(screen):
                menu_state = 'registration'
        if menu_state == 'login' and is_login:
            if input_boxes[0]:
                draw_text(screen, "Ваше имя: " + input_boxes[0].text, font,
                          (0, 0, 0), 200, 200)
            stats = check_coins(input_boxes[0].text)
            draw_text(screen, "Ваша статистика:", font, (0, 0, 0), 200, 300)
            for i in range(len(stats)):
                draw_text(
                    screen,
                    f"Игра: {stats[i][0]}, Количество монет:{stats[i][1]} ",
                    font, (0, 0, 0), 200, 400 + i * 50)
            back_button = button.Button(1000, 250, back_img, 0.2)

            if back_button.draw(screen):
                menu_state = 'main'
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
                if register_user(input_registration_boxes[0].text,
                                 input_registration_boxes[1].text):
                    menu_state = 'login'
        if menu_state == 'End':
            draw_text(screen, "Пока что на этом все", font, (0, 0, 0), 557,
                      250)
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
