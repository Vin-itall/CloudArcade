import pygame
import py_retro
import time
from flask import Flask, render_template, Response
from os import path
from py_retro import core, pygame_input
import sys
import os
import googleapiclient.discovery
from pprint import pprint
import boto3

sqs = boto3.client(
    'sqs',
    'us-east-1',
    aws_access_key_id= 'AKIAQ7PPHJ5MGBKCJA7G',
    aws_secret_access_key= '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'
    # aws_session_token=SESSION_TOKEN,
)

def publish_message(Username, ip):
    global queue_url
    MessageAttributes = ip
    sqs.send_message(QueueUrl=queue_url, MessageGroupId=Username, MessageBody=MessageAttributes)
    print('Successfully uploaded')

os.environ["SDL_VIDEODRIVER"] = "dummy"
compute = googleapiclient.discovery.build('compute', 'v1')

# AWS Queue
# sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/067610562392/responseQueue.fifo'

request = compute.instances().get(project='cloudarcademaster-274423', zone='us-west3-a', instance='worker-1')
response = request.execute()
meta = response['metadata']['items']
ip = response['networkInterfaces'][0]['accessConfigs'][0]['natIP']

Username = meta[0]['value']
Game = meta[2]['value']
Core = meta[1]['value']
ip = 'http://' + ip + ':80/' + Username
publish_message(Username, ip)

app = Flask(__name__)

buttonStart = 0
buttonA = 0
buttonB = 0
buttonX = 0
buttonY = 0
buttonSelect =0
buttonUP =0
buttonDOWN =0
buttonLEFT =0
buttonRIGHT =0
buttonQuit = 0


libpath = '/home/vjachary/CloudArcade/Worker/Cores/' + str(Core) +'.so'
rompath = '/home/vjachary/CloudArcade/Worker/test roms/'+str(Core)+'/'+str(Game)

@app.route('/'+str(Username))
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/start_action')
def start_action():
    global buttonStart
    buttonStart = 1
    return ("nothing")

@app.route('/a_action')
def a_action():
    global buttonA
    buttonA = 1
    return ("nothing")

@app.route('/b_action')
def b_action():
    global buttonB
    buttonB = 1
    return ("nothing")

@app.route('/x_action')
def x_action():
    global buttonX
    buttonX = 1
    return ("nothing")

@app.route('/y_action')
def y_action():
    global buttonY
    buttonY = 1
    return ("nothing")

@app.route('/select_action')
def select_action():
    global buttonSelect
    buttonSelect = 1
    return ("nothing")

@app.route('/u_action')
def u_action():
    global buttonUP
    buttonUP = 1
    return ("nothing")

@app.route('/d_action')
def d_action():
    global buttonDOWN
    buttonDOWN = 1
    return ("nothing")

@app.route('/l_action')
def l_action():
    global buttonLEFT
    buttonLEFT = 1
    return ("nothing")

@app.route('/r_action')
def r_action():
    global buttonRIGHT
    buttonRIGHT = 1
    return ("nothing")

@app.route('/q_action')
def q_action():
    global buttonQuit
    os.system("shutdown now -h")
    return ("nothing")


def clearAll():
    global buttonStart,buttonA,buttonB,buttonX,buttonY,buttonSelect,buttonUP,buttonDOWN,buttonLEFT,buttonRIGHT
    buttonStart = 0
    buttonA = 0
    buttonB = 0
    buttonX = 0
    buttonY = 0
    buttonSelect =0
    buttonUP =0
    buttonDOWN =0
    buttonLEFT =0
    buttonRIGHT =0

def getCache():
    global buttonStart, buttonA, buttonB, buttonX, buttonY, buttonSelect, buttonUP, buttonDOWN, buttonLEFT, buttonRIGHT,buttonQuit
    ccache = customcache = [[0] * 20 for i in range(8)]
    if buttonStart == 1:
        ccache[0][3] = 1
    else:
        ccache[0][3] = 0
    if buttonA == 1:
        ccache[0][8] = 1
    else:
        ccache[0][8] = 0
    if buttonB == 1:
        ccache[0][0] = 1
    else:
        ccache[0][0] = 0
    if buttonX == 1:
        ccache[0][9] = 1
    else:
        ccache[0][9] = 0
    if buttonY == 1:
        ccache[0][1] = 1
    else:
        ccache[0][1] = 0
    if buttonSelect == 1:
        ccache[0][2] = 1
    else:
        ccache[0][2] = 0
    if buttonUP == 1:
        ccache[0][4] = 1
    else:
        ccache[0][4] = 0
    if buttonDOWN == 1:
        ccache[0][5] = 1
    else:
        ccache[0][5] = 0
    if buttonLEFT == 1:
        ccache[0][6] = 1
    else:
        ccache[0][6] = 0
    if buttonRIGHT == 1:
        ccache[0][7] = 1
    else:
        ccache[0][7] = 0
    return ccache


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
    MAX_MAPPINGS = 20
    MAX_PLAYERS = 8
    while running:
        customcache = [[0] * MAX_MAPPINGS for i in range(MAX_PLAYERS)]
        # pygame.event.pump()
        es.run()
        pygame.display.flip()
        pygame_input.receive_spadcache(getCache())
        clearAll()
        updateframe = py_retro.pygame_video.getFrame()
        yield (b'--frame\r\n'b'Content-Type: image/bmp\r\n\r\n' + updateframe + b'\r\n')
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
