from flask import Flask, redirect, url_for, session, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, pprint
from flask_migrate import Migrate
from flask_restful import Api
from application.views.google_api import print_index_table
import os


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = Api


def create_app(mode='dev'):

    app = Flask(__name__)

    from application.config import config_name
    app.config.from_object(config_name[mode])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    import numpy as np

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    from application.views.google_api import google_api_bp
    app.register_blueprint(google_api_bp)

    from application.models.user import User

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

    return app



