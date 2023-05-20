# MindsDB DBT adapter

The dbt-mindsdb package allows dbt to connect to [MindsDB](https://github.com/mindsdb/mindsdb).


## Installation

```
pip install dbt-mindsdb
```

## Configurations

Basic `profile.yml` for connecting to MindsDB:

```yml
mindsdb:
  outputs:
    dev:
      host: '127.0.0.1'
      password: ''
      port: 47335
      database: 'mindsdb'
      project: 'my_project'
      # schema: 'my_project'
      type: mindsdb
      username: 'mindsdb'
  target: dev

```
| Key      | Required | Description                                          | Example                        |
| -------- | -------- | ---------------------------------------------------- | ------------------------------ |
| type     |    ✔️   | The specific adapter to use                            | `mindsdb`                      |
| host     |    ✔️   | The MindsDB (hostname) to connect to                   | `cloud.mindsdb.com`            |
| port     |    ✔️   | The port to use                                        | `3306`  or `47335`             |
| schema   |    ✔️   | Specify the schema (project) to build models into      | The MindsDB datasource         |
| username |    ✔️   | The username to use to connect to the server           | `mindsdb` or mindsdb cloud user|
| password |    ✔️   | The password to use for authenticating to the server   | `pass                          |

## Usage

- Create dbt project, choose mindsdb database and set up connection
```    
    dbt init <project_name>
```
- create a integration with "integration" materialization:
```
    {{
    config(
      materialized='integration',
      engine='trino',
      parameters={
        "user": env_var('TRINO_USER'),
        "auth": "basic",
        "http_scheme": "https",
        "port": 443,
        "password": env_var('TRINO_PASSWORD'),
        "host": "trino.company.com",
        "catalog": "hive",
        "schema": "photorep_schema",
        "with": "with (transactional = true)"
      }
    )
    }}
```

- To create predictor add dbt model with "predictor" materialization: 
Name of the model is used as name of predictor.
Parameters:
  - integration - name of used integration to get data from and save result to.
    In has to be created in mindsdb beforehand
  - predict - field for prediction
  - predict_alias [optional] - alias for predicted field
  - using [optional] - options for configure trained model
```    
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
```

- Other paramaters for time-series predictor:
  - order_by - column that the time series will be order by. 
  - group_by - rows that make a partition
  - window - the number [int] of rows to "look back" into when making a prediction 
  - horizon - keyword specifies the number of future predictions, default value is 1


- To apply predictor add dbt model with "table" materialization. 
It creates or replaces table in selected integration with results of predictor.
Name of the model is used as name of the table to store prediction results. 
If you need to specify schema you can do it with dot separator: schema_name.table_name.sql    
Parameters:
  - integration - name of used integration to get data from and save result to.
    In has to be created in mindsdb beforehand
```    
    {{ config(materialized='table', integration='int1') }}
        select a, bc from ddd JOIN TEST_PREDICTOR_NAME where name > LATEST
```
Notes: predictor_name has been removed. Instead it must be set explicitly in JOIN part of the model

## Testing

- Install dev requirements
```    
  pip install -r dev_requirements.txt
```
- Run pytest
```    
  python -m pytest tests/
```
