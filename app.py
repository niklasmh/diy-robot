from flask import Flask, request, render_template
from flask_socketio import SocketIO
import test

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    print('connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('disconnected')


@socketio.on('move')
def handle_move(data):
    print('move: ' + data)


@socketio.on('locate')
def handle_locate():
    print('locate')
    print(test.f())


if __name__ == '__main__':
    socketio.run(app)
