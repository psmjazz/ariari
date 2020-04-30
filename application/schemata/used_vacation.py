from flask_marshmallow import Marshmallow
from application import ma
from application.models.used_vacation import *


class UsedVacationSchema(ma.ModelSchema):
    class Meta:
        model = UsedVacation
