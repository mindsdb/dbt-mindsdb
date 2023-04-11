from dbt.adapters.base import AdapterPlugin

from dbt.adapters.mindsdb.connections import MindsdbConnectionManager
from dbt.adapters.mindsdb.connections import MindsdbCredentials
from dbt.adapters.mindsdb.relation import MindsdbRelation

from dbt.adapters.mindsdb.impl import MindsdbAdapter
from dbt.include import mindsdb


Plugin = AdapterPlugin(
    adapter=MindsdbAdapter,
    credentials=MindsdbCredentials,
    include_path=mindsdb.PACKAGE_PATH)
