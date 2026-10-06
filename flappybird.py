import pygame
from sys import exit

#game variables
GAME_WIDTH = 360
GAME_HEIGHT = 640

#game images
background_image =  pygame.image.load("flappybirdbg.png")

def draw():
    window.blit(background_image,(0,0))

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
