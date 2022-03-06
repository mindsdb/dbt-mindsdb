# 🚧 dbt-mindsdb 🚧

The dbt-mindsdb package allows dbt to connect to [MindsDB](https://github.com/mindsdb/mindsdb).


## Installation

Atm, can only be installed from source:

```
git clone git@github.com:mindsdb/dbt-mindsdb.git
python setup.py develop
```

There is an dependency issue with latest dbt-core, so make sure to run:

```
pip install markupsafe==2.0.1
```

## Configurations

Basic `profile.yml` for connecting to MindsDB:

```yml
mindsdb:
  outputs:
    dev:
      database: 'mindsdb'
      host: '127.0.0.1'
      password: ''
      port: 47335
      schema: 'mindsdb'
      type: mindsdb
      username: 'mindsdb'
  target: dev

```

