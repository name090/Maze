import pygame
import random
import time
from collections import deque

# Ініціалізація pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('background music.mp3')
pygame.mixer.music.play(-1)

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

# Масштабування зображень
wall_image = pygame.transform.scale(wall_image, (CELL_SIZE, CELL_SIZE))
exit_image = pygame.transform.scale(exit_image, (CELL_SIZE, CELL_SIZE))
for key in player_images:
    player_images[key] = pygame.transform.scale(player_images[key], (CELL_SIZE, CELL_SIZE))

# Генерація лабіринту
def generate_maze():
    while True:
        maze = [[1 if random.random() < 0.2 else 0 for _ in range(WIDTH // CELL_SIZE)] for _ in range(HEIGHT // CELL_SIZE)]
        player_x, player_y = 0, 0
        exit_x, exit_y = generate_exit(maze)
        
        if bfs(maze, (player_x, player_y), (exit_x, exit_y)):
            return maze, (exit_x, exit_y)

# BFS для перевірки шляху
def bfs(maze, start, goal):
    queue = deque([start])
    visited = set()
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
    return False

# Генерація виходу
def generate_exit(maze):
    while True:
        exit_x, exit_y = random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1)
        if maze[exit_y][exit_x] == 0:
            return exit_x, exit_y

# Основна гра
def game():
    level = 1
    player_x, player_y = 0, 0
    player_direction = "down"
    clock = pygame.time.Clock()
    start_time = time.time()
    total_time = 300
    running = True
    
    while running:
        if level > 10:
            font = pygame.font.SysFont(None, 55)
            text = font.render("You Win!", True, YELLOW)
            SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False
            break
        
        maze, (exit_x, exit_y) = generate_maze()
        
        while running:
            SCREEN.fill(GREEN)
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    SCREEN.blit(wall_image if maze[i][j] else background_image, (j * CELL_SIZE, i * CELL_SIZE))
            
            SCREEN.blit(player_images[player_direction], (player_x * CELL_SIZE, player_y * CELL_SIZE))
            SCREEN.blit(exit_image, (exit_x * CELL_SIZE, exit_y * CELL_SIZE))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
            
            if player_x == exit_x and player_y == exit_y:
                level += 1
                player_x, player_y = 0, 0
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
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0 and maze[player_y][player_x - 1] == 0:
                player_x -= 1
                player_direction = "left"
            if keys[pygame.K_RIGHT] and player_x < len(maze[0]) - 1 and maze[player_y][player_x + 1] == 0:
                player_x += 1
                player_direction = "right"
            if keys[pygame.K_UP] and player_y > 0 and maze[player_y - 1][player_x] == 0:
                player_y -= 1
                player_direction = "up"
            if keys[pygame.K_DOWN] and player_y < len(maze) - 1 and maze[player_y + 1][player_x] == 0:
                player_y += 1
                player_direction = "down"
            
            pygame.display.flip()
            clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    game()
