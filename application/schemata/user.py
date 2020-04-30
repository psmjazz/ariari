from application import ma
from application.models.user import *


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


