import pygame
from sys import exit
import random

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
background_image = pygame.image.load(
    "flappybirdbg.png"
)

bird_image = pygame.image.load(
    "flappybird.png"
)

bird_image = pygame.transform.scale(
    bird_image,
    (bird_width, bird_height)
)

top_pipe_image = pygame.image.load(
    "toppipe.png"
)

top_pipe_image = pygame.transform.scale(
    top_pipe_image,
    (pipe_width, pipe_height)
)

bottom_pipe_image = pygame.image.load(
    "bottompipe.png"
)

bottom_pipe_image = pygame.transform.scale(
    bottom_pipe_image,
    (pipe_width, pipe_height)
)


# =========================
# GAME LOGIC
# =========================
bird = Bird(bird_image)

pipes = []

velocity_x = -2
velocity_y = 0
gravity = 0.4

score = 0
game_over = False


# =========================
# FONT
# =========================
score_font = pygame.font.SysFont(
    "Comic Sans MS",
    45
)

game_over_font = pygame.font.SysFont(
    "Comic Sans MS",
    40,
    bold=True
)

button_font = pygame.font.SysFont(
    "Comic Sans MS",
    25,
    bold=True
)


# =========================
# MAIN LAGI BUTTON
# =========================
button_rect = pygame.Rect(
    GAME_WIDTH // 2 - 100,
    GAME_HEIGHT // 2,
    200,
    60
)


# =========================
# DRAW
# =========================
def draw():

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

    # Score
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
    # GAME OVER POPUP
    # =========================
    if game_over:

        # Dark transparent overlay
        overlay = pygame.Surface(
            (GAME_WIDTH, GAME_HEIGHT)
        )

        overlay.set_alpha(160)

        overlay.fill(
            (0, 0, 0)
        )

        window.blit(
            overlay,
            (0, 0)
        )

        # GAME OVER TEXT
        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            "White"
        )

        game_over_text_rect = game_over_text.get_rect(
            center=(
                GAME_WIDTH // 2,
                GAME_HEIGHT // 2 - 70
            )
        )

        window.blit(
            game_over_text,
            game_over_text_rect
        )

        # SCORE
        score_text = button_font.render(
            "Score: " + str(int(score)),
            True,
            "White"
        )

        score_text_rect = score_text.get_rect(
            center=(
                GAME_WIDTH // 2,
                GAME_HEIGHT // 2 - 25
            )
        )

        window.blit(
            score_text,
            score_text_rect
        )

        # =========================
        # BUTTON MAIN LAGI
        # =========================

        pygame.draw.rect(
            window,
            (50, 200, 80),
            button_rect,
            border_radius=10
        )

        # Button text
        button_text = button_font.render(
            "MAIN LAGI",
            True,
            "White"
        )

        button_text_rect = button_text.get_rect(
            center=button_rect.center
        )

        window.blit(
            button_text,
            button_text_rect
        )


# =========================
# MOVE
# =========================
def move():

    global velocity_y
    global score
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

        return

    # Move pipes
    for pipe in pipes:

        pipe.x += velocity_x

        # Score
        if not pipe.passed and bird.x > pipe.x + pipe.width:

            score += 0.5

            pipe.passed = True

        # Collision
        if bird.colliderect(pipe):

            game_over = True

            return

    # Remove pipes that are outside screen
    while len(pipes) > 0 and pipes[0].x < -pipe_width:

        pipes.pop(0)


# =========================
# CREATE PIPES
# =========================
def create_pipes():

    random_pipe_y = (
        pipe_y
        - pipe_height / 4
        - random.random() * (pipe_height / 2)
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

                # Only fly when game is running
                if not game_over:

                    velocity_y = -6

        # =========================
        # MOUSE CLICK
        # =========================
        if event.type == pygame.MOUSEBUTTONDOWN:

            if game_over:

                # Check MAIN LAGI button
                if button_rect.collidepoint(
                    event.pos
                ):

                    # Reset bird
                    bird.y = bird_y

                    # Reset velocity
                    velocity_y = 0

                    # Clear pipes
                    pipes.clear()

                    # Reset score
                    score = 0

                    # Start game again
                    game_over = False

    # =========================
    # UPDATE GAME
    # =========================
    if not game_over:

        move()

    # =========================
    # DRAW
    # =========================
    draw()

    pygame.display.update()

    clock.tick(60)
