import os
import re
import tempfile
from pathlib import Path
import shutil
from importlib import reload

import unittest
from unittest import mock

import dbt.main
import dbt.logger


DBT_PROJECT_TMPL = '''
name: 'demo'
version: '1.0.0'
config-version: 2

profile: 'demo'

model-paths: ["models"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"
'''

DBT_PROFILE_TMPL = '''
demo:
  outputs:
    dev:
      database: mindsdb
      host: 127.0.0.1
      password: ''
      port: 47335
      type: mindsdb
      username: mindsdb
      schema: mindsdb
  target: dev
'''


class TestMindsDBAdapter(unittest.TestCase):

    def setUp(self):
        reload(dbt.main)
        reload(dbt.logger)
        self.create_project()

    def tearDown(self):
        self.delete_project()

    def create_project(self):
        project_dir = Path(tempfile.mkdtemp(prefix='dbt-profile-'))
        project_file = project_dir / 'dbt_project.yml'
        with open(project_file, 'w') as fd:
            fd.write(DBT_PROJECT_TMPL)

        profile_file = project_dir / 'profiles.yml'
        with open(profile_file, 'w') as fd:
            fd.write(DBT_PROFILE_TMPL)

        model_dir = project_dir / 'models'
        os.mkdir(model_dir)

        self.project_dir = project_dir

    def add_model(self, model_name, model_content):
        model_dir = self.project_dir / 'models'

        model_file = model_dir / f'{model_name}.sql'

        with open(model_file, 'w') as fd:
            fd.write(model_content)

    def delete_project(self):
        shutil.rmtree(self.project_dir)

    def run_dbt(self):

        args = [
            # '--debug',
            'run',
            '--profiles-dir', str(self.project_dir),
            '--project-dir', str(self.project_dir)
        ]

        return dbt.main.handle_and_check(args)

    def get_dbt_queries(self):

        conn_m = mock.Mock()

        def connect_f(connection):
            connection.state = 'open'
            connection.handle = conn_m

            mock_fetch = conn_m.cursor.return_value.fetchall
            mock_fetch.side_effect = lambda: []

            conn_m.cursor.return_value.rowcount = 0

            conn_m.cursor.return_value.description = []

            return connection

        with mock.patch('dbt.adapters.mindsdb.MindsdbConnectionManager.open') as connect_m:
            connect_m.side_effect = connect_f
            self.run_dbt()

        arg_list = conn_m.cursor().execute.call_args_list

        queries = []
        for arg in arg_list:
            query = arg.args[0]

            # ignore comments
            query = re.sub(r'/\*[\s\S]*?\*/', '', query)
            query = self.sql_line_format(query)
            queries.append(query)

        return queries

    def sql_line_format(self, sql):
        # to one line sql
        sql = re.sub(r'[\s\n]+', ' ', sql)
        return sql.strip(' ;')

    def test_create_predictor(self):
        model = '''
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
        '''

        expected1 = 'DROP PREDICTOR IF EXISTS new_predictor'

        expected2 = '''
        CREATE PREDICTOR new_predictor
            FROM photorep  (
                  select * from stores
            ) PREDICT name  as name 
             
             USING
               encoders.location.module = "CategoricalAutoEncoder",
               encoders.rental_price.module = "NumericEncoder"
        '''

        expected2 = self.sql_line_format(expected2)

        self.add_model('new_predictor', model)
        queries = self.get_dbt_queries()

        # queries exist
        assert expected1 in queries
        assert expected2 in queries

        # right queries order
        assert queries.index(expected1) < queries.index(expected2)

    def test_prediction(self):

        model = '''
            {{ config(materialized='table', integration='int1') }}
                select a, bc from ddd JOIN TEST_PREDICTOR_NAME where name > latest
        '''

        expected = '''
            create or replace table `int1`.`schem`.`predict`
            select * from (
                select a, bc from ddd JOIN TEST_PREDICTOR_NAME where name > latest
            )
        '''

        expected = self.sql_line_format(expected)

        self.add_model('schem.predict', model)
        queries = self.get_dbt_queries()

        assert expected in queries



    def test_create_database(self):
        model = '''
        {{
        config(
          materialized='database',
          engine='trino',
          parameters={
            "user": "user",
            "auth": "basic",
            "http_scheme": "https",
            "port": 443,
            "password": "password",
            "host": "localhost",
            "catalog": "catalog",
            "schema": "schema",
            "with": "with (transactional = true)"
          }
        )
        }}
        '''

        # expected1 = 'DROP DATABASE IF EXISTS new_database'
        expected1 = 'SHOW DATABASES'

        expected2 = '''
        CREATE DATABASE new_database WITH ENGINE='trino',
        PARAMETERS={'user': 'user', 'auth': 'basic', 'http_scheme': 'https', 'port': 443, 'password': 'password', 'host': 'localhost', 'catalog': 'catalog', 'schema': 'schema', 'with': 'with (transactional = true)'}
        '''

        expected2 = self.sql_line_format(expected2)

        self.add_model('new_database', model)
        queries = self.get_dbt_queries()

        # queries exist
        assert expected1 in queries
        assert expected2 in queries

        # right queries order
        assert queries.index(expected1) < queries.index(expected2)

