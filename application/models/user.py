from application import db
import datetime


class User(db.Model):
    __table_name__ = 'user'
    __table_args__ = (
        db.UniqueConstraint('google_id', 'en_name', name="unique_user_constraint"),
    )
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(30), nullable=False, unique=True)
    ko_name = db.Column(db.String(10), default="None")
    en_name = db.Column(db.String(10), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.today())
    admin = db.Column(db.Integer, default=False)

    def __repr__(self):
        return "사용자 번호 : %r  /  Google ID : %r  /  한글이름 : %r  /  영어이름 : %r  /  입사일 : %r  /  관리자 여부 : %r" %(self.id, self.google_id, self.ko_name, self.en_name, str(self.entry_date)[:10], bool(self.admin))

    def get_id(self):
        return self.id

    def get_google_id(self):
        return self.google_id

    def get_en_name(self):
        return self.en_name
