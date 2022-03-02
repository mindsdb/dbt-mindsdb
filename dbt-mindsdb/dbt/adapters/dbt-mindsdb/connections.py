from dataclasses import dataclass

from dbt.adapters.base import Credentials
from dbt.adapters.sql import SQLConnectionManager
import pymysql


@dataclass
class DbtMindsDBCredentials(Credentials):
    host: str
    port: Optional[int] = None
    username: str
    password: str

    @property
    def type(self):
        return 'dbt-mindsdb'

    def _connection_keys(self):
         """
        List of keys to display in the `dbt debug` output.
        """
        return ('host', 'port', 'database', 'username')


class DbtMindsDBConnectionManager(SQLConnectionManager):
    TYPE = 'dbt-mindsdb'

    @classmethod
    def get_response(cls, cursor):
        return cursor.status_message
        
    @classmethod
    def open(cls, connection):
        if connection.state == 'open':
            logger.debug('Connection is already open, skipping open.')
            return connection

        credentials = connection.credentials
        #TODO: shoud we ue pymysql?
        try:
            handle = pymysql.connect(
                host=credentials.host,
                port=credentials.port,
                username=credentials.username,
                password=credentials.password
            )
            connection.state = 'open'
            connection.handle = handle
        return connection

    #TODO: Remove this if mindsdb sql api doesn't support canceling ongoing queries   
    def cancel(self, connection):
        tid = connection.handle.transaction_id()
        sql = 'select cancel_transaction({})'.format(tid)
        logger.debug("Cancelling query '{}' ({})".format(connection_name, pid))
        _, cursor = self.add_query(sql, 'master')
        res = cursor.fetchone()
        logger.debug("Canceled query '{}': {}".format(connection_name, res))
    
    @contextmanager
    def exception_handler(self, sql: str):
        try:
            yield
        except dbt_mindsdb.DatabaseError as exc:
            self.release(connection_name)

            logger.debug('myadapter error: {}'.format(str(e)))
            raise dbt.exceptions.DatabaseException(str(exc))
        except Exception as exc:
            logger.debug("Error running SQL: {}".format(sql))
            logger.debug("Rolling back transaction.")
            self.release(connection_name)
            raise dbt.exceptions.RuntimeException(str(exc))