from flask import Flask, render_template, request, session
from flask_socketio import SocketIO
import ssl

# import os
# print(os.getcwd())
import modules.FrameCutter as fc

# print('name :',__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

user_frame = {}

@app.route('/')
def index():
    return 'hello'

@app.route('/info')
def info():
    return 'info'

@app.route('/playing')
def hello():
    return render_template('cam-posenet/cam.html')

# @app.route('/exercise/result', method = ['GET'])
# def predict():
#     return 

@socketio.on('message')
def handle_connect(msg):
    print(msg)
    # user_frame['a'] = fc.FrameCutter(['leftHip', 'rightHip'], mask=5, threshold=6) #스쿼트
    user_frame['a'] = fc.FrameCutter(['leftWrist', 'rightWrist'], mask=5, threshold=10) # 덤벨 숄더...
    # user_frame['a'] = fc.FrameCutter(['leftWrist', 'rightWrist'], partial_min_score=0.3, num_action=5, mask=5, threshold=20) # PT 체조

@socketio.on('skeleton-data')
def handle_skeleton_data(data):
    user_frame['a'].add_frame(data)
    if user_frame['a'].check_rep():
        print('rep!!', user_frame['a'].features)
        user_frame['a'].initialize()

@socketio.on('disconnect')
def handle_disconnect():
    print('disconnect')
    
    del user_frame['a']

if __name__ == '__main__':
    socketio.run(app)