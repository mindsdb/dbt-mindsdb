from dbt.adapters.sql import SQLAdapter
from dbt.adapters.mindsdb import MindsdbConnectionManager


class MindsdbAdapter(SQLAdapter):
    ConnectionManager = MindsdbConnectionManager

    @classmethod
    def date_function(cls):
        return 'datenow()'