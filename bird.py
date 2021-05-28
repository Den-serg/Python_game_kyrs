import random
from sounds import *
from bullet import *
from images import *


class Bird:
    def __init__(self, away_y):
        self.x = random.randrange(450, 730)
        self.y = away_y
        self.ay = away_y
        self.width = 55
        self.height = 105
        self.speed = 3
        self.dest_y = self.speed * random.randrange(20, 70)
        self.img_count = 0
        self.cd_hide = 0
        self.come = True
        self.go_away = False
        self.cd_shot = 0
        self.all_bullets = []

    def draw(self):
        if self.img_count == 30:
            self.img_count = 0

        display.blit(bird_img[self.img_count // 5], (self.x, self.y))
        self.img_count += 1

        if self.come and self.cd_hide == 0:
            return 1
        elif self.go_away:
            return 2
        elif self.cd_hide > 0:
            self.cd_hide -= 1

        return 0

    def show(self):
        if self.y < self.dest_y:
            self.y += self.speed
        else:
            self.come = False
            # self.go_away = True
            self.dest_y = self.ay

    def hide(self):
        if self.y > self.dest_y:
            self.y -= self.speed
        else:
            self.come = True
            self.go_away = False
            self.x = random.randrange(450, 730)
            self.dest_y = self.speed * random.randrange(20, 70)
            self.cd_hide = 80

    def check_dmg(self, bullet):
        if self.x < bullet.x <= self.x + self.width:
            if self.y < bullet.y <= self.y + self.height:
                self.go_away = True

    def shot(self):
        if not self.come:
            if not self.cd_shot:
                pygame.mixer.Sound.play(bullet_sound)

                new_bullet = Bullet(self.x, self.y)
                new_bullet.find_path(user_x + user_width // 2, user_y + user_height // 2)

                self.all_bullets.append(new_bullet)
                self.cd_shot = 200
            else:
                self.cd_shot -= 1

            for bullet in self.all_bullets:
                if not bullet.move_to(reverse=True):
                    self.all_bullets.remove(bullet)
