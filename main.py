import pygame
import sys
import random
from datetime import datetime
import sqlite3

# Константы
WIDTH, HEIGHT = 800, 400
FPS = 30
GROUND_HEIGHT = 350
ORANGE = (255, 165, 0)
LINE_COLOR = (255, 255, 255)
COUNTER_COLOR = (178, 213, 213)
DAY_BACKGROUND = "day_background.jpg"
NIGHT_BACKGROUND = "night_background.jpg"
DATABASE_FILE = "game_data.db"

# Загрузка изображений
pygame.init()
try:
    dino_image = pygame.Surface((20, 20), pygame.SRCALPHA)  # Уменьшаем размер круга
    pygame.draw.circle(dino_image, ORANGE, (10, 10), 10)  # Уменьшаем радиус круга
except pygame.error as e:
    print("Error loading dino image:", e)
    sys.exit()

# Инициализация окна
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Apelsin Minimum Wages")
except pygame.error as e:
    print("Error initializing window:", e)
    sys.exit()

# Загрузка изображения фона (дневного и ночного)
try:
    day_background = pygame.image.load(DAY_BACKGROUND).convert()
    day_background = pygame.transform.scale(day_background, (WIDTH, HEIGHT))
    night_background = pygame.image.load(NIGHT_BACKGROUND).convert()
    night_background = pygame.transform.scale(night_background, (WIDTH, HEIGHT))
except pygame.error as e:
    print("Error loading background image:", e)
    sys.exit()

# Загрузка изображения елки
try:
    cactus_image = pygame.image.load("cactus.png").convert_alpha()
    cactus_image = pygame.transform.scale(cactus_image, (30, 60))
except pygame.error as e:
    print("Error loading cactus image:", e)
    sys.exit()

# Инициализация игры
clock = pygame.time.Clock()

class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = dino_image
            self.rect = self.image.get_rect()
            self.rect.bottom = GROUND_HEIGHT
            self.rect.x = 50
            self.jump_speed = 0
            self.jump_height = -25  # Увеличение высоты прыжка
            self.jump_length = 15   # Длина прыжка
            self.jump_countdown = 0
            self.elapsed_time = 0
        except pygame.error as e:
            print("Error creating Dino sprite:", e)
            sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == GROUND_HEIGHT and self.jump_countdown == 0:
            self.jump_speed = self.jump_height
            self.jump_countdown = self.jump_length

        if self.jump_countdown > 0:
            self.jump_speed += 1
            self.rect.y += self.jump_speed

            if self.rect.bottom > GROUND_HEIGHT:
                self.rect.bottom = GROUND_HEIGHT
                self.jump_countdown = 0  # Сброс счетчика после завершения прыжка
        else:
            if self.rect.bottom < GROUND_HEIGHT:
                self.rect.y += 5  # Имитация падения, когда не в прыжке

        self.elapsed_time += clock.get_rawtime()  # Увеличиваем счетчик миллисекунд

class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        try:
            self.image = cactus_image
            self.rect = self.image.get_rect()
            self.rect.bottom = GROUND_HEIGHT
            self.speed = speed
        except pygame.error as e:
            print("Error creating Cactus sprite:", e)
            sys.exit()

    def spawn(self):
        self.rect.x = WIDTH + random.randint(400, 700)  # Увеличение расстояния между елками

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.spawn()

# Инициализация базы данных
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()

# Создание таблицы, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER NOT NULL
    )
''')
conn.commit()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
cacti = pygame.sprite.Group()

# Создание игрока
try:
    player = Dino()
    all_sprites.add(player)
except pygame.error as e:
    print("Error creating player sprite:", e)
    sys.exit()

# Создание кактусов
max_cacti_together = 3
speed_increase = 0  # Переменная для увеличения скорости
for _ in range(max_cacti_together):
    cactus_speed = 5 + speed_increase
    try:
        cactus = Cactus(cactus_speed)
        cactus.spawn()
        all_sprites.add(cactus)
        cacti.add(cactus)
    except pygame.error as e:
        print("Error creating cactus sprite:", e)
        sys.exit()

# Счетчик новых ёлок
new_cactus_count = 0

# Расстояние между елками
distance_between_cacti = 200  # Измените это значение на необходимое вам

# Время, после которого начинают чаще появляться препятствия (в миллисекундах)
increase_spawn_time = 1000

# Основной игровой цикл
running = True
start_game = False  # Флаг начала игры
player_name = ""  # Имя игрока

# Окно старта
font = pygame.font.Font(None, 36)
input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
text_surface = font.render(text, True, color)
width = max(200, text_surface.get_width()+10)

while not start_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            start_game = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    start_game = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                width = max(200, font.render(text, True, color).get_width()+10)
                text_surface = font.render(text, True, color)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, color, input_box, 2)
    screen.blit(text_surface, (input_box.x+5, input_box.y+5))
    input_box.w = width
    pygame.display.flip()
    clock.tick(FPS)

player_name = text

# Основной игровой цикл после ввода имени
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление игры
    try:
        all_sprites.update()
    except pygame.error as e:
        print("Error updating sprites:", e)
        sys.exit()

    # Проверка столкновения динозавра с кактусами
    hits = pygame.sprite.spritecollide(player, cacti, False)
    if hits:
        score = int(player.elapsed_time)
        result_text = f"Game Over! Your score: {score} ms"

        # Добавление результата в базу данных
        cursor.execute("INSERT INTO players (name, score) VALUES (?, ?)", (player_name, score))
        conn.commit()

        running = False

    # Создание новых елок
    if random.randint(0, 100) < 5 and len(cacti) < max_cacti_together:
        new_cactus = Cactus(5 + speed_increase)
        new_cactus.spawn()

        # Проверка наложения елки на уже существующую
        overlapping = pygame.sprite.spritecollide(new_cactus, cacti, False)
        if not overlapping and new_cactus_count < 4:
            # Регулировка расстояния между елками
            if len(cacti) == 0 or (len(cacti) > 0 and cacti.sprites()[-1].rect.right < WIDTH - distance_between_cacti):
                all_sprites.add(new_cactus)
                cacti.add(new_cactus)
                new_cactus_count += 1
            else:
                new_cactus.spawn()  # Если новая елка не подходит, спавним другую

    # Сброс счетчика новых ёлок
    if new_cactus_count >= 4 and all(c.rect.right < 0 for c in cacti):
        new_cactus_count = 0

    # Увеличение скорости при успешном избегании
    if not hits:
        speed_increase += 0.01

    # Появление препятствий чаще после определенного времени
    if player.elapsed_time > increase_spawn_time:
        increase_spawn_time += 1000  # Увеличиваем время для следующего увеличения
        speed_increase += 0.01  # Увеличиваем скорость

    # Определение времени суток
    current_time = datetime.now().time()
    is_daytime = current_time.hour >= 6 and current_time.hour < 18

    # Отрисовка фона в зависимости от времени суток
    try:
        if is_daytime:
            screen.blit(day_background, (0, 0))
        else:
            screen.blit(night_background, (0, 0))
    except pygame.error as e:
        print("Error drawing background:", e)
        sys.exit()

    # Отрисовка
    try:
        all_sprites.draw(screen)
    except pygame.error as e:
        print("Error drawing sprites:", e)
        sys.exit()

    # Отображение времени в правом верхнем углу
    try:
        font = pygame.font.Font(None, 36)
        time_text = font.render(f"{player.elapsed_time} ms", True, COUNTER_COLOR)
        screen.blit(time_text, (WIDTH - 150, 20))
    except pygame.error as e:
        print("Error rendering text:", e)
        sys.exit()

    # Отрисовка линии, по которой катится круг
    try:
        pygame.draw.line(screen, LINE_COLOR, (0, GROUND_HEIGHT + 10), (WIDTH, GROUND_HEIGHT + 10), 2)
    except pygame.error as e:
        print("Error drawing line:", e)
        sys.exit()

    # Обновление экрана
    pygame.display.flip()

    # Задержка
    try:
        clock.tick(FPS)
    except pygame.error as e:
        print("Error ticking clock:", e)
        sys.exit()

# Завершение игры и закрытие базы данных
pygame.quit()
conn.close()
sys.exit()
