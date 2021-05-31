import os
import logging

from psycopg2 import connect, OperationalError
from psycopg2 import IntegrityError


class PGConnection(object):
    def __init__(self):
        try:
            self.connect = connect(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                dbname=os.getenv("POSTGRES_DB"),
            )

            logging.debug("Database connection created.")
            self.cursor = self.connect.cursor()
        except (OperationalError, Exception) as error:
            logging.warning(error)
            raise Exception(error)

    def __del__(self):
        try:
            self.cursor.close()
            self.connect.close()
            logging.debug("Database connection closed.")
        except Exception as error:
            logging.warning(error)

    def __execute_query(self, query):
        try:
            self.cursor.execute(query)
        except (AttributeError, IntegrityError) as error:
            self.connect.rollback()
            logging.info(error)
            return False

    def execute_fecth(self, query, one_row=True):
        self.__execute_query(query)
        logging.debug(self.cursor.query)
        if not one_row:
            return self.cursor.fetchall()
        return self.cursor.fetchone()

    def execute_statement(self, query):
        self.__execute_query(query)
        self.connect.commit()
        logging.debug(self.cursor.query)
        return True if self.cursor.rowcount > 0 else False
