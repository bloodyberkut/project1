import pygame
from random import randrange

WIDTH, HEIGHT = 1200, 800
fps = 60

platform_weight = 275
platform_height = 25
platform_speed = 7
platform = pygame.Rect(WIDTH // 2 - platform_weight // 2, HEIGHT - platform_height - 10, platform_weight, platform_height)

ball_radius = 15
ball_speed = 5
ball_rect = int(ball_radius * 2 ** 0.2)
ball = pygame.Rect(randrange(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
ball_x, ball_y = 1, -1

blocks = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
block_color = [(randrange(10, 255 + 1), randrange(10, 255 + 1), randrange(10, 255 + 1))for i in range(10) for j in range(4)]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("scape.jpg").convert()


def detect_collision(ball_x, ball_y, ball, rect):
    if ball_x > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if ball_y > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        ball_x, ball_y = -ball_x, -ball_y
    elif delta_x > delta_y:
        ball_y = -ball_y
    elif delta_y > delta_x:
        ball_x = -ball_x
    return ball_x, ball_y


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.blit(background, (0, 0))
    [pygame.draw.rect(screen, block_color[color], block) for color, block in enumerate(blocks)]
    pygame.draw.rect(screen, pygame.Color('red'), platform)
    pygame.draw.circle(screen, pygame.Color('white'), ball.center, ball_radius)
    ball.x += ball_speed * ball_x
    ball.y += ball_speed * ball_y
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        ball_x = -ball_x
    if ball.centery < ball_radius:
        ball_y = -ball_y
    if ball.colliderect(platform) and ball_y > 0:
        ball_x, ball_y = detect_collision(ball_x, ball_y, ball, platform)

    coll = ball.collidelist(blocks)
    if coll != -1:
        coll_rect = blocks.pop(coll)
        coll_color = block_color.pop(coll)
        ball_x, ball_y = detect_collision(ball_x, ball_y, ball, coll_rect)
        coll_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(screen, coll_color, coll_rect)
        fps += 2
        platform_speed += 0.5
        ball_speed += 0.1

    if ball.bottom > HEIGHT:
        print('You lose')
        exit()
    elif not len(blocks):
        print('You win!')
        exit()


    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and platform.left > 0:
        platform.left -= platform_speed
    if key[pygame.K_RIGHT] and platform.right < WIDTH:
        platform.right += platform_speed


    pygame.display.flip()
    clock.tick(fps)