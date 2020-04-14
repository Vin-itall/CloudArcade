
import time
from flask import Flask, render_template, Response
from os import path
app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

count = 0
def gen():
    global count
    """Video streaming generator function."""
    while True:
        imp = '/home/atmc/Desktop/CloudArcade-master/Code/bmps/'+str(count + 1) + '.bmp'
        if path.exists(imp):
            frame = open(imp, 'rb').read()
            count+=1
            yield (b'--frame\r\n'b'Content-Type: image/bmp\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.0167)
        else:
            lframe = open('/home/atmc/Desktop/CloudArcade-master/Code/default/default.bmp', 'rb').read()
            print('dus bahane')
            yield (b'--frame\r\n'b'Content-Type: image/bmp\r\n\r\n' + lframe + b'\r\n')
            time.sleep(0.00001)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
