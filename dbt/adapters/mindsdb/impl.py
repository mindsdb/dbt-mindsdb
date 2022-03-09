from dbt.adapters.sql import SQLAdapter
from dbt.adapters.mindsdb import MindsdbConnectionManager


class MindsdbAdapter(SQLAdapter):
    ConnectionManager = MindsdbConnectionManager

    @classmethod
    def date_function(cls):
        return 'current_date()'

    def quote(self, identifier):
        return '`{}`'.format(identifier)
