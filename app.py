import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from werkzeug import exceptions
from flasgger import Swagger

from config import app_config
from utils.http.responses import Response
from utils.app import commands
from resources.user import BLOCKLIST
from utils.http import errors

from resources.user import (
    UserRegisterResource,
    UserLoginResource,
    UserCurrentInfoResource,
    UserRefreshAccessTokenResource,
    UserRevokeAccessTokenResource,
    UserInfoResource,
    UserListResource,
)
from resources.institution import InstitutionListResource, InstitutionResource
from resources.fund import (
    FundListResource, 
    CheckListResource, 
    BankTransferListResource,
    CheckResource, 
    BankTransferResource
)


def create_app():
    app = Flask(__name__)

    config_name = app_config[os.getenv("FLASK_ENV")]
    app.config.from_object(config_name)

    app.config["SWAGGER"] = {
        "title": "RESTful API",
        "uiversion": 3,
        "specs_route": "/docs/",
    }

    Swagger(app, template_file="docs/swagger.json")

    commands.init_app(app)

    api = Api(app)

    jwt = JWTManager(app)

    @app.route("/")
    def index():
        return Response.get_message(200, message="Haiti MSPP RESTful API")

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        return {"role": identity["role"]}

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user["id"]

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in BLOCKLIST

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return Response.get_error(401, error="The token has expired")

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return Response.get_error(401, error="Signature verification failed")

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return Response.get_error(
            401, error="Request does not contain an access token."
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return Response.get_error(401, error="The token is not fresh")

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return Response.get_error(401, error="The token has been revoked")

    # Return validation errors as JSON
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(error):
        messages = error.data.get("messages", ["Invalid request"])
        return Response.get_error(error.code, error=messages)

    api.add_resource(UserLoginResource, "/api/user/login")
    api.add_resource(UserCurrentInfoResource, "/api/user/info")
    api.add_resource(UserRefreshAccessTokenResource, "/api/user/refresh_token")
    api.add_resource(UserRevokeAccessTokenResource, "/api/user/logout")
    api.add_resource(UserRegisterResource, "/api/admin/user/register")
    api.add_resource(UserInfoResource, "/api/admin/user/<string:id>")
    api.add_resource(UserListResource, "/api/admin/user")

    api.add_resource(InstitutionResource, "/api/institution/<string:id>")
    api.add_resource(InstitutionListResource, "/api/institution")

    api.add_resource(FundListResource, "/api/fund")
    api.add_resource(CheckListResource, "/api/fund/<string:fund_id>/check")
    api.add_resource(CheckResource, "/api/fund/check/<string:check_id>")
    api.add_resource(BankTransferListResource, "/api/fund/<string:fund_id>/bank_transfer")
    api.add_resource(BankTransferResource, "/api/fund/bank_transfer/<string:banktransfer_id>")

    app.register_error_handler(exceptions.NotFound, errors.handle_404_error)
    app.register_error_handler(
        exceptions.InternalServerError, errors.handle_server_error
    )
    app.register_error_handler(exceptions.BadRequest, errors.handle_400_error)
    app.register_error_handler(FileNotFoundError, errors.handle_400_error)
    app.register_error_handler(TypeError, errors.handle_400_error)
    app.register_error_handler(KeyError, errors.handle_400_error)
    app.register_error_handler(AttributeError, errors.handle_400_error)
    app.register_error_handler(ValueError, errors.handle_400_error)
    app.register_error_handler(AssertionError, errors.handle_400_error)

    return app
