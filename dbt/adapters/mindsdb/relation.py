from dataclasses import dataclass,field

from dbt.adapters.base.relation import BaseRelation, Policy
from dbt.contracts.relation import ComponentName


@dataclass
class MindsdbQuotePolicy(Policy):
    database: bool = False
    schema: bool = False
    identifier: bool = False


@dataclass(frozen=True, eq=False, repr=False)
class MindsdbRelation(BaseRelation):
    quote_policy: MindsdbQuotePolicy = field(default_factory=lambda: MindsdbQuotePolicy())

    # Overridden as Mindsdb converts relation identifiers to lowercase
    def _is_exactish_match(self, field: ComponentName, value: str) -> bool:
       return self.path.get_lowered_part(field) == value.lower()
