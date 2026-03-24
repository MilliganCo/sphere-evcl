import pygame
import math
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1800, 1200  # Размер окна
RADIUS = 60  # Радиус сферы
PLAYER_SYMBOL = '*'  # Символ игрока (звёздочка)
FPS = 60  # Частота кадров

# Ключи управления
DIRECTIONS = {
    'W': (0, 1),
    'S': (0, -1),
    'A': (-1, 0),
    'D': (1, 0),
}

# Цвета (приглушённые)
COLORS = [
    (150, 0, 0),   # Red
    (0, 150, 0),   # Green
    (0, 0, 150),   # Blue
    (150, 150, 0), # Yellow
    (150, 85, 0),  # Orange
    (0, 150, 150), # Cyan
    (150, 0, 150), # Magenta
    (150, 150, 150) # White
]

# Размеры клетки лабиринта
CELL_SIZE = 30
MAZE_WIDTH = 40
MAZE_HEIGHT = 30

# Функция преобразования сферических координат в декартовы
def spherical_to_cartesian(r, theta, phi):
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    return x, y, z

# Функция генерации лабиринта с реальными проходами (Алгоритм Прима)
def generate_maze():
    maze = [['#' for _ in range(MAZE_WIDTH)] for _ in range(MAZE_HEIGHT)]

    # Список для активных клеток, с которых начинаем генерацию
    walls = []
    start_x, start_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)
    maze[start_y][start_x] = ' '  # Начальная точка
    walls.append((start_x, start_y))

    # Алгоритм Прима для генерации лабиринта
    while walls:
        x, y = random.choice(walls)
        walls.remove((x, y))

        neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            if 0 < nx < MAZE_WIDTH - 1 and 0 < ny < MAZE_HEIGHT - 1 and maze[ny][nx] == '#':
                maze[ny][nx] = ' '
                maze[(ny + y) // 2][(nx + x) // 2] = ' '
                walls.append((nx, ny))
                break

    return maze

# Функция для рендеринга лабиринта и объектов
def render_world(screen, maze, player_x, player_y):
    screen.fill((0, 0, 0))  # Очистка экрана

    # Рисуем лабиринт на сфере
    for y in range(MAZE_HEIGHT):
        for x in range(MAZE_WIDTH):
            # Преобразование клеток лабиринта на сферу
            theta = 2 * math.pi * x / MAZE_WIDTH
            phi = math.pi * y / MAZE_HEIGHT

            # Преобразование в декартовы координаты
            dx, dy, dz = spherical_to_cartesian(RADIUS, theta, phi)

            # Перевод в 2D
            screen_x = WIDTH / 2 + (dx / dz) * (WIDTH / 4)
            screen_y = HEIGHT / 2 + (dy / dz) * (HEIGHT / 4)

            # Если клетка пуста, рисуем её
            color = (100, 100, 100) if maze[y][x] == '#' else (0, 0, 0)
            pygame.draw.rect(screen, color, (screen_x - CELL_SIZE / 2, screen_y - CELL_SIZE / 2, CELL_SIZE, CELL_SIZE))

    # Рисуем игрока (звездочка) на сфере
    player_theta = 2 * math.pi * player_x / MAZE_WIDTH
    player_phi = math.pi * player_y / MAZE_HEIGHT
    player_dx, player_dy, player_dz = spherical_to_cartesian(RADIUS, player_theta, player_phi)

    # Перевод в 2D
    player_screen_x = WIDTH / 2 + (player_dx / player_dz) * (WIDTH / 4)
    player_screen_y = HEIGHT / 2 + (player_dy / player_dz) * (HEIGHT / 4)

    pygame.draw.circle(screen, (255, 255, 255), (player_screen_x, player_screen_y), 15)  # Символ игрока в центре
    font = pygame.font.Font(None, 36)
    text = font.render(PLAYER_SYMBOL, True, (255, 0, 0))
    screen.blit(text, (player_screen_x - text.get_width() // 2, player_screen_y - text.get_height() // 2))

    pygame.display.flip()

# Функция для обновления позиции игрока
def move_player(player_x, player_y, maze, direction):
    dx, dy = DIRECTIONS[direction]
    new_x, new_y = player_x + dx, player_y + dy

    # Проверка на стены
    if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and maze[new_y][new_x] == ' ':
        return new_x, new_y
    return player_x, player_y

def main():
    # Инициализация окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Сферический лабиринт")

    # Генерация лабиринта
    maze = generate_maze()

    # Начальная позиция игрока
    player_x, player_y = random.randint(1, MAZE_WIDTH - 2), random.randint(1, MAZE_HEIGHT - 2)

    clock = pygame.time.Clock()

    # Игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Обработка клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_x, player_y = move_player(player_x, player_y, maze, 'W')
        if keys[pygame.K_s]:
            player_x, player_y = move_player(player_x, player_y, maze, 'S')
        if keys[pygame.K_a]:
            player_x, player_y = move_player(player_x, player_y, maze, 'A')
        if keys[pygame.K_d]:
            player_x, player_y = move_player(player_x, player_y, maze, 'D')

        render_world(screen, maze, player_x, player_y)
        clock.tick(FPS)  # Ограничение FPS

if __name__ == "__main__":
    main()
