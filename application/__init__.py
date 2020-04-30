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

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    from application.views.user import user_bp
    app.register_blueprint(user_bp)

    from application.views.used_vacation import used_vacation_bp
    app.register_blueprint(used_vacation_bp)

    from application.views.remain_vacation import remain_vacation_bp
    app.register_blueprint(remain_vacation_bp)

    from application.views.google_api import google_api_bp
    app.register_blueprint(google_api_bp)

    from application.models.user import User

    @app.route('/')
    def init():
        return print_index_table()

    @app.route('/main')
    def main():
        if 'google_id' not in session:
            return redirect(url_for('google_api.authorize'))

        google_id = session['google_id']
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            return render_template('user/user_register.html', g_id=google_id, google_id=google_id)
        elif user.admin:
            target_id = "temp" if not request.args.get('사용자 번호') else str(request.args.get('사용자 번호'))
            return render_template('main_page/admin_user_main.html', id=str(user.id))
        elif not user.admin:
            return render_template('main_page/general_user_main.html', id=str(user.id))

    return app



