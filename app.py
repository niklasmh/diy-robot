from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import find_robot_position

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


def get_position(new_image=True):
    position = find_robot_position.locate(
        assumed_position=[0, 0],
        capture_new_image=new_image
    )
    if position:
        emit("position", str(position[0]) + "," + str(position[1]))
    else:
        emit("position-failed", "Could not find position")


@socketio.on('locate')
def handle_locate():
    print('locate')
    get_position(new_image=True)


@socketio.on('relocate')
def handle_locate():
    print('relocate')
    get_position(new_image=False)


if __name__ == '__main__':
    socketio.run(app)
