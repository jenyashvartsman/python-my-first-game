import pygame
import random
import sys

# Initialize Pygame
pygame.init()
WINDOWED_SIZE = (800, 600)
is_fullscreen = False
screen = pygame.display.set_mode(WINDOWED_SIZE, pygame.RESIZABLE)
pygame.display.set_caption("Monkey Banana Game")

# Colors
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)

# Fonts
font = pygame.font.SysFont(None, 36)

SCORE_BAR_HEIGHT = 50

# Trees (obstacles)
tree_size = 60
num_trees = 5
trees = []
for _ in range(num_trees):
    while True:
        x = random.randint(0, 800 - tree_size)
        y = random.randint(SCORE_BAR_HEIGHT, 600 - tree_size)
        tree_rect = pygame.Rect(x, y, tree_size, tree_size)
        # Prevent trees from spawning on top of the monkey (will fix after monkey spawn)
        trees.append(tree_rect)
        break

# Monkey (player)
monkey_size = 50
while True:
    monkey_x = random.randint(0, 800 - monkey_size)
    monkey_y = random.randint(SCORE_BAR_HEIGHT, 600 - monkey_size)
    monkey_rect = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)
    collision = False
    for tree in trees:
        if monkey_rect.colliderect(tree):
            collision = True
            break
    if not collision:
        break

monkey_speed = 5

# Banana (target)
banana_radius = 20
banana_x = random.randint(0, 800 - banana_radius * 2)
banana_y = random.randint(SCORE_BAR_HEIGHT, 600 - banana_radius * 2)

# Score
score = 0

# Clock
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(WHITE)
    # Draw score bar background
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, 800, SCORE_BAR_HEIGHT))
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
        monkey_x -= monkey_speed
    if keys[pygame.K_RIGHT]:
        monkey_x += monkey_speed
    if keys[pygame.K_UP]:
        monkey_y -= monkey_speed
    if keys[pygame.K_DOWN]:
        monkey_y += monkey_speed

    # Clamp to screen bounds
    monkey_x = max(0, min(800 - monkey_size, monkey_x))
    monkey_y = max(SCORE_BAR_HEIGHT, min(600 - monkey_size, monkey_y))

    monkey_rect = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)

    # Block movement if colliding with a tree
    for tree in trees:
        if monkey_rect.colliderect(tree):
            monkey_x, monkey_y = prev_x, prev_y
            monkey_rect = pygame.Rect(monkey_x, monkey_y, monkey_size, monkey_size)
            break

    # Draw trees
    for tree in trees:
        pygame.draw.rect(screen, GREEN, tree)

    # Draw monkey
    pygame.draw.rect(screen, BROWN, monkey_rect)

    # Draw banana
    banana_center = (banana_x + banana_radius, banana_y + banana_radius)
    banana_rect = pygame.Rect(banana_x, banana_y, banana_radius * 2, banana_radius * 2)
    pygame.draw.circle(screen, YELLOW, banana_center, banana_radius)

    # Eat banana
    if monkey_rect.colliderect(banana_rect):
        score += 1
        banana_x = random.randint(0, 800 - banana_radius * 2)
        banana_y = random.randint(SCORE_BAR_HEIGHT, 600 - banana_radius * 2)
        pygame.display.set_caption(f"Monkey Banana Game - Bananas eaten: {score}")

    # Also, update the caption every frame to keep it in sync
    pygame.display.set_caption(f"Monkey Banana Game - Bananas eaten: {score}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
