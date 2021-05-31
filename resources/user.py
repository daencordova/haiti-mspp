from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash
from webargs import fields, validate
from webargs.flaskparser import use_args
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)

from models.user import UserModel
from schemas.user import UserSchema
from utils.http.responses import Response
from utils.auth.decorators import admin_required


BLOCKLIST = set()


class UserRegisterResource(Resource):
    @admin_required()
    @use_args(
        {
            "fullname": fields.Str(required=True),
            "username": fields.Str(required=True),
            "email": fields.Str(required=True),
            "password": fields.Str(required=True, validate=lambda p: len(p) >= 6),
            "role": fields.Str(required=True),
        },
        location="json",
    )
    def post(self, args):
        model = UserModel()
        schema = UserSchema()

        if not args:
            return Response.get_message(400, message="No input data provided")

        data = schema.load(args)

        if model.search_by("username", value=data["username"]):
            return Response.get_message(302, message="This username already exists")

        if model.search_by("email", value=data["email"]):
            return Response.get_message(302, message="This email already exists")

        try:
            user_id = model.save(**data)

            if not user_id:
                return Response.get_error(422, error="Something failed")

            query = model.get_by("user_id", value=user_id)
            serialized = schema.dump(query)

            return Response.get_message(
                201, message="Created Successfully", data=serialized
            )
        except Exception as error:
            return Response.get_error(400, error)


class UserLoginResource(Resource):
    @use_args(
        {"username": fields.Str(required=True), "password": fields.Str(required=True)},
        location="json",
    )
    def post(self, args):
        model = UserModel()

        if "username" not in args or "password" not in args:
            return Response.get_message(400, message="No input data provided")

        query = model.get_for_login(args["username"])
        pass_check = check_password_hash(query["password"], args["password"])

        if not query or not pass_check:
            return Response.get_message(403, message="Invalid credentials")

        access_token = create_access_token(identity=query)
        refresh_token = create_refresh_token(identity=query)

        data = {
            "user_id": query["user_id"],
            "email": query["email"],
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return Response.get_message(200, message="Logged In Successfully", data=data)


class UserRefreshAccessTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        model = UserModel()
        user_id = get_jwt_identity()

        if not user_id:
            return Response.get_message(401, message="Invalid user")

        query = model.get_by("user_id", value=user_id)
        token = create_access_token(identity=query)
        return Response.get_message(
            200, message="Token Refreshed", data={"token": token}
        )


class UserRevokeAccessTokenResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]

        if not jti:
            message = "Something bad occurred while trying to log you out"
            return Response.get_message(400, message=message)

        BLOCKLIST.add(jti)
        return Response.get_message(200, message="Logged Out Successfully")


class UserCurrentInfoResource(Resource):
    @jwt_required()
    def get(self):
        model = UserModel()
        schema = UserSchema()

        query = model.get_by("user_id", value=get_jwt_identity())

        if not query:
            return Response.get_message(404, message="Unable to find this user")

        serialized = schema.dump(query)
        return Response.get_message(200, message="OK", data=serialized)

    @jwt_required()
    @use_args(
        {
            "old_password": fields.Str(required=True),
            "new_password": fields.Str(required=True),
        },
        location="json",
    )
    def patch(self, args):
        model = UserModel()

        user_id = get_jwt_identity()
        query = model.get_password(user_id=user_id)

        if not query:
            return Response.get_message(404, message="Unable to find this user")

        if "old_password" not in args or "new_password" not in args:
            return Response.get_message(400, message="No input data provided")

        pass_check = check_password_hash(query["password"], args["old_password"])

        if not pass_check:
            message = "Confirm your current password before changing your password"
            return Response.get_message(400, message=message)

        password = generate_password_hash(args["new_password"])

        try:
            result = model.change_password(user_id, password)

            if not result:
                return Response.get_error(422, error="Something failed")

            return Response.get_message(200, message="Modified Successfully")
        except Exception as error:
            return Response.get_error(304, error)


class UserInfoResource(Resource):
    @admin_required()
    def get(self, user_id):
        model = UserModel()
        schema = UserSchema()

        query = model.get_by("user_id", value=user_id)

        if not query:
            return Response.get_message(404, message="User not found")

        serialized = schema.dump(query)
        return Response.get_message(200, message="OK", data=serialized)

    @admin_required()
    def delete(self, user_id):
        model = UserModel()
        query = model.get_by("user_id", value=user_id)

        if not query:
            return Response.get_message(404, message="Unable to find this user")

        try:
            result = model.delete(user_id)

            if not result:
                return Response.get_error(422, error="Something failed")

            return Response.get_message(204, message="Deleted Successfully")
        except Exception as error:
            return Response.get_error(422, error)


class UserListResource(Resource):
    @admin_required()
    def get(self):
        model = UserModel()
        schema_list = UserSchema(many=True)
        data = schema_list.dump(model.get_all())
        return Response.get_message(200, message="OK", data=data)
