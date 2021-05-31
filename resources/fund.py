from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required

from models.fund import FundModel, CheckModel, BankTransferModel
from schemas.fund import FundSchema, CheckSchema, BankTransferSchema
from utils.http.responses import Response


class FundListResource(Resource):
    @jwt_required()
    def get(self):
        model = FundModel()
        schema_list = FundSchema(many=True)
        data = schema_list.dump(model.get_all())
        return Response.get_message(200, message="OK", data=data)

    @jwt_required()
    @use_args(
        {
            "name": fields.Str(required=True),
            "amount": fields.Str(required=True),
            "description": fields.Str(),
            "payment_type": fields.Str(required=True),
            "institution_id": fields.Str(required=True),
        },
        location="json",
    )
    def post(self, args):
        model = FundModel()
        schema = FundSchema()

        if not args:
            return Response.get_message(400, message="No input data provided")

        data = schema.load(args)

        try:
            fund_id = model.save(**data)

            if not fund_id:
                return Response.get_error(422, error="Something failed")

            query = model.get_by("fund_id", value=fund_id)
            serialized = schema.dump(query)

            return Response.get_message(
                201, message="Created Successfully", data=serialized
            )
        except Exception as error:
            return Response.get_error(400, error)


class CheckListResource(Resource):
    @jwt_required()
    def get(self, fund_id):
        model = CheckModel()
        schema = CheckSchema()

        query = model.get_by("fund_id", value=fund_id, condition="funds")

        if not query:
            return Response.get_message(404, message="Check not found")

        serialized = schema.dump(query)
        return Response.get_message(200, message="OK", data=serialized)

    @jwt_required()
    @use_args(
        {
            "number": fields.Str(required=True),
            "recipient": fields.Str(required=True),
        },
        location="json",
    )
    def post(self, args, fund_id):
        fund_model = FundModel()
        check_model = CheckModel()
        banktransfer_model = BankTransferModel()
        schema = CheckSchema()

        if not args:
            return Response.get_message(400, message="No input data provided")

        if not fund_model.search_by("fund_id", value=fund_id):
            return Response.get_message(404, message="Unable to find this fund.")

        if check_model.search_by("fund_id", value=fund_id):
            return Response.get_message(302, message="A check was already saved for this fund.")

        if banktransfer_model.search_by("fund_id", value=fund_id):
            return Response.get_message(302, message="A bank transfer was already saved for this fund.")

        args.update(fund_id=fund_id)

        data = schema.load(args)

        try:
            check_id = check_model.save(**data)

            if not check_id:
                return Response.get_error(422, error="Something failed")

            query = check_model.get_by("check_id", value=check_id)
            serialized = schema.dump(query)

            return Response.get_message(
                201, message="Created Successfully", data=serialized
            )
        except Exception as error:
            return Response.get_error(400, error)

    
class CheckResource(Resource):
    @jwt_required()
    def get(self, check_id):
        model = CheckModel()
        schema = CheckSchema()

        query = model.get_by("check_id", value=check_id, condition="checks")

        if not query:
            return Response.get_message(404, message="Check not found")

        serialized = schema.dump(query)
        return Response.get_message(200, message="OK", data=serialized)


class BankTransferListResource(Resource):
    @jwt_required()
    def get(self, banktransfer_id):
        model = BankTransferModel()
        schema = BankTransferSchema()

        query = model.get_by("bank_transfer_id", value=banktransfer_id, condition="funds")

        if not query:
            return Response.get_message(404, message="Bank transfer not found")

        serialized = schema.dump(query)
        return Response.get_message(200, message="OK", data=serialized)

    @jwt_required()
    @use_args(
        {
            "bank_name": fields.Str(required=True),
            "account_name": fields.Str(required=True)
        },
        location="json",
    )
    def post(self, args, fund_id):
        fund_model = FundModel()
        check_model = CheckModel()
        banktransfer_model = BankTransferModel()
        schema = BankTransferSchema()

        if not args:
            return Response.get_message(400, message="No input data provided")

        if not fund_model.search_by("fund_id", value=fund_id):
            return Response.get_message(404, message="Unable to find this fund.")

        if check_model.search_by("fund_id", value=fund_id):
            return Response.get_message(302, message="A check was already saved for this fund.")

        if banktransfer_model.search_by("fund_id", value=fund_id):
            return Response.get_message(302, message="A bank transfer was already saved for this fund.")

        args.update(fund_id=fund_id)

        data = schema.load(args)

        try:
            bank_transfer_id = banktransfer_model.save(**data)

            if not id:
                return Response.get_error(422, error="Something failed")

            query = banktransfer_model.get_by("bank_transfer_id", value=bank_transfer_id)
            serialized = schema.dump(query)

            return Response.get_message(
                201, message="Created Successfully", data=serialized
            )
        except Exception as error:
            return Response.get_error(400, error)


class BankTransferResource(Resource):
    @jwt_required()
    def get(self, banktransfer_id):
        model = BankTransferModel()
        schema = BankTransferSchema()

        query = model.get_by("bank_transfer_id", value=banktransfer_id, condition="bank_transfers")

        if not query:
            return Response.get_message(404, message="Check not found")

        serialized = schema.dump(query)
        return Response.get_message(200, message="OK", data=serialized)
