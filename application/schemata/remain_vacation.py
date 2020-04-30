from flask_marshmallow import Marshmallow
from application import ma
from application.models.remain_vacation import *


class RemainVacationSchema(ma.ModelSchema):
    class Meta:
        model = RemainVacation
