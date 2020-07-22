from flask import Flask, redirect, url_for, session, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, pprint
from flask_migrate import Migrate
from flask_restful import Api
from application.views.google_api import print_index_table
from flask_socketio import SocketIO
import os


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
socketio = SocketIO()
api = Api

#박상민 추가
import application.modules.FrameCutter as fc
user_frame = {}
#/박상민 추가

def create_app(mode='dev'):

    app = Flask(__name__)

    from application.config import config_name
    app.config.from_object(config_name[mode])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    from application.views.google_api import google_api_bp
    app.register_blueprint(google_api_bp)

    @app.route('/playing')
    def input_video():
        return render_template('cam.html')

    @app.route('/')
    def init():
        return render_template('homepage/index.html', user_name=None)

    @app.route('/<path:name>')
    def routing(name):
        path = 'homepage/' + str(name) + '.html'

        if 'user_name' in session:
            user_name = session['user_name']
        else:
            user_name = None

        return render_template(path, user_name=user_name)

    @app.route('/main')
    def main():
        if 'google_id' not in session and 'user_name' not in session:
            return redirect(url_for('google_api.authorize'))

        google_id = session['google_id']
        user_name = session['user_name']

        return render_template('homepage/index.html', user_name=user_name)

    #박상민 추가
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
            # 결과 데이터 전달
            socketio.emit('pose-result', {"score":1})
            user_frame['a'].initialize()


    @socketio.on('disconnect')
    def handle_disconnect():
        print('disconnect')

        del user_frame['a']
    #/박상민 추가

    return app



