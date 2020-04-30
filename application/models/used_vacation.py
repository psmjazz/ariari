from application import db
from application.models.user import User


class UsedVacation(db.Model):
    __table_name__ = 'used_vacation'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(30), db.ForeignKey('user.google_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('used_vacations', cascade='all, delete', lazy=True))
    summary = db.Column(db.String(30), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    kind = db.Column(db.String(10), nullable=False)
    reference = db.Column(db.String(30), nullable=True)
    event_id = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "Google id : %r  /  내용 : %r  /  시작일 : %r  /  종료일 : %r  /  휴가 종류 : %r" % (self.user.google_id, self.summary, str(self.start_date), str(self.end_date), self.kind)

    def get_period(self):
        period = self.end_date - self.start_date

        if period.days < 0:
            raise Exception("End date earlier than Start date")

        return period
