from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from flask_jwt_extended import jwt_required

from models.institution import InstitutionModel
from schemas.institution import InstitutionSchema
from utils.http.responses import Response


class InstitutionListResource(Resource):
    @jwt_required()
    def get(self):
        model = InstitutionModel()
        schema_list = InstitutionSchema(many=True)
        data = schema_list.dump(model.get_all())
        return Response.get_message(200, message="OK", data=data)

    @jwt_required()
    @use_args(
        {
            "code": fields.Str(required=True),
            "name": fields.Str(required=True),
            "authorising_officer": fields.Str(required=True),
            "email": fields.Str(),
            "telephone": fields.Str(),
            "website": fields.Str(),
            "address": fields.Str(),
        },
        location="json",
    )
    def post(self, args):
        model = InstitutionModel()
        schema = InstitutionSchema()

        if not args:
            return Response.get_message(400, message="No input data provided")

        data = schema.load(args)

        if model.search_by("code", value=data["code"]):
            return Response.get_message(302, message="This code is already being used")

        if model.search_by("name", value=data["name"]):
            return Response.get_message(302, message="This name is already being used")

        try:
            institution_id = model.save(**data)

            if not institution_id:
                return Response.get_error(422, error="Something failed")

            query = model.get_by("institution_id", value=institution_id)
            serialized = schema.dump(query)

            return Response.get_message(
                201, message="Created Successfully", data=serialized
            )
        except Exception as error:
            return Response.get_error(400, error)


class InstitutionResource(Resource):
    @jwt_required()
    def get(self, institution_id):
        model = InstitutionModel()
        schema = InstitutionSchema()

        query = model.get_by("institution_id", value=institution_id)

        if not query:
            return Response.get_message(404, message="Institution not found")

        serialized = schema.dump(query)
        return Response.get_message(200, message="OK", data=serialized)

    @jwt_required()
    @use_args(
        {
            "code": fields.Str(required=True),
            "name": fields.Str(required=True),
            "authorising_officer": fields.Str(required=True),
            "email": fields.Str(),
            "telephone": fields.Str(),
            "website": fields.Str(),
            "address": fields.Str(),
            "status": fields.Bool(),
        },
        location="json",
    )
    def patch(self, institution_id, args):
        model = InstitutionModel()
        schema = InstitutionSchema()

        if model.search_by("institution_id", value=institution_id):
            return Response.get_message(404, message="Unable to find this institution")

        if not args:
            return Response.get_message(400, message="No input data provided")

        data = schema.load(args)

        try:
            result = model.update(institution_id, **data)

            if not result:
                return Response.get_error(422, error="Something failed")

            query = model.get_by("institution_id", value=institution_id)
            serialized = schema.dump(query)

            return Response.get_message(
                200, message="Modified Successfully", data=serialized
            )
        except Exception as error:
            return Response.get_error(304, error)

    @jwt_required()
    def delete(self, institution_id):
        model = InstitutionModel()
        query = model.get_by("institution_id", value=institution_id)

        if not query:
            return Response.get_message(404, message="Unable to find this institution")

        try:
            result = model.delete(institution_id)

            if not result:
                return Response.get_error(422, error="Something failed")

            return Response.get_message(204, message="Deleted Successfully")
        except Exception as error:
            return Response.get_error(422, error)
