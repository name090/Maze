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
WIDTH, HEIGHT = 600, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабіринт")

# Розміри клітин
CELL_SIZE = 20

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
            color = BLACK if maze[i][j] == 1 else WHITE
            pygame.draw.rect(SCREEN, color, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Перевірка, чи можна переміщатися в клітину
def is_valid_move(maze, x, y):
    if 0 <= x < len(maze[0]) and 0 <= y < len(maze):
        return maze[y][x] == 0
    return False

# Створення виходу в лабіринті
def generate_exit(maze):
    exit_x = random.randint(0, len(maze[0]) - 1)
    exit_y = random.randint(0, len(maze) - 1)
    
    # Перевіримо, чи є вихід у прохідній клітинці
    while maze[exit_y][exit_x] == 1:
        exit_x = random.randint(0, len(maze[0]) - 1)
        exit_y = random.randint(0, len(maze) - 1)
    
    return (exit_x, exit_y)

# Перевірка, чи є шлях до виходу
def is_path_to_exit(maze, start_x, start_y, exit_x, exit_y):
    # Використовуємо BFS для перевірки шляху від старту до виходу
    queue = deque([(start_x, start_y)])
    visited = set()
    visited.add((start_x, start_y))
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Ліво, Право, Вверх, Вниз
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == (exit_x, exit_y):
            return True
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and (nx, ny) not in visited and maze[ny][nx] == 0:
                visited.add((nx, ny))
                queue.append((nx, ny))
    
    return False

# Основна функція гри
def game():
    level = 1
    player_x, player_y = 0, 0  # Початкова позиція гравця
    clock = pygame.time.Clock()
    
    start_time = time.time()
    total_time = 300  # 5 хвилин = 300 секунд

    # Основний цикл гри
    running = True
    while running:
        # Генерація лабіринту і виходу
        maze = generate_maze()
        exit_x, exit_y = generate_exit(maze)
        
        # Перевірка, чи є шлях до виходу
        while not is_path_to_exit(maze, player_x, player_y, exit_x, exit_y):
            maze = generate_maze()
            exit_x, exit_y = generate_exit(maze)
        
        while True:
            SCREEN.fill(GREEN)
            
            draw_maze(maze)
            pygame.draw.rect(SCREEN, RED, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(SCREEN, BLUE, (exit_x * CELL_SIZE, exit_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            
            # Перевірка досягнення виходу
            if player_x == exit_x and player_y == exit_y:
                level += 1
                player_x, player_y = 0, 0  # Скидаємо позицію гравця на старт
                
                # Якщо рівень 10 або більше, виводимо "You Win"
                if level > 10:
                    font = pygame.font.SysFont(None, 55)
                    text = font.render("You Win!", True, YELLOW)
                    SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)  # Чекаємо 2 секунди, щоб показати повідомлення
                    running = False
                    break
                break

            # Перевірка часу
            elapsed_time = time.time() - start_time
            remaining_time = total_time - elapsed_time
            if remaining_time <= 0:
                # Якщо час вичерпано, виводимо "YOU LOST"
                font = pygame.font.SysFont(None, 55)
                text = font.render("YOU LOST", True, YELLOW)
                SCREEN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)  # Чекаємо 2 секунди, щоб показати повідомлення
                running = False
                break

            # Малювання таймера
            font = pygame.font.SysFont(None, 30)
            timer_text = font.render(f"Time: {int(remaining_time)}", True, BLUE)
            SCREEN.blit(timer_text, (10, 10))

            # Малювання поточного рівня
            level_text = font.render(f"Level: {level}", True, BLUE)
            SCREEN.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Переміщення гравця
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and is_valid_move(maze, player_x - 1, player_y):
                player_x -= 1
            if keys[pygame.K_RIGHT] and is_valid_move(maze, player_x + 1, player_y):
                player_x += 1
            if keys[pygame.K_UP] and is_valid_move(maze, player_x, player_y - 1):
                player_y -= 1
            if keys[pygame.K_DOWN] and is_valid_move(maze, player_x, player_y + 1):
                player_y += 1

            # Оновлення екрану
            pygame.display.flip()
            
            # Обмеження FPS
            clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    game()
