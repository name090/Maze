import pygame
import random
import time
from collections import deque

# Ініціалізація pygame
pygame.init()

# Визначення кольорів
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Розміри екрану
WIDTH, HEIGHT = 800, 608
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабіринт")

# Розміри клітин
CELL_SIZE = 32

# Завантаження зображень
background_image = pygame.image.load("background.png")
wall_image = pygame.image.load("wall.png")
exit_image = pygame.image.load("exit.png")
player_images = {
    "down": pygame.image.load("hero1.png"),
    "left": pygame.image.load("hero2.png"),
    "up": pygame.image.load("hero3.png"),
    "right": pygame.image.load("hero4.png")
}

# Масштабування зображень під розміри клітин
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))
for key in player_images:
    player_images[key] = pygame.transform.scale(player_images[key], (CELL_SIZE, CELL_SIZE))

# Створення лабіринту
def generate_maze():
    maze = []
    for i in range(0, HEIGHT, CELL_SIZE):
        row = []
        for j in range(0, WIDTH, CELL_SIZE):
            if random.random() < 0.2:  # 20% ймовірність стіни
                row.append(1)
            else:
                row.append(0)
        maze.append(row)
    return maze

# Малювання лабіринту
def draw_maze(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                SCREEN.blit(wall_image, (j * CELL_SIZE, i * CELL_SIZE))  # Малюємо стіну
            else:
                SCREEN.blit(background_image, (j * CELL_SIZE, i * CELL_SIZE))  # Малюємо фон

# Перевірка, чи можна переміщатися в клітину
def is_valid_move(maze, x, y):
    if 0 <= x < len(maze[0]) and 0 <= y < len(maze):
        return maze[y][x] == 0
    return False

# Створення виходу в лабіринті
def generate_exit(maze):
    exit_x = random.randint(0, len(maze[0]) - 1)
    exit_y = random.randint(0, len(maze) - 1)
    
    while maze[exit_y][exit_x] == 1:
        exit_x = random.randint(0, len(maze[0]) - 1)
        exit_y = random.randint(0, len(maze) - 1)
    
    return (exit_x, exit_y)

# Основна функція гри
def game():
    level = 1
    player_x, player_y = 0, 0
    player_direction = "down"  # Початковий напрямок персонажа
    clock = pygame.time.Clock()
    
    start_time = time.time()
    total_time = 300

    running = True
    while running:
        maze = generate_maze()
        exit_x, exit_y = generate_exit(maze)
        
        while not is_valid_move(maze, player_x, player_y):
            maze = generate_maze()
            exit_x, exit_y = generate_exit(maze)
        
        while True:
            SCREEN.fill(GREEN)
            draw_maze(maze)
            SCREEN.blit(player_images[player_direction], (player_x * CELL_SIZE, player_y * CELL_SIZE))
            SCREEN.blit(exit_image, (exit_x * CELL_SIZE, exit_y * CELL_SIZE))
            
            if player_x == exit_x and player_y == exit_y:
                level += 1
                player_x, player_y = 0, 0
                if level > 10:
                    font = pygame.font.SysFont(None, 55)
                    text = font.render("You Win!", True, YELLOW)
                    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    running = False
                    break
                break

            elapsed_time = time.time() - start_time
            remaining_time = total_time - elapsed_time
            if remaining_time <= 0:
                font = pygame.font.SysFont(None, 55)
                text = font.render("YOU LOST", True, YELLOW)
                SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
                break

            font = pygame.font.SysFont(None, 30)
            timer_text = font.render(f"Time: {int(remaining_time)}", True, BLUE)
            SCREEN.blit(timer_text, (10, 10))

            level_text = font.render(f"Level: {level}", True, BLUE)
            SCREEN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if is_valid_move(maze, player_x - 1, player_y):
                    player_x -= 1
                    player_direction = "left"
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if is_valid_move(maze, player_x + 1, player_y):
                    player_x += 1
                    player_direction = "right"
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if is_valid_move(maze, player_x, player_y - 1):
                    player_y -= 1
                    player_direction = "up"
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if is_valid_move(maze, player_x, player_y + 1):
                    player_y += 1
                    player_direction = "down"
            
            pygame.display.flip()
            clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    game()
