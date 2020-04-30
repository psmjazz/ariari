from googleapiclient.discovery import build
import google.oauth2.credentials
from flask import session, redirect
from application import db
from application.models.remain_vacation import RemainVacation
from application.models.used_vacation import UsedVacation
from application.models.user import User
from application.schemata.user import UserSchema
from application.views.google_api import credentials_to_dict
from marshmallow import Schema, fields, post_load, pprint, pre_load
import calendar
import datetime
import arrow


class GoogleCalendarEvent(object):
    def __init__(self, events):
        self.events = events
        self.created_at = str(arrow.now())[:10]

    def __repr__(self):
        return 'events : %r  /  created_at : %r' % (self.events, self.created_at)


class EventSchema(Schema):
    events = fields.List(fields.Dict)
    created_at = fields.Str()

    @post_load
    def make_events(self, data, **kwargs):
        return GoogleCalendarEvent(data['events'])


class GoogleCalendarCrawlingService:

    @classmethod
    def run(cls):
        events = cls.get_events()
        users = cls.sync_used_vacations(events=events)
        cls.calc_remain_vacation(users)

    @classmethod
    def get_events(cls):
        if 'credentials' not in session:
            return redirect('/authorize')

        credentials = google.oauth2.credentials.Credentials(
            **session['credentials'])

        service = build('calendar', 'v3', credentials=credentials)
        today = arrow.now()
        last_day = calendar.monthrange(today.year, today.month)

        # 'bluewhale.kr_0gbuu26gl7vue837u7f07mn360@group.calendar.google.com'  <== AIMMO Google calednar id
        events_result = service.events().list(
            calendarId='primary', timeMin=datetime.datetime(2020, 2, 1).isoformat() + 'Z',
            showDeleted=True, timeMax=datetime.datetime(2020, 2, 29).isoformat() + 'Z', maxResults=2500,
            singleEvents=True, orderBy='startTime'
        ).execute().get('items', [])

        # events_result = service.events().list(
        #     calendarId='primary', timeMin=datetime.datetime(today.year, today.month, 1).isoformat() + 'Z',
        #     showDeleted=True, timeMax=datetime.datetime(today.year, today.month, last_day[1]).isoformat() + 'Z', maxResults=2500,
        #     singleEvents=True, orderBy='startTime'
        # ).execute().get('items', [])

        events = GoogleCalendarEvent(events_result)
        event_schema = EventSchema()

        session['credentials'] = credentials_to_dict(credentials)
        session['events'] = event_schema.dump(events)
        return events

    @classmethod
    def sync_used_vacations(cls, events):
        event_schema = EventSchema()

        if 'events' not in session:
            events = cls.get_events().events
        elif event_schema.load(session['events']).created_at < str(arrow.now().shift(days=-1))[:10]:
            events = cls.get_events().events
        else:
            events = event_schema.load(session['events']).events

        used_vacation = UsedVacation.query.with_entities(UsedVacation.user_id, UsedVacation.event_id).all()
        users = list(set([x[0] for x in used_vacation if x]))
        event_id = [x[1] for x in used_vacation]

        for event in events:
            if "휴가" in event['summary'] or "연차" in event['summary'] or "반차" in event['summary'] or "민방위" in event['summary'] or "예비군" in event['summary']:
                if event['id'] in event_id:
                    if event['status'] == 'cancelled':
                        deleted_vacation = UsedVacation.query.filter_by(event_id=event['id']).one()
                        db.session.delete(deleted_vacation)
                        db.session.commit()
                        continue
                    else:
                        continue

                else:
                    user, summary, start, end, kind, event_id = cls.Attribute(event=event)
                    used_vacation = UsedVacation(user=user, summary=summary, start_date=start, end_date=end, kind=kind, event_id=event_id)
                    if user not in users:
                        users.append(user.google_id)

                if used_vacation is not None:
                    db.session.add(used_vacation)
                    db.session.commit()
        return users

    @classmethod
    def calc_remain_vacation(cls, users):
        for user_id in users:
            remain_vacation = RemainVacation.query.filter_by(user_id=user_id).one_or_none()

            year, total, remain = cls.calculate_vacation(remain_vacation.user)

            remain_vacation.number_of_years = year
            remain_vacation.total_vacation = total
            remain_vacation.remain_vacation = remain
            db.session.commit()

    @classmethod
    def Attribute(cls, event):
        user = User.query.filter_by(google_id=event['creator'].get('email')).first()
        summary = event['summary']
        start = event['start'].get('date') if event['start'].get('date') else event['start'].get('dateTime')[0:10]
        end = event['end'].get('date') if event['end'].get('date') else event['end'].get('dateTime')[0:10]
        kind = "연차"

        if "휴가" in summary and "대체" not in summary and "반차" not in summary:
            kind = "연차"
        if "연차" in summary and "대체" not in summary and "반차" not in summary:
            kind = "연차"
        if "년차" in summary and "대체" not in summary and "반차" not in summary:
            kind = "연차"
        if "반차" in summary:
            kind = "반차"
        if "대체휴가" in summary or "민방위" in summary or "예비군" in summary:
            kind = "공가"
        if "민방위" in summary or "예비군" in summary:
            kind = "공가"

        event_id = event['id']

        return user, summary, start, end, kind, event_id

    @classmethod
    def calculate_vacation(cls, user):

        years = datetime.datetime.today().year - user.entry_date.year

        if years != 0:
            total = 15 + (years // 2)
        else:
            working_day = (datetime.datetime(user.entry_date.year, 12, 31) - user.entry_date).days
            vacation = (15 * (working_day / 365)) if not calendar.isleap(user.entry_date.year) else (
                        15 * ((working_day + 1) / 366))
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


class RegisterUser:

    @classmethod
    def run(cls, data):
        user = cls.register_user(data)
        cls.register_remain_vacation(user)

        return user

    @classmethod
    def register_user(cls, data):
        user_schema = UserSchema()

        if data.get('entry_date'):
            data['entry_date'] = datetime.datetime.strptime(data.get('entry_date'), "%Y-%m-%d").isoformat()
        else:
            data['entry_date'] = datetime.datetime.today().isoformat()
        if not User.query.first():
            data['admin'] = 1

        user = user_schema.load(data)
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def register_remain_vacation(cls, user):

        years, total, remain = GoogleCalendarCrawlingService.calculate_vacation(user)

        remain_vacation = RemainVacation(user=user, number_of_years=years, total_vacation=total, remain_vacation=remain)
        db.session.add(remain_vacation)
        db.session.commit()

        return True