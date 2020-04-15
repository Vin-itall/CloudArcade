import pygame
from pygame.locals import *

pygame.init()
display = pygame.display.set_mode((100,100))
sdljoy = pygame.key

while True:
	pygame.event.pump()
	if sdljoy.get_pressed()[pygame.K_DOWN]:
		break