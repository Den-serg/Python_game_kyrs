import parameters as p
from button import *
from bird import *
from object import *
from effects import *
import images as img
from states import *
from save import *


class Game:
    def __init__(self):
        pygame.display.set_caption("Dragon Run!")
        pygame.display.set_icon(icon)

        self.cactus_options = [69, 449, 37, 410, 40, 420]
        # Кол-во жизней
        self.health = 2
        self.img_counter = 0
        # Jump
        self.make_jump = False
        self.jump_counter = 30
        # Для счета
        self.scores = 0
        self.max_scores = 0
        self.max_above = 0
        # Для пуль
        self.cool_down = 0
        # состояния
        self.game_state = GameState()
        # для сохранения
        self.save_data = Save()
        self.land = 0
        self.pers = 0
        self.level = 1

    def start(self):
        while True:
            if self.game_state.check(State.MENU):
                self.show_menu()
            elif self.game_state.check(State.START):
                self.choose_theme()
                self.choose_hero()
                self.start_game()
            elif self.game_state.check(State.CONTINUE):
                self.max_scores = self.save_data.get('max')
                set_theme(self.save_data.get('fon'))
                set_hero(self.save_data.get('dino'))
                self.start_game()
            elif self.game_state.check(State.LEVEL_2):
                self.level_2()
            elif self.game_state.check(State.QUIT):
                self.save_data.save()
                self.save_data.add('max', self.max_scores)
                self.save_data.add('fon', self.land)
                self.save_data.add('dino', self.pers)
                break

    def choose_theme(self):
        theme1 = Button(250, 70)
        theme2 = Button(300, 70)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill((0, 255, 255))

            if theme1.draw(270, 200, 'Day theme', font_size=50):
                set_theme(1)
                self.land = 1
                return
            if theme2.draw(270, 300, 'Night theme', font_size=50):
                set_theme(2)
                self.land = 2
                return

            pygame.display.update()
            clock.tick(60)

    def choose_hero(self):
        hero1 = Button(190, 70)
        hero2 = Button(170, 70)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill((0, 255, 255))

            if hero1.draw(270, 200, 'Orange', font_size=50):
                set_hero(1)
                self.pers = 1
                return
            if hero2.draw(270, 300, 'Purple', font_size=50):
                set_hero(2)
                self.pers = 2
                return

            pygame.display.update()
            clock.tick(60)

    def level_2(self):
        pygame.mixer.music.load('Music/background.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        game = True
        cactus_mas = []
        self.create_cactus_mas(cactus_mas)

        stone, cloud = self.open_random_objects(stone_img, cloud_img)
        heart = Object(display_width, 280, 30, health_img, 4)

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # Jump
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if keys[pygame.K_SPACE]:
                self.make_jump = True

            if self.make_jump:
                self.jump()

            self.count_score(cactus_mas)

            display.blit(img.land_lvl2, (0, 0))

            print_text("Scores: " + str(self.scores), 600, 10)

            self.draw_array(cactus_mas)
            self.move_objects(stone, cloud)

            self.draw_dino()

            if keys[pygame.K_ESCAPE]:
                self.pause()

            heart.move()
            self.hearts_plus(heart)

            if self.check_collision(cactus_mas):
                pygame.mixer.music.stop()
                game = False

            self.show_health()

            draw_mouse()
            pygame.display.update()
            clock.tick(60)
        return self.game_over()

    def show_menu(self):
        menu_bckrg = pygame.image.load('Locations/Menu.jpg')

        pygame.mixer.music.load('Music/Big_Slinker.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        start_but = Button(288, 70)
        continue_but = Button(222, 70)
        lvl2_but = Button(170, 70)
        quit_but = Button(120, 70)

        show = True

        while show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.blit(menu_bckrg, (0, 0))
            if start_but.draw(270, 200, 'Start game', font_size=50):
                self.game_state.change(State.START)
                return
            if lvl2_but.draw(320, 300, 'Level 2', font_size=50):
                self.game_state.change(State.LEVEL_2)
                return
            if continue_but.draw(300, 400, 'Continue', font_size=50):
                self.game_state.change(State.CONTINUE)
                return
            if quit_but.draw(358, 500, 'Quit', quit, font_size=50):
                self.game_state.change(State.QUIT)
                return

            draw_mouse()

            pygame.display.update()
            clock.tick(60)

    def start_game(self):

        while self.game_cycle():
            self.scores = 0
            self.make_jump = False
            self.jump_counter = 30
            p.user_y = p.display_height - p.user_height - 100
            self.health = 2
            self.cool_down = 0

    def game_cycle(self):
        pygame.mixer.music.load('Music/background.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        game = True
        cactus_mas = []
        self.create_cactus_mas(cactus_mas)

        stone, cloud = self.open_random_objects(stone_img, cloud_img)
        heart = Object(display_width, 280, 30, health_img, 4)

        all_bullets = []
        all_mas_bullets = []

        bird1 = Bird(-80)
        bird2 = Bird(-70)

        all_birds = [bird1, bird2]

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # Jump
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if keys[pygame.K_SPACE]:
                self.make_jump = True

            if self.make_jump:
                self.jump()

            self.count_score(cactus_mas)

            display.blit(img.land, (0, 0))

            print_text("Scores: " + str(self.scores), 600, 10)

            self.draw_array(cactus_mas)
            self.move_objects(stone, cloud)

            self.draw_dino()

            if keys[pygame.K_ESCAPE]:
                self.pause()

            if not self.cool_down:
                if keys[pygame.K_x]:
                    pygame.mixer.Sound.play(bullet_sound)
                    all_bullets.append(Bullet(p.user_x + p.user_width, p.user_y + 26))
                    self.cool_down = 50
                elif click[0]:
                    pygame.mixer.Sound.play(bullet_sound)
                    add_bullet = Bullet(p.user_x + p.user_width, p.user_y + 26)
                    add_bullet.find_path(mouse[0], mouse[1])

                    all_mas_bullets.append(add_bullet)
                    self.cool_down = 50

            else:
                print_text('Cool down time:' + str(self.cool_down // 10), 482, 40)
                self.cool_down -= 1

            for bullet in all_bullets:
                if not bullet.move():
                    all_bullets.remove(bullet)

            for bullet in all_mas_bullets:
                if not bullet.move_to():
                    all_mas_bullets.remove(bullet)

            heart.move()
            self.hearts_plus(heart)

            if self.check_collision(cactus_mas):
                pygame.mixer.music.stop()
                game = False

            self.show_health()

            self.draw_birds(all_birds)
            self.check_birds_dmg(all_mas_bullets, all_birds)

            draw_mouse()
            pygame.display.update()
            clock.tick(60)
        return self.game_over()

    def jump(self):
        if self.jump_counter >= -30:
            if self.jump_counter == 30:
                pygame.mixer.Sound.play(jump_sound)
            if self.jump_counter == -25:  # Задержки в музыке
                pygame.mixer.Sound.play(fall_sound)

            p.user_y -= self.jump_counter / 2.5
            self.jump_counter -= 1
        else:
            self.jump_counter = 30
            self.make_jump = False

    # Create Cactus
    def create_cactus_mas(self, array):
        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]
        array.append(Object(display_width + 20, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]
        array.append(Object(display_width + 300, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]
        array.append(Object(display_width + 600, height, width, img, 4))

    # Ищет Кактус
    @staticmethod
    def find_radius(array):
        maximum = max(array[0].x, array[1].x, array[2].x)

        if maximum < display_width:
            radius = display_width
            if radius - maximum < 50:
                radius += 280
        else:
            radius = maximum

        choice = random.randrange(0, 9)
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(250, 400)

        return radius

    # Рисуем массив кактусов
    def draw_array(self, array):
        for cactus in array:
            check = cactus.move()
            if not check:
                self.object_return(array, cactus)

    def object_return(self, objects, obj):
        radius = self.find_radius(objects)

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]

        obj.return_self(radius, height, width, img)

    # Рисуем облака и камки
    @staticmethod
    def open_random_objects(stone, cloud):
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]

        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]

        stone = Object(display_width, display_height - 75, 10, img_of_stone, 4)
        cloud = Object(display_width, 80, 70, img_of_cloud, 2)

        return stone, cloud

    @staticmethod
    def move_objects(stone, cloud):
        check = stone.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_stone = stone_img[choice]
            stone.return_self(p.display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

        check = cloud.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_cloud = cloud_img[choice]
            cloud.return_self(p.display_width, random.randrange(10, 200), stone.width, img_of_cloud)

    # Прорисока главного перса
    def draw_dino(self):
        if self.img_counter == 25:
            self.img_counter = 0

        display.blit(img.dino_img[self.img_counter // 5], (p.user_x, p.user_y))
        self.img_counter += 1

    @staticmethod
    def pause():
        paused = True
        pygame.mixer.music.pause()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text('Paused. Press ENTER to continue', 160, 300)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                paused = False

            pygame.display.update()
            clock.tick(15)

        pygame.mixer.music.unpause()

    def check_collision(self, barriers):
        for barrier in barriers:
            if barrier.y == 449:  # Встреча с маленьким кактусом
                if not self.make_jump:
                    if barrier.x <= p.user_x + p.user_width - 25 <= barrier.x + barrier.width:
                        if self.check_health():
                            self.object_return(barriers, barrier)
                            return False
                        else:
                            return True
                elif self.jump_counter >= 0:
                    if p.user_y + p.user_height - 5 >= barrier.y:
                        if barrier.x <= p.user_x + p.user_width - 35 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                else:
                    if p.user_y + p.user_height - 10 >= barrier.y:
                        if barrier.x <= p.user_x <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
            else:
                if not self.make_jump:
                    if barrier.x <= p.user_x + p.user_width - 2 <= barrier.x + barrier.width:
                        if self.check_health():
                            self.object_return(barriers, barrier)
                            return False
                        else:
                            return True
                elif self.jump_counter >= 10:
                    if p.user_y + p.user_height - 5 >= barrier.y:
                        if barrier.x <= p.user_x + p.user_width - 5 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                elif self.jump_counter >= -1:
                    if p.user_y + p.user_height - 5 >= barrier.y:
                        if barrier.x <= p.user_x + p.user_width - 35 <= barrier.x + barrier.width:
                            if self.check_health():
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                    else:
                        if p.user_y + p.user_height - 8 >= barrier.y:
                            if barrier.x <= p.user_x + 5 <= barrier.x + barrier.width:
                                if self.check_health():
                                    self.object_return(barriers, barrier)
                                    return False
                                else:
                                    return True
        return False

    def count_score(self, barriers):
        above_cactus = 0

        if -20 <= self.jump_counter < 25:
            for barrier in barriers:
                if p.user_y + p.user_height - 5 <= barrier.y:
                    if barrier.x <= p.user_x <= barrier.x + barrier.width:
                        above_cactus += 1
                    elif barrier.x <= p.user_x + p.user_width <= barrier.x + barrier.width:
                        above_cactus += 1

            self.max_above = max(self.max_above, above_cactus)
        else:
            if self.jump_counter == -30:
                self.scores += self.max_above
                self.max_above = 0

    def game_over(self):
        if self.scores > self.max_scores:
            self.max_scores = self.scores

        stopped = True
        while stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text('Game over. Press ENTER to play game again, ESC to exit', 0, 300)
            print_text('Max score: ' + str(self.max_scores), 300, 350)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                return True
            if keys[pygame.K_ESCAPE]:
                self.game_state.change(State.QUIT)
                return False

            pygame.display.update()
            clock.tick(15)

    def show_health(self):
        show = 0
        x = 20
        while show != self.health:
            display.blit(health_img, (x, 20))
            x += 40
            show += 1

    def check_health(self):
        self.health -= 1
        if self.health == 0:
            pygame.mixer.Sound.play(loss_sound)
            return False
        else:
            pygame.mixer.Sound.play(fall_sound)
            return True

    def hearts_plus(self, heart):

        if heart.x <= -heart.width:
            radius = p.display_width + random.randrange(1000, 3000)
            heart.return_self(radius, heart.y, heart.width, heart.image)

        if p.user_x <= heart.x <= p.user_x + p.user_width:
            if p.user_y <= heart.y <= p.user_y + p.user_height:
                pygame.mixer.Sound.play(heart_plus_sound)
                if self.health < 5:
                    self.health += 1

                radius = p.display_width + random.randrange(500, 3000)
                heart.return_self(radius, heart.y, heart.width, heart.image)

    @staticmethod
    def draw_birds(birds):
        for bird in birds:
            action = bird.draw()
            if action == 1:
                bird.show()
            elif action == 2:
                bird.hide()
            else:
                bird.shot()

    @staticmethod
    def check_birds_dmg(bullets, birds):
        for bird in birds:
            for bullet in bullets:
                bird.check_dmg(bullet)
