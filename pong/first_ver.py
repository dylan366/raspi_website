import pygame

pygame.init()

WIDTH = 600
HEIGHT = 400

#colours
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#ball
radius = 8
ball_x = WIDTH//2 - radius
ball_y = HEIGHT//2 - radius

ball_vel_x = 0.1
ball_vel_y = 0.1

#paddles
paddles_width = 20
paddles_height = 120

PADDLE_SPEED = 0.2

left_paddle_y = right_paddle_y = HEIGHT//2 - paddles_height//2
left_paddle_x = 0
right_paddle_x = WIDTH - paddles_width

right_paddle_vel = 0
left_paddle_vel = 0

# CONTROLS
UP_BUTTON = pygame.K_UP
DOWN_BUTTON = pygame.K_DOWN

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")

running = True

while running: 
    window.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == DOWN_BUTTON:
            #plyer right
            if event.key == UP_BUTTON:
                right_paddle_vel = -1 * PADDLE_SPEED
            if event.key == DOWN_BUTTON:
                right_paddle_vel = PADDLE_SPEED
            #player left
            if event.key == pygame.K_w:
                left_paddle_vel = -1 * PADDLE_SPEED
            if event.key == pygame.K_s:
                left_paddle_vel = PADDLE_SPEED
        if event.type == pygame.KEYUP:
            right_paddle_vel = 0
            left_paddle_vel = 0
            
            
            
    if ball_y <= 0 + radius or ball_y >= HEIGHT - radius: #out of bounds
        ball_vel_y *= -1
    
    #back to starting position with opposite speed
    if ball_x >= WIDTH - radius:
        ball_x = WIDTH//2 - radius
        ball_y = HEIGHT//2 - radius
        ball_vel_x *= -1
        ball_vel_y *= -1
    if ball_x <= 0 + radius:
        ball_x = WIDTH//2 - radius
        ball_y = HEIGHT//2 - radius
        ball_vel_x = 0.1
        ball_vel_y = 0.1
    
    #paddle check
    #left
    if left_paddle_y >= HEIGHT - paddles_height:
        left_paddle_y = HEIGHT - paddles_height
    if left_paddle_y <= 0:
        left_paddle_y = 0
    #right
    if right_paddle_y >= HEIGHT - paddles_height:
        right_paddle_y = HEIGHT - paddles_height
    if right_paddle_y <= 0:
        right_paddle_y = 0
    
    #COLLISION
    #left (need to add paddel width since starting point is away from the screen)
    if left_paddle_x <= ball_x <= left_paddle_x + paddles_width:
        if left_paddle_y <= ball_y <= left_paddle_y + paddles_height:
            ball_x = left_paddle_x + paddles_width
            ball_vel_x *= -1
    #right (starting point is facing ball but ball start is facing away so now change ball dimensions not paddles)
    if right_paddle_x <= ball_x <= right_paddle_x + paddles_width:
        if right_paddle_y <= ball_y <= right_paddle_y + paddles_height:
            ball_x = right_paddle_x
            ball_vel_x *= -1
    # movement
    # balls
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    
    right_paddle_y += right_paddle_vel
    left_paddle_y += left_paddle_vel
    
    
    pygame.draw.circle(window, WHITE, (ball_x, ball_y), radius)
    pygame.draw.rect(window, WHITE, pygame.Rect(left_paddle_x, left_paddle_y, paddles_width, paddles_height))
    pygame.draw.rect(window, WHITE, pygame.Rect(right_paddle_x, right_paddle_y, paddles_width, paddles_height))
    
    pygame.display.update()
