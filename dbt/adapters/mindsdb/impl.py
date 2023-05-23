from dbt.adapters.sql import SQLAdapter
from dbt.adapters.mindsdb import MindsdbConnectionManager, MindsdbRelation

LIST_SCHEMAS_MACRO_NAME = 'list_schemas'
LIST_RELATIONS_MACRO_NAME = 'list_relations_without_caching'

class MindsdbAdapter(SQLAdapter):
    Relation = MindsdbRelation
    ConnectionManager = MindsdbConnectionManager

    @classmethod
    def date_function(cls):
        return 'current_date()'

    def quote(self, identifier):
        return '`{}`'.format(identifier)
