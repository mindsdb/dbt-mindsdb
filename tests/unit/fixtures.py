

create_predictor_model_sql = """
        {{
            config(
                materialized='predictor',
                integration='photorep',
                predict='name',
                predict_alias='name',
                using={
                    'encoders.location.module': 'CategoricalAutoEncoder',
                    'encoders.rental_price.module': 'NumericEncoder'
                }
            )
        }}
          select * from stores
"""

use_predictor_model_sql = """
       {{ config(materialized='table', predictor_name='TEST_PREDICTOR_NAME', integration='int1') }}
           select a, bc from ddd where name > latest
"""
