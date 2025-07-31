import pygame
import random
import sys

# Window
WINDOWED_SIZE = (800, 600)

# Colors
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOWED_SIZE)
pygame.display.set_caption("Monkey Banana Game")

# Fonts
font = pygame.font.SysFont(None, 36)

# Monkey (player)
monkey_size = 50
monkey_x = 100
monkey_y = 100
monkey_speed = 5

# Banana (target)
banana_radius = 20
banana_x = random.randint(0, 800 - banana_radius * 2)
banana_y = random.randint(0, 600 - banana_radius * 2)

# Score
score = 0

# Clock
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keypresses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        monkey_x -= monkey_speed
    if keys[pygame.K_RIGHT]:
        monkey_x += monkey_speed
    if keys[pygame.K_UP]:
        monkey_y -= monkey_speed
    if keys[pygame.K_DOWN]:
        monkey_y += monkey_speed

    # Keep monkey inside screen
    monkey_x = max(0, min(800 - monkey_size, monkey_x))
    monkey_y = max(0, min(600 - monkey_size, monkey_y))

    # Draw monkey (as a square)
    monkey_rect = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)
    pygame.draw.rect(screen, BROWN, monkey_rect)

    # Draw banana (as a circle)
    banana_center = (banana_x + banana_radius, banana_y + banana_radius)
    pygame.draw.circle(screen, YELLOW, banana_center, banana_radius)

    # Check collision
    banana_rect = pygame.Rect(banana_x, banana_y, banana_radius * 2, banana_radius * 2)
    if monkey_rect.colliderect(banana_rect):
        score += 1
        banana_x = random.randint(0, 800 - banana_radius * 2)
        banana_y = random.randint(0, 600 - banana_radius * 2)

    # Draw score
    score_text = font.render(f"Bananas eaten: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
