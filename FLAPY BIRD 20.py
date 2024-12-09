import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar dan warna
SCREEN_WIDTH = 1080  # Ukuran layar
SCREEN_HEIGHT = 2400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)
EXPLOSION_COLOR = (255, 0, 0)  # Warna ledakan

# Atur layar dan judul game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Bird")

# Variabel game
bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_width = 34
bird_height = 24
gravity = 0.5
bird_velocity = 0
bird_flap = -10
bird_colors = [(0, 0, 0), (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]
bird_color_index = 0
selected_color = bird_colors[bird_color_index]
color_names = ['Black', 'Red', 'Blue', 'Green', 'Yellow']
color_name = color_names[bird_color_index]

pipe_width = 70
pipe_gap = 300
pipe_velocity = -8
pipe_frequency = 2000

score = 0
high_score = 0
font = pygame.font.SysFont(None, 36)
button_font = pygame.font.SysFont(None, 72)
color_name_font = pygame.font.SysFont(None, 96)
game_active = False
explosion_active = False

# List pipa
pipe_list = []

# Fungsi untuk menggambar pipa
def draw_pipe(x, height):
    pygame.draw.rect(screen, GREEN, (x, 0, pipe_width, height))
    pygame.draw.rect(screen, GREEN, (x, height + pipe_gap, pipe_width, SCREEN_HEIGHT))

# Fungsi untuk menampilkan skor
def display_score():
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 120, 10))

def display_high_score():
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (10, 10))

# Fungsi untuk memulai ulang game
def reset_game():
    global bird_y, bird_velocity, score, pipe_list, game_active, explosion_active
    bird_y = SCREEN_HEIGHT // 2
    bird_velocity = 0
    score = 0
    pipe_list.clear()
    game_active = True
    explosion_active = False
    pygame.time.set_timer(pygame.USEREVENT, pipe_frequency)

# Fungsi untuk efek ledakan
def draw_explosion(x, y):
    pygame.draw.circle(screen, EXPLOSION_COLOR, (x, y), 20)
    pygame.draw.circle(screen, EXPLOSION_COLOR, (x, y), 30, 2)
    pygame.draw.circle(screen, EXPLOSION_COLOR, (x, y), 40, 2)

# Fungsi untuk menggambar latar belakang
def draw_background(scroll_speed):
    screen.fill(SKY_BLUE)

# Fungsi untuk menggambar tombol
def draw_button(text, x, y, width, height, color, font):
    button_rect = pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x + (width // 2 - text_surface.get_width() // 2), y + (height // 2 - text_surface.get_height() // 2)))
    return button_rect

# Loop utama game
running = True
while running:
    screen.fill(WHITE)
    draw_background(pipe_velocity)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                bird_velocity = bird_flap
            else:
                if start_button_rect.collidepoint(event.pos):
                    reset_game()
                elif color_button_rect.collidepoint(event.pos):
                    bird_color_index = (bird_color_index + 1) % len(bird_colors)
                    selected_color = bird_colors[bird_color_index]
                    color_name = color_names[bird_color_index]

        if event.type == pygame.USEREVENT and game_active:
            pipe_height = random.randint(200, 1000)
            pipe_list.append([SCREEN_WIDTH, pipe_height, False])

    if game_active:
        bird_velocity += gravity
        bird_y += bird_velocity

        for pipe in pipe_list:
            pipe[0] += pipe_velocity

            if not pipe[2] and bird_x > pipe[0] + pipe_width:
                score += 1
                pipe[2] = True

            if bird_x + bird_width > pipe[0] and bird_x < pipe[0] + pipe_width:
                if bird_y < pipe[1] or bird_y + bird_height > pipe[1] + pipe_gap:
                    game_active = False
                    high_score = max(high_score, score)
                    explosion_active = True

        pipe_list = [pipe for pipe in pipe_list if pipe[0] + pipe_width > 0]

        if bird_y > SCREEN_HEIGHT - bird_height or bird_y < 0:
            game_active = False
            high_score = max(high_score, score)
            explosion_active = True

        pygame.draw.rect(screen, selected_color, (bird_x, bird_y, bird_width, bird_height))
        for pipe_x, pipe_height, _ in pipe_list:
            draw_pipe(pipe_x, pipe_height)

        display_score()

        if explosion_active:
            draw_explosion(bird_x + bird_width // 2, bird_y + bird_height // 2)
            explosion_active = False

    else:
        display_high_score()

        start_button_rect = draw_button("Start Game", SCREEN_WIDTH - 400 - 50, SCREEN_HEIGHT // 2, 400, 200, (0, 255, 0), button_font)
        color_button_rect = draw_button("Change Color", 50, SCREEN_HEIGHT // 2, 400, 200, (255, 140, 0), button_font)

        color_text = color_name_font.render(f"Color: {color_name}", True, BLACK)
        screen.blit(color_text, (50 + (400 // 2 - color_text.get_width() // 2), SCREEN_HEIGHT // 2 - 100))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
