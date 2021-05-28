import pygame
import parameters as p
from images import light_img


# Для шрифта
def print_text(message, x, y, font_color=(0, 0, 0), font_type='Effect/PingPong.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    p.display.blit(text, (x, y))


def draw_mouse():
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    mouse_size = [10, 12, 16, 20, 28, 34, 40, 45, 48, 54, 58]

    if click[0] or click[1]:
        p.need_draw_click = True

    if p.need_draw_click:
        draw_x = mouse[0] - mouse_size[p.mouse_count] // 2
        draw_y = mouse[1] - mouse_size[p.mouse_count] // 2

        p.display.blit(light_img[p.mouse_count], (draw_x, draw_y))
        p.mouse_count += 1

        if p.mouse_count == 10:
            p.mouse_count = 0
            p.need_draw_click = False
