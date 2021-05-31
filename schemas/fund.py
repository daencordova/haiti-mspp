from marshmallow import fields, pre_load

from schemas.schema import ma
from utils.app.core import generate_id


class FundSchema(ma.Schema):

    fund_id = fields.UUID(required=True)
    name = fields.String(required=True)
    amount = fields.String(required=True)
    description = fields.String()
    payment_type = fields.String(required=True)
    status = fields.Boolean()
    institution_id = fields.UUID(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @pre_load
    def process_input(self, data, **kwargs):
        data.update(fund_id=generate_id())
        return data


class CheckSchema(ma.Schema):

    check_id = fields.UUID(required=True)
    number = fields.String(required=True)
    recipient = fields.String(required=True)
    fund_id = fields.UUID(required=True)
    fund = fields.Nested(FundSchema)

    @pre_load
    def process_input(self, data, **kwargs):
        data.update(check_id=generate_id())
        return data


class BankTransferSchema(ma.Schema):

    bank_transfer_id = fields.UUID(required=True)
    bank_name = fields.String(required=True)
    account_name = fields.String(required=True)
    fund_id = fields.UUID(required=True)
    fund = fields.Nested(FundSchema)

    @pre_load
    def process_input(self, data, **kwargs):
        data.update(bank_transfer_id=generate_id())
        return data
