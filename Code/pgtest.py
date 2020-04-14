
import pygame
import py_retro
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"

libpath = '/home/atmc/Desktop/CloudArcade-master/cores/snes9x_libretro.so'
rompath = '/home/atmc/Desktop/CloudArcade-master/roms/snes/A.smc'


def main():
    es = py_retro.core.EmulatedSystem(libpath)
    es.load_game_normal(path=rompath)

    screen = py_retro.pygame_video.pygame_display_set_mode(es, False)

    py_retro.pygame_video.set_video_refresh_surface(es, screen)
    # py_retro.portaudio_audio.set_audio_sample_internal(es)
    py_retro.pygame_input.set_input_poll_joystick(es)

    # run each frame until closed.
    running = True
    fps = es.get_av_info()['fps'] or 60
    clock = pygame.time.Clock()

    while running:
        es.run()
        pygame.display.flip()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
