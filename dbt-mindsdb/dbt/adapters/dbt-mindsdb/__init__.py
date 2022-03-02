from dbt.adapters.dbt-mindsdb.connections import dbt-mindsdbConnectionManager
from dbt.adapters.dbt-mindsdb.connections import dbt-mindsdbCredentials
from dbt.adapters.dbt-mindsdb.impl import dbt-mindsdbAdapter

from dbt.adapters.base import AdapterPlugin
from dbt.include import dbt-mindsdb


Plugin = AdapterPlugin(
    adapter=dbt-mindsdbAdapter,
    credentials=dbt-mindsdbCredentials,
    include_path=dbt-mindsdb.PACKAGE_PATH)
