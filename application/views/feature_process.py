from flask import Flask, render_template, request, session, current_app
from flask_socketio import SocketIO

import application.modules.FrameCutter as fc

socketio = SocketIO()
user_frame = {}


@socketio.on('message')
def handle_connect(msg):
    print(msg)
    # user_frame['a'] = fc.FrameCutter(['leftHip', 'rightHip'], mask=5, threshold=6) #스쿼트
    user_frame['a'] = fc.FrameCutter(['leftWrist', 'rightWrist'], mask=5, threshold=10)  # 덤벨 숄더...
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
