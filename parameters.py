import pygame

# Display
display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))

# persona
user_width = 60
user_height = 100
user_x = display_width // 3
user_y = display_height - user_height - 100

# fps
clock = pygame.time.Clock()

# Для визуализиции откликов
mouse_count = 0
need_draw_click = False
