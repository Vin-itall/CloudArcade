
import pygame
import py_retro
import time
from flask import Flask, render_template, Response
from os import path

app = Flask(__name__)
# import os
# os.environ["SDL_VIDEODRIVER"] = "dummy"
queue =[]
libpath = '/home/atmc/CloudArcade/cores/snes9x_libretro.so'
rompath = '/home/atmc/CloudArcade/test roms/snes/A.smc'

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
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
        updateframe = py_retro.pygame_video.getFrame()
        yield (b'--frame\r\n'b'Content-Type: image/bmp\r\n\r\n' + updateframe + b'\r\n')
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
