#!/usr/bin/env python3
import pygame, sys

WIDTH, HEIGHT = 640, 480
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 80
BALL_SIZE = 10
WHITE = (255,255,255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Paddles and ball
    left = pygame.Rect(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right = pygame.Rect(WIDTH-20, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
    vx, vy = 4, 4

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left.top > 0:
            left.y -= 5
        if keys[pygame.K_s] and left.bottom < HEIGHT:
            left.y += 5

        # simple AI for right paddle
        if right.centery < ball.centery and right.bottom < HEIGHT:
            right.y += 4
        if right.centery > ball.centery and right.top > 0:
            right.y -= 4

        # move ball
        ball.x += vx; ball.y += vy
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            vy = -vy
        if ball.colliderect(left) or ball.colliderect(right):
            vx = -vx

        # score reset
        if ball.left <= 0 or ball.right >= WIDTH:
            ball.center = (WIDTH//2, HEIGHT//2)

        screen.fill((0,0,0))
        pygame.draw.rect(screen, WHITE, left)
        pygame.draw.rect(screen, WHITE, right)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2,0), (WIDTH//2, HEIGHT))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
