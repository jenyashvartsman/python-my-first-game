import pygame
import random
import sys

# CONSTANTS
WINDOWED_SIZE = (800, 600)
SCORE_BAR_HEIGHT = 50
TREE_SIZE = 60
NUM_TREES = 5
MONKEY_SIZE = 35
MONKEY_SPEED = 5
BANANA_RADIUS = 15

BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

# Initialize Pygame
pygame.init()
is_fullscreen = False
screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Monkey Banana Game")
font = pygame.font.SysFont(None, 36)

# Load images
monkey_img = pygame.image.load("images/monkey.png").convert_alpha()
monkey_img = pygame.transform.scale(monkey_img, (MONKEY_SIZE, MONKEY_SIZE))

tree_img = pygame.image.load("images/tree.png").convert_alpha()
tree_img = pygame.transform.scale(tree_img, (TREE_SIZE, TREE_SIZE))

banana_img = pygame.image.load("images/banana.png").convert_alpha()
banana_img = pygame.transform.scale(banana_img, (BANANA_RADIUS * 2, BANANA_RADIUS * 2))

# Obstacles (trees)
obstacles = []
for _ in range(NUM_TREES):
    while True:
        x = random.randint(0, WINDOWED_SIZE[0] - TREE_SIZE)
        y = random.randint(SCORE_BAR_HEIGHT, WINDOWED_SIZE[1] - TREE_SIZE)
        tree_rect = pygame.Rect(x, y, TREE_SIZE, TREE_SIZE)
        obstacles.append(tree_rect)
        break

# Monkey (player)
while True:
    monkey_x = random.randint(0, WINDOWED_SIZE[0] - MONKEY_SIZE)
    monkey_y = random.randint(SCORE_BAR_HEIGHT, WINDOWED_SIZE[1] - MONKEY_SIZE)
    monkey_rect = pygame.Rect(monkey_x, monkey_y, MONKEY_SIZE, MONKEY_SIZE)
    collision = False
    for obstacle in obstacles:
        if monkey_rect.colliderect(obstacle):
            collision = True
            break
    if not collision:
        break

# Banana (target)
banana_x = random.randint(0, WINDOWED_SIZE[0] - BANANA_RADIUS * 2)
banana_y = random.randint(SCORE_BAR_HEIGHT, WINDOWED_SIZE[1] - BANANA_RADIUS * 2)

# Score
score = 0

# Clock
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    # Draw score bar background
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WINDOWED_SIZE[0], SCORE_BAR_HEIGHT))
    # Draw score text
    score_text = font.render(f"Bananas eaten: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)

    # Movement input
    keys = pygame.key.get_pressed()
    prev_x, prev_y = monkey_x, monkey_y

    if keys[pygame.K_LEFT]:
        monkey_x -= MONKEY_SPEED
    if keys[pygame.K_RIGHT]:
        monkey_x += MONKEY_SPEED
    if keys[pygame.K_UP]:
        monkey_y -= MONKEY_SPEED
    if keys[pygame.K_DOWN]:
        monkey_y += MONKEY_SPEED

    # Clamp to screen bounds
    monkey_x = max(0, min(WINDOWED_SIZE[0] - MONKEY_SIZE, monkey_x))
    monkey_y = max(SCORE_BAR_HEIGHT, min(WINDOWED_SIZE[1] - MONKEY_SIZE, monkey_y))

    monkey_rect = pygame.Rect(monkey_x, monkey_y, MONKEY_SIZE, MONKEY_SIZE)

    # Block movement if colliding with an obstacle
    for obstacle in obstacles:
        if monkey_rect.colliderect(obstacle):
            monkey_x, monkey_y = prev_x, prev_y
            monkey_rect = pygame.Rect(monkey_x, monkey_y, MONKEY_SIZE, MONKEY_SIZE)
            break

    # Draw obstacles (trees)
    for obstacle in obstacles:
        screen.blit(tree_img, (obstacle.x, obstacle.y))

    # Draw monkey
    screen.blit(monkey_img, (monkey_rect.x, monkey_rect.y))

    # Draw banana
    screen.blit(banana_img, (banana_x, banana_y))
    banana_rect = pygame.Rect(banana_x, banana_y, BANANA_RADIUS * 2, BANANA_RADIUS * 2)

    # Eat banana
    if monkey_rect.colliderect(banana_rect):
        score += 1
        banana_x = random.randint(0, WINDOWED_SIZE[0] - BANANA_RADIUS * 2)
        banana_y = random.randint(SCORE_BAR_HEIGHT, WINDOWED_SIZE[1] - BANANA_RADIUS * 2)
        pygame.display.set_caption(f"Monkey Banana Game - Bananas eaten: {score}")

    # Also, update the caption every frame to keep it in sync
    pygame.display.set_caption(f"Monkey Banana Game - Bananas eaten: {score}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
