import pygame
import time

pygame.joystick.init()
print(pygame.joystick.get_count())
sdl_joy = pygame.joystick.Joystick(0)
sdl_joy.init()

for i in range(20):
    print(int(sdl_joy.get_button(i)))
    time.sleep(5)
