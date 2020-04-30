import arrow

from application.schemata.used_vacation import UsedVacationSchema
from application.models.used_vacation import UsedVacation
from application.models.user import User
from application import db, api
from application.service import GoogleCalendarCrawlingService
# from application.views.google_api import session, get_event, GoogleCalendarEvent
from flask import Blueprint, Response, request, redirect, url_for, make_response, render_template, current_app
from flask_restful import Resource


used_vacation_bp = Blueprint("used_vacation", __name__, url_prefix='/users/vacations/')
used_vacation_schema = UsedVacationSchema()
api = api(used_vacation_bp)
maxResult = 2500
headers = {'Content-type': 'text/html'}
google_service = GoogleCalendarCrawlingService()


class UserUsedVacation(Resource):
    def get(self, id=None):
        data = request.args
        request_user = User.query.get(data.get('id'))

        if request_user.admin == False and id != data.get('id'):
            return Response("No Authority", 401)

        if id is None:
            used_vacation = UsedVacation.query.all()
            return make_response(render_template('user/multiple_user_result.html', title="사용한 전체 휴가", result=used_vacation, id=str(request_user.id), user=request_user), 201, headers)

        if id is not None:
            target_user = User.query.get(id)
            used_vacation = UsedVacation.query.filter_by(user=target_user).all()
            if id != data.get('id'):
                target_id = data.get('사용자 번호')
                return make_response(render_template('user/select_specific_user.html', title='사용자 정보', result=used_vacation, target_id=str(target_id), id=str(request_user.id)), 200, headers)
            else:
                return make_response(render_template('user/multiple_user_result.html', title="사용한 휴가", result=used_vacation, id=str(target_user.id), user=request_user), 201, headers)

    def post(self, id=None):
        google_service.run()
        return redirect(url_for('main'))


api.add_resource(UserUsedVacation, '/used', '/<string:id>/used', endpoint='used')