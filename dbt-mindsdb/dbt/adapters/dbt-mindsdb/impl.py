from dbt.adapters.sql import SQLAdapter
from dbt.adapters.dbt-mindsdb import dbt-mindsdbConnectionManager


class dbt-mindsdbAdapter(SQLAdapter):
    ConnectionManager = dbt-mindsdbConnectionManager
