import pygame

pygame.init()

w, h = 900, 600 ##Width and height that will be used to create screen.
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Pong")

running = True

while running:
    screen.fill((255, 255, 0))



