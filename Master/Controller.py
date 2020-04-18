from flask import Flask, render_template, Response, request
Controller = Flask(__name__)

@Controller.route('/')
def index():
    return render_template('MainPage.html')


@Controller.route('/login_action')
def login():
    username = request.args.get('username')
    game = request.args.get('game')
    return ('nothing')

if __name__ == '__main__':
    Controller.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
