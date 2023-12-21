import pygame
import sys
import math

pygame.init()

window_size = (501, 501)

white = (255, 255, 255)
red = (255, 0, 0)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Послать круг")

font = pygame.font.Font(None, 36)

circle_radius = 20
circle_x, circle_y = window_size[0] // 2, window_size[1] // 2

target_x, target_y = 0, 0

speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            target_x, target_y = event.pos

    angle = math.atan2(target_y - circle_y, target_x - circle_x)
    circle_x += speed * math.cos(angle)
    circle_y += speed * math.sin(angle)

    screen.fill(white)

    pygame.draw.circle(screen, red, (int(circle_x), int(circle_y)), circle_radius)

    pygame.display.flip()

    pygame.time.Clock().tick(30)
