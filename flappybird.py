import pygame
from sys import exit

#game variables
GAME_WIDTH = 360
GAME_HEIGHT = 640

#bird class
bird_x = GAME_WIDTH/8
bird_y = GAME_HEIGHT/2
bird_width = 34 #17/12
bird_height = 24

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img


#game images
background_image =  pygame.image.load("flappybirdbg.png")
bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

#game logic
bird = Bird(bird_image)

def draw():
    window.blit(background_image,(0,0))
    window.blit(bird.img, bird)

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Burung Flepy")
clock = pygame.time.Clock()

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
    draw()
    pygame.display.update()
    clock.tick(60) #60 fps
