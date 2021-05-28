import pygame

pygame.init()

# Иконка
icon = pygame.image.load('Locations/icon.png')

# Земля
land = pygame.image.load('Locations/Land1.jpg')
land_lvl2 = pygame.image.load('Locations/LandLevel.jpg')

# Массив для изображений кактусов
cactus_img = [pygame.image.load('Objects/Cactus0.png'), pygame.image.load('Objects/Cactus1.png'), pygame.image.load('Objects/Cactus2.png')]

# Массив для изображение камней
stone_img = [pygame.image.load('Objects/Stone0.png'), pygame.image.load('Objects/Stone1.png')]

# Массив изображений для облаков
cloud_img = [pygame.image.load('Objects/Cloud0.png'), pygame.image.load('Objects/Cloud1.png')]

# Массив анимаций главного персонажа
dino_img = [pygame.image.load('Dino/Dino0.png'), pygame.image.load('Dino/Dino1.png'), pygame.image.load('Dino/Dino2.png'),
            pygame.image.load('Dino/Dino3.png'), pygame.image.load('Dino/Dino4.png')]

# Массив анимаций Врагов
bird_img = [pygame.image.load('Bird/Bird0.png'), pygame.image.load('Bird/Bird1.png'), pygame.image.load('Bird/Bird2.png'),
            pygame.image.load('Bird/Bird3.png'), pygame.image.load('Bird/Bird4.png'), pygame.image.load('Bird/Bird5.png')]

# Для красоты
light_img = [pygame.image.load('Effect/Light0.png'), pygame.image.load('Effect/Light1.png'), pygame.image.load('Effect/Light2.png'),
             pygame.image.load('Effect/Light3.png'), pygame.image.load('Effect/Light4.png'), pygame.image.load('Effect/Light5.png'),
             pygame.image.load('Effect/Light6.png'), pygame.image.load('Effect/Light7.png'), pygame.image.load('Effect/Light8.png'),
             pygame.image.load('Effect/Light9.png'), pygame.image.load('Effect/Light10.png')]

# Иконки жизней
health_img = pygame.image.load('Effect/heart.png')
health_img = pygame.transform.scale(health_img, (30, 30))

# Иконка выстрела
bullet_img = pygame.image.load('Effect/shot.png')
bullet_img = pygame.transform.scale(bullet_img, (30, 9))


def set_theme(num):
    global land
    land = pygame.image.load('Locations/Land{}.jpg'.format(num))
    return num


def set_hero(num):
    global dino_img

    if num == 1:
        dino_img = [pygame.image.load('Dino/Dino0.png'), pygame.image.load('Dino/Dino1.png'), pygame.image.load('Dino/Dino2.png'),
                    pygame.image.load('Dino/Dino3.png'), pygame.image.load('Dino/Dino4.png')]
    else:
        dino_img = [pygame.image.load('Dino/Dino2_0.png'), pygame.image.load('Dino/Dino2_1.png'), pygame.image.load('Dino/Dino2_2.png'),
                    pygame.image.load('Dino/Dino2_3.png'), pygame.image.load('Dino/Dino2_4.png')]
