import logging

from utils.app.pgconnection import PGConnection
from schemas.user import UserSchema

from models.user import UserModel
from models.institution import InstitutionModel
from models.fund import FundModel, CheckModel, BankTransferModel


schema = UserSchema()

models = {
    "users": UserModel(),
    "institutions": InstitutionModel(),
    "funds": FundModel(),
    "checks": CheckModel(),
    "bank_transfers": BankTransferModel(),
}


def create_db():
    for model in models.values():
        model.migrate_table()


def seed_db():
    USERS = [
        {
            "fullname": "Administrador",
            "username": "admin",
            "email": "admin@admin.com",
            "password": "admin",
            "role": "admin",
        },
        {
            "fullname": "Usuario",
            "username": "user",
            "email": "user@gmail.com",
            "password": "user",
            "role": "user",
        },
    ]

    for user in USERS:
        data = schema.load(user)
        result = models["users"].save(**data)

        if result:
            logging.info("Table users seeded...")


def drop_db():
    conn = PGConnection()

    tables = list(models.keys())

    for table in tables[::-1]:
        conn.execute_statement(f"DROP TABLE IF EXISTS {table};")


def init_app(app):
    for command in [create_db, drop_db, seed_db]:
        app.cli.add_command(app.cli.command()(command))
