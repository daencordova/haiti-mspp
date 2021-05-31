import logging

from utils.app.pgconnection import PGConnection


class Model(object):
    def __init__(self):
        try:
            self.conn = PGConnection()
        except Exception as error:
            logging.warning(error)

    def get(self, query, one_row=False):
        return self.conn.execute_fecth(query, one_row)

    def set(self, query):
        return self.conn.execute_statement(query)

    def if_exists(self, query):
        response = self.conn.execute_fecth(query, one_row=True)
        return True if response[0] >= 1 else False

    def migrate(self, sql, name):
        if self.set(sql):
            logging.info(f"Table {name} was created in database...")

    def get_columns(self, fields):
        return ", ".join(fields)

    def to_dict(self, row, fields):
        return {field: row[index] for index, field in enumerate(fields)}
