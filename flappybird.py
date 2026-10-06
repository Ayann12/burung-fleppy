import pygame
from sys import exit
import random

import os
import sys

# =========================
# resource convert img
# =========================
def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)




# =========================
# GAME VARIABLES
# =========================
GAME_WIDTH = 360
GAME_HEIGHT = 640

# =========================
# BIRD VARIABLES
# =========================
bird_x = GAME_WIDTH / 8
bird_y = GAME_HEIGHT / 2
bird_width = 34
bird_height = 24


# =========================
# BIRD CLASS
# =========================
class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(
            self,
            bird_x,
            bird_y,
            bird_width,
            bird_height
        )
        self.img = img


# =========================
# PIPE VARIABLES
# =========================
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512


# =========================
# PIPE CLASS
# =========================
class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(
            self,
            pipe_x,
            pipe_y,
            pipe_width,
            pipe_height
        )
        self.img = img
        self.passed = False


# =========================
# INITIALIZE PYGAME
# =========================
pygame.init()

window = pygame.display.set_mode(
    (GAME_WIDTH, GAME_HEIGHT)
)

pygame.display.set_caption("Burung Flepy")

clock = pygame.time.Clock()


# =========================
# GAME IMAGES
# =========================
background_image = pygame.image.load(resource_path(
    "flappybirdbg.png"
))

bird_image = pygame.image.load(resource_path(
    "flappybird.png"
))

bird_image = pygame.transform.scale(
    bird_image,
    (bird_width, bird_height)
)

top_pipe_image = pygame.image.load(resource_path(
    "toppipe.png"
))

top_pipe_image = pygame.transform.scale(
    top_pipe_image,
    (pipe_width, pipe_height)
)

bottom_pipe_image = pygame.image.load(resource_path(
    "bottompipe.png"
))

bottom_pipe_image = pygame.transform.scale(
    bottom_pipe_image,
    (pipe_width, pipe_height)
)


# =========================
# GAME OBJECTS
# =========================
bird = Bird(bird_image)

pipes = []

velocity_x = -2
velocity_y = 0
gravity = 0.4

score = 0
best_score = 0

game_over = False

# =========================
# GAME STATE
# =========================
# menu = Main Menu
# playing = Game
game_state = "menu"


# =========================
# FONT
# =========================

# Main menu title
title_font = pygame.font.SysFont(
    "Comic Sans MS",
    32,
    bold=True
)

# Score
score_font = pygame.font.SysFont(
    "Comic Sans MS",
    45
)

# Game Over
game_over_font = pygame.font.SysFont(
    "Comic Sans MS",
    40,
    bold=True
)

# Buttons
button_font = pygame.font.SysFont(
    "Comic Sans MS",
    20,
    bold=True
)

# Small text
small_font = pygame.font.SysFont(
    "Comic Sans MS",
    18
)


# =========================
# BUTTONS
# =========================

# MULAI
start_button = pygame.Rect(
    GAME_WIDTH // 2 - 75,
    GAME_HEIGHT // 2 - 10,
    150,
    45
)

# KELUAR
exit_button = pygame.Rect(
    GAME_WIDTH // 2 - 75,
    GAME_HEIGHT // 2 + 50,
    150,
    45
)

# MAIN LAGI
restart_button = pygame.Rect(
    GAME_WIDTH // 2 - 100,
    GAME_HEIGHT // 2 + 20,
    200,
    60
)

# MENU UTAMA
menu_button = pygame.Rect(
    GAME_WIDTH // 2 - 100,
    GAME_HEIGHT // 2 + 90,
    200,
    50
)


# =========================
# DRAW BUTTON
# =========================
def draw_button(rect, text, color):

    pygame.draw.rect(
        window,
        color,
        rect,
        border_radius=10
    )

    text_surface = button_font.render(
        text,
        True,
        "White"
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    window.blit(
        text_surface,
        text_rect
    )


# =========================
# MAIN MENU
# =========================
def draw_main_menu():

    # Background
    window.blit(
        background_image,
        (0, 0)
    )

    # Dark overlay
    overlay = pygame.Surface(
        (GAME_WIDTH, GAME_HEIGHT)
    )

    overlay.set_alpha(70)

    overlay.fill(
        (0, 0, 0)
    )

    window.blit(
        overlay,
        (0, 0)
    )

    # =========================
    # TITLE
    # =========================

    title_text = title_font.render(
        "BURUNG FLEPY",
        True,
        "White"
    )

    title_rect = title_text.get_rect(
        center=(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2 - 100
        )
    )

    window.blit(
        title_text,
        title_rect
    )

    # =========================
    # BEST SCORE
    # =========================

    best_text = small_font.render(
        "Best Score: " + str(int(best_score)),
        True,
        "Yellow"
    )

    best_rect = best_text.get_rect(
        center=(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2 - 60
        )
    )

    window.blit(
        best_text,
        best_rect
    )

    # =========================
    # MULAI
    # =========================

    draw_button(
        start_button,
        "MULAI",
        (50, 180, 80)
    )

    # =========================
    # KELUAR
    # =========================

    draw_button(
        exit_button,
        "KELUAR",
        (200, 60, 60)
    )


# =========================
# DRAW GAME
# =========================
def draw_game():

    # Background
    window.blit(
        background_image,
        (0, 0)
    )

    # Bird
    window.blit(
        bird.img,
        bird
    )

    # Pipes
    for pipe in pipes:

        window.blit(
            pipe.img,
            pipe
        )

    # =========================
    # SCORE
    # =========================

    text_str = str(int(score))

    text_render = score_font.render(
        text_str,
        True,
        "White"
    )

    window.blit(
        text_render,
        (5, 0)
    )


# =========================
# GAME OVER SCREEN
# =========================
def draw_game_over():

    # Draw game first
    draw_game()

    # Dark overlay
    overlay = pygame.Surface(
        (GAME_WIDTH, GAME_HEIGHT)
    )

    overlay.set_alpha(170)

    overlay.fill(
        (0, 0, 0)
    )

    window.blit(
        overlay,
        (0, 0)
    )

    # =========================
    # GAME OVER
    # =========================

    game_over_text = game_over_font.render(
        "GAME OVER",
        True,
        "White"
    )

    game_over_rect = game_over_text.get_rect(
        center=(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2 - 100
        )
    )

    window.blit(
        game_over_text,
        game_over_rect
    )

    # =========================
    # SCORE
    # =========================

    score_text = button_font.render(
        "Score: " + str(int(score)),
        True,
        "White"
    )

    score_rect = score_text.get_rect(
        center=(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2 - 55
        )
    )

    window.blit(
        score_text,
        score_rect
    )

    # =========================
    # BEST SCORE
    # =========================

    best_text = button_font.render(
        "Best Score: " + str(int(best_score)),
        True,
        "Yellow"
    )

    best_rect = best_text.get_rect(
        center=(
            GAME_WIDTH // 2,
            GAME_HEIGHT // 2 - 20
        )
    )

    window.blit(
        best_text,
        best_rect
    )

    # =========================
    # MAIN LAGI
    # =========================

    draw_button(
        restart_button,
        "MAIN LAGI",
        (50, 200, 80)
    )

    # =========================
    # MENU UTAMA
    # =========================

    draw_button(
        menu_button,
        "MENU UTAMA",
        (70, 120, 200)
    )


# =========================
# RESET GAME
# =========================
def reset_game():

    global velocity_y
    global score
    global game_over

    # Reset bird
    bird.y = bird_y

    # Reset velocity
    velocity_y = 0

    # Clear pipes
    pipes.clear()

    # Reset score
    score = 0

    # Reset game over
    game_over = False


# =========================
# MOVE
# =========================
def move():

    global velocity_y
    global score
    global best_score
    global game_over

    # Gravity
    velocity_y += gravity

    # Bird movement
    bird.y += velocity_y

    # Prevent bird going above screen
    bird.y = max(
        bird.y,
        0
    )

    # Bird falls below screen
    if bird.y > GAME_HEIGHT:

        game_over = True

        if score > best_score:
            best_score = score

        return

    # Move pipes
    for pipe in pipes:

        pipe.x += velocity_x

        # =========================
        # SCORE
        # =========================

        if (
            not pipe.passed
            and bird.x > pipe.x + pipe.width
        ):

            score += 0.5

            pipe.passed = True

            if score > best_score:
                best_score = score

        # =========================
        # COLLISION
        # =========================

        if bird.colliderect(pipe):

            game_over = True

            if score > best_score:
                best_score = score

            return

    # Remove pipes outside screen
    while (
        len(pipes) > 0
        and pipes[0].x < -pipe_width
    ):

        pipes.pop(0)


# =========================
# CREATE PIPES
# =========================
def create_pipes():

    random_pipe_y = (
        pipe_y
        - pipe_height / 4
        - random.random()
        * (pipe_height / 2)
    )

    opening_space = GAME_HEIGHT / 4

    # Top pipe
    top_pipe = Pipe(
        top_pipe_image
    )

    top_pipe.y = random_pipe_y

    pipes.append(
        top_pipe
    )

    # Bottom pipe
    bottom_pipe = Pipe(
        bottom_pipe_image
    )

    bottom_pipe.y = (
        top_pipe.y
        + top_pipe.height
        + opening_space
    )

    pipes.append(
        bottom_pipe
    )


# =========================
# PIPE TIMER
# =========================
create_pipes_timer = pygame.USEREVENT + 0

pygame.time.set_timer(
    create_pipes_timer,
    1500
)


# =========================
# GAME LOOP
# =========================
while True:

    # =========================
    # EVENTS
    # =========================

    for event in pygame.event.get():

        # =========================
        # QUIT
        # =========================

        if event.type == pygame.QUIT:

            pygame.quit()

            exit()

        # =========================
        # CREATE PIPES
        # =========================

        if (
            event.type == create_pipes_timer
            and game_state == "playing"
            and not game_over
        ):

            create_pipes()

        # =========================
        # KEYBOARD
        # =========================

        if event.type == pygame.KEYDOWN:

            if event.key in (
                pygame.K_SPACE,
                pygame.K_UP
            ):

                if (
                    game_state == "playing"
                    and not game_over
                ):

                    velocity_y = -6

        # =========================
        # MOUSE CLICK
        # =========================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = event.pos

            # =========================
            # MAIN MENU
            # =========================

            if game_state == "menu":

                # MULAI
                if start_button.collidepoint(
                    mouse_pos
                ):

                    reset_game()

                    game_state = "playing"

                # KELUAR
                elif exit_button.collidepoint(
                    mouse_pos
                ):

                    pygame.quit()

                    exit()

            # =========================
            # GAME
            # =========================

            elif game_state == "playing":

                if game_over:

                    # MAIN LAGI
                    if restart_button.collidepoint(
                        mouse_pos
                    ):

                        reset_game()

                    # MENU UTAMA
                    elif menu_button.collidepoint(
                        mouse_pos
                    ):

                        reset_game()

                        game_state = "menu"

    # =========================
    # UPDATE GAME
    # =========================

    if (
        game_state == "playing"
        and not game_over
    ):

        move()

    # =========================
    # DRAW
    # =========================

    if game_state == "menu":

        draw_main_menu()

    elif game_state == "playing":

        if game_over:

            draw_game_over()

        else:

            draw_game()

    # =========================
    # UPDATE DISPLAY
    # =========================

    pygame.display.update()

    clock.tick(60)