import pygame
from pygame.locals import *
import random

pygame.init()

# criando a janela do game
width = 500
heigth = 500
screen_size = (width, heigth)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# cores
gray = (100, 100, 100)
green = (76, 200, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# game assets
gameover = False
speed = 2
score = 0

# markers size
marker_width = 10
marker_heigth = 50

road = (100, 0, 300, heigth)
left_edge_marker = (95, 0, marker_width, heigth)
rigth_edge_marker = (395, 0, marker_width, heigth)

# lanes
left_lane = 150
center_lane = 250
rigth_lane = 350
lanes = [left_lane, center_lane, rigth_lane]

lane_marker_move_y = 0

class Veiculo(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_heigth = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_heigth))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class Player_Veiculo(Veiculo):
    def __init__(self, x, y):
        images = pygame.image.load('images/car.png')
        super().__init__(images, x, y)

player_x = 250
player_y = 400

# criando o carro do player
player_group = pygame.sprite.Group()
player = Player_Veiculo(player_x, player_y)
player_group.add(player)

# carregando os outros carros no cenário
images_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filenames in images_filenames:
    image = pygame.image.load('images/' + image_filenames)
    vehicle_images.append(image)

# sprite
vehicle_group = pygame.sprite.Group()

# carregando a imagem de colisão
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# loop do game
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # usando as setas para movimentar o carro do player
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < rigth_lane:
                player.rect.x += 100

        for vehicle in vehicle_group:
            if pygame.sprite.collide_rect(player, vehicle):
                gameover = True
                # determinando a posição da imagem de colisão
                if event.key == K_LEFT:
                    player.rect.left = vehicle.rect.right
                    crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                elif event.key == K_RIGHT:
                    player.rect.right = vehicle.rect.left
                    crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]

    # desenhando cenário
    screen.fill(green)

    # desenhando a rodovia
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, rigth_edge_marker)

    # desenhando as lanes
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_heigth * 2:
        lane_marker_move_y = 0

    for y in range(marker_heigth * -2, heigth, marker_heigth * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_heigth))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_heigth))

    # desenhando o carro do player
    player_group.draw(screen)

    # adicionando mais veículos
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            # selecionando uma lane aleatória
            lane = random.choice(lanes)

            # selecionando a imagem de um veículo aleatório
            image = random.choice(vehicle_images)
            vehicle = Veiculo(image, lane, heigth / -2)
            vehicle_group.add(vehicle)

    # fazendo os veículos se moverem
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        if vehicle.rect.top >= heigth:
            vehicle.kill()

            # adicionando o score
            score += 1

            # aumentando a velocidade ao passar 5 veículos
            if score > 0 and score % 5 == 0:
                speed += 1

    # desenhando os veículos
    vehicle_group.draw(screen)

    # score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)

    # verificar se houve colisão
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # display de game over
    if gameover:
        screen.blit(crash, crash_rect)
        pygame.draw.rect(screen, red, (0, 50, width, 100))

        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game Over. Jogar Novamente? (Pressione Y ou N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)

    pygame.display.update()

    # checar se o player quer jogar novamente
    while gameover:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                gameover = False
                running = False

            if event.type == KEYDOWN:
                if event.key == K_y:
                    # resetando o game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # saindo do loop
                    gameover = False
                    running = False

pygame.quit()