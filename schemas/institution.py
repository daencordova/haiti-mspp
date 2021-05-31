from marshmallow import fields, pre_load

from flask_jwt_extended import get_jwt_identity

from schemas.schema import ma
from utils.app.core import generate_id


class InstitutionSchema(ma.Schema):

    institution_id = fields.UUID(required=True)
    code = fields.String(required=True)
    name = fields.String(required=True)
    authorising_officer = fields.String(required=True)
    email = fields.String()
    telephone = fields.String()
    website = fields.String()
    address = fields.String()
    status = fields.Boolean()
    user_id = fields.UUID(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @pre_load
    def process_input(self, data, **kwargs):
        data.update(institution_id=generate_id(), user_id=get_jwt_identity())
        return data
