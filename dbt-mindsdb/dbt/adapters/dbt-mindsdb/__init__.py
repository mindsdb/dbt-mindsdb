from dbt.adapters.dbt-mindsdb.connections import DbtMindsDBConnectionManager
from dbt.adapters.dbt-mindsdb.connections import DbtMindsDBCredentials
from dbt.adapters.dbt-mindsdb.impl import DbtMindsDBAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import dbt-mindsdb


Plugin = AdapterPlugin(
    adapter=DbtMindsDBAdapter,
    credentials=DbtMindsDBCredentials,
    include_path=dDbtMindsDB.PACKAGE_PATH)
