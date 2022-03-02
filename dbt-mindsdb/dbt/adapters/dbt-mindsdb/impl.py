from dbt.adapters.sql import SQLAdapter
from dbt.adapters.dbt-mindsdb import DbtMindsDBConnectionManager


class DbtMindsDBAdapter(SQLAdapter):
    ConnectionManager = DbtMindsDBConnectionManager

    @classmethod
    def date_function(cls):
        return 'datenow()'