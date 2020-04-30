from application.schemata.remain_vacation import RemainVacationSchema
from application.models.remain_vacation import RemainVacation
from application.models.used_vacation import UsedVacation
from application.models.user import User
from application import db, api
from flask import Blueprint, Response, request, render_template, make_response, current_app
from flask_restful import Resource
import datetime
import calendar

remain_vacation_bp = Blueprint("remain_vacation", __name__, url_prefix='/users/vacations/')
remain_vacation_schema = RemainVacationSchema()
api = api(remain_vacation_bp)
headers = {'Content-Type': 'text/html'}


class UserVacation(Resource):
    def get(self, id=None):
        data = request.args
        request_user = User.query.filter_by(id=data.get('id')).one_or_none()

        if not request_user.admin:
            if id != data.get('id') or id is None:
                return Response("No Authority", 401, mimetype='application/json')

            target_user = User.query.get(id)
            remain_vacation = RemainVacation.query.filter_by(user=target_user).one_or_none()
            return make_response(render_template('user/specific_user_result.html', title="남은 휴가", result=remain_vacation, request_user=request_user, id=str(request_user.id)), 200, headers)

        elif request_user.admin:
            if id is None:
                remain_vacation = RemainVacation.query.all()
                return make_response(render_template('user/multiple_user_result.html', title="남은 휴가", result=remain_vacation, user=request_user, id=str(request_user.id)), 200, headers)
            else:
                target_user = User.query.get(id)
                remain_vacation = RemainVacation.query.filter_by(user=target_user).one_or_none()
                if id != data.get('id'):
                    target_id = data.get('사용자 번호')
                    result = [remain_vacation]
                    return make_response(render_template('user/select_specific_user.html', title='사용자 정보', result=result, target_id=str(target_id), id=str(request_user.id)), 200, headers)
                else:
                    return make_response(render_template('user/specific_user_result.html', title="남은 휴가", result=remain_vacation, request_user=request_user, id=str(request_user.id)), 200, headers)

    def put(self, id=None):
        if id:
            user = User.query.get(id)
        else:
            user = User.query.get(request.form.get('id'))

        remain_vacation = RemainVacation.query.filter_by(user=user).one()

        year, total, remain = calculate_vacation(user)

        remain_vacation.number_of_years = year
        remain_vacation.total_vacation = total
        remain_vacation.remain_vacation = remain

        db.session.commit()

    def delete(self, id):
        user = User.query.get(id)
        remain_vacation = RemainVacation.query.filter_by(user=user).delete()

        db.session.commit()

        return Response(remain_vacation_schema.dumps(remain_vacation), 200, mimetype='application/json')


api.add_resource(UserVacation, '/remain', '/<string:id>/remain', endpoint='user_vacation')


def calculate_vacation(user):
    user = user
    years = datetime.datetime.today().year - user.entry_date.year

    if years != 0:
        total = 15 + (years // 2)
    else:
        working_day = (datetime.datetime(user.entry_date.year, 12, 31) - user.entry_date).days
        vacation = (15 * (working_day / 365)) if not calendar.isleap(user.entry_date.year) else (15 * ((working_day+1) / 366))
        flag = vacation - int(vacation)
        total = 0

        if 0.0 < flag <= 0.5:
            total = int(vacation) + 0.5
        elif 0.5 < flag < 1.0:
            total = int(vacation) + 1
        elif flag == 0.0:
            total = vacation

    remain = total - len(UsedVacation.query.filter_by(user=user, kind="연차").all())
    remain = remain - (0.5 * len(UsedVacation.query.filter_by(user=user, kind="반차").all()))

    return years, total, remain
