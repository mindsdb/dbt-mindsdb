from dataclasses import dataclass
from contextlib import contextmanager
import dbt.exceptions
from dbt.contracts.connection import AdapterResponse
from pymysql.cursors import Cursor

from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
from dbt.logger import GLOBAL_LOGGER as logger
from typing import Optional
import pymysql

@dataclass
class MindsdbCredentials(Credentials):
    host: str
    port: int
    username: str
    password: str
    database: str
    schema: str

    @property
    def type(self):
        return 'mindsdb'

    def _connection_keys(self):
        """
        List of keys to display in the `dbt debug` output.
        """
        return 'host', 'port', 'user', 'database', 'schema'



class MindsdbConnectionManager(SQLConnectionManager):
    TYPE = 'mindsdb'

    @classmethod
    def get_response(cls, cursor: Cursor) -> AdapterResponse:
        return AdapterResponse(
            _message="{}".format(f"OK. Rows affected: {cursor.rowcount}"),
            rows_affected=cursor.rowcount,
            code=200
        )
        
    @classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')
            return connection

        credentials = connection.credentials
        # TODO: shoud we ue pymysql?
        try:
            handle = pymysql.connect(
                host=credentials.host,
                port=credentials.port,
                user=credentials.username,
                password=credentials.password,
                database=credentials.database
            )
            connection.state = 'open'
            connection.handle = handle
        except pymysql.Error as exc:
            logger.debug(
                "Got an error when attempting to open a "
                "connection: '{}'".format(exc)
            )
        return connection


    #TODO: Remove this if mindsdb sql api doesn't support canceling ongoing queries   
    def cancel(self, connection):
        pass
    
    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except pymysql.DatabaseError as exc:
            logger.debug('myadapter error: {}'.format(str(exc)))
            raise dbt.exceptions.DatabaseException(str(exc))
        except Exception as exc:
            logger.debug("Error running SQL: {}".format(sql))
            logger.debug("Rolling back transaction.")
            raise dbt.exceptions.RuntimeException(str(exc))
