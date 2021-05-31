from marshmallow import fields, pre_load
from marshmallow.validate import Length
from werkzeug.security import generate_password_hash

from .schema import ma
from utils.app.core import generate_id


class UserSchema(ma.Schema):
    user_id = fields.UUID(required=True)
    fullname = fields.String(required=True)
    username = fields.String(required=True, validate=Length(min=3))
    email = fields.Email(required=True)
    password = fields.Method(deserialize="load_password", validate=Length(min=6))
    role = fields.String()
    status = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def load_password(self, value):
        return generate_password_hash(value)

    @pre_load
    def process_input(self, data, **kwargs):
        email = data["email"].lower().strip()
        data.update(user_id=generate_id(), email=email)
        return data
