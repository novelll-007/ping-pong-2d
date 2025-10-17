# Simple 2D Ping Pong Game by Comet Assistant

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ping Pong Game')

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Paddle positions
left_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
right_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Ball position and velocity
ball_x = WIDTH // 2 - BALL_SIZE // 2
ball_y = HEIGHT // 2 - BALL_SIZE // 2
ball_vel_x = BALL_SPEED_X
ball_vel_y = BALL_SPEED_Y

# Scores
left_score = 0
right_score = 0

# Font for displaying scores
font = pygame.font.Font(None, 74)

def draw_objects():
    """Draw all game objects on the screen."""
    screen.fill(BLACK)
    
    # Draw paddles
    pygame.draw.rect(screen, WHITE, (30, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 30 - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # Draw ball
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    
    # Draw center line
    for i in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, i, 4, 10))
    
    # Draw scores
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (3 * WIDTH // 4, 20))

def move_paddles(keys):
    """Move paddles based on keyboard input."""
    global left_paddle_y, right_paddle_y
    
    # Left paddle (W and S keys)
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle_y < HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += PADDLE_SPEED
    
    # Right paddle (Up and Down arrow keys)
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle_y < HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += PADDLE_SPEED

def move_ball():
    """Move the ball and handle collisions."""
    global ball_x, ball_y, ball_vel_x, ball_vel_y, left_score, right_score
    
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    
    # Ball collision with top and bottom walls
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_vel_y *= -1
    
    # Ball collision with left paddle
    if (ball_x <= 30 + PADDLE_WIDTH and 
        left_paddle_y <= ball_y + BALL_SIZE and 
        ball_y <= left_paddle_y + PADDLE_HEIGHT):
        ball_vel_x *= -1
        ball_x = 30 + PADDLE_WIDTH
    
    # Ball collision with right paddle
    if (ball_x + BALL_SIZE >= WIDTH - 30 - PADDLE_WIDTH and 
        right_paddle_y <= ball_y + BALL_SIZE and 
        ball_y <= right_paddle_y + PADDLE_HEIGHT):
        ball_vel_x *= -1
        ball_x = WIDTH - 30 - PADDLE_WIDTH - BALL_SIZE
    
    # Ball goes out of bounds (scoring)
    if ball_x < 0:
        right_score += 1
        reset_ball()
    elif ball_x > WIDTH:
        left_score += 1
        reset_ball()

def reset_ball():
    """Reset ball to center after a score."""
    global ball_x, ball_y, ball_vel_x, ball_vel_y
    ball_x = WIDTH // 2 - BALL_SIZE // 2
    ball_y = HEIGHT // 2 - BALL_SIZE // 2
    ball_vel_x = BALL_SPEED_X * (-1 if ball_vel_x > 0 else 1)
    ball_vel_y = BALL_SPEED_Y

def main():
    """Main game loop."""
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Update game objects
        move_paddles(keys)
        move_ball()
        
        # Draw everything
        draw_objects()
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate (60 FPS)
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
