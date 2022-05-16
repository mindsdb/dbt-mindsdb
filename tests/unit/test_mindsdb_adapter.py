import re
import pytest
from dbt.tests.util import run_dbt
from unittest import mock

from tests.unit.fixtures import (
    create_predictor_model_sql,
    use_predictor_model_sql
)


pytest_plugins = ["dbt.tests.fixtures.project"]


@pytest.fixture(scope="class")
def dbt_profile_target():
    return {
        'type': 'mindsdb',
        'host': '127.0.0.1',
        'port': 47335,
        'username': 'mindsdb',
        'password': '',
        'database': 'mindsdb',
        'schema': 'mindsdb',
    }


@pytest.fixture(scope="class")
def mdb_connection():
    conn_m = mock.Mock()

    def connect_f(connection):
        connection.state = 'open'
        connection.handle = conn_m

        mock_fetch = conn_m.cursor.return_value.fetchall
        mock_fetch.side_effect = lambda: []

        conn_m.cursor.return_value.rowcount = 0

        conn_m.cursor.return_value.description = []

        return connection

    patcher = mock.patch('dbt.adapters.mindsdb.MindsdbConnectionManager.open')
    connect_m = patcher.__enter__()
    connect_m.side_effect = connect_f

    return conn_m


def sql_line_format(sql):
    # to one line sql
    sql = re.sub(r'[\s\n]+', ' ', sql)
    return sql.strip(' ;')


def get_queries(conn_m):
    arg_list = conn_m.cursor().execute.call_args_list

    queries = []
    for arg in arg_list:
        query = arg[0][0]

        # ignore comments
        query = re.sub(r'/\*[\s\S]*?\*/', '', query)
        query = sql_line_format(query)
        queries.append(query)

    return queries


class TestCreatePredictor:

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "new_predictor.sql": create_predictor_model_sql,
        }

    def test_model(self, mdb_connection, project):
        run_dbt(["run"])

        queries = get_queries(mdb_connection)

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

        expected2 = sql_line_format(expected2)

        # queries exist
        assert expected1 in queries
        assert expected2 in queries


class TestUsePredictor:

    @pytest.fixture(scope="class")
    def models(self):
        return {
            "schem.predict.sql": use_predictor_model_sql,
        }

    def test_model(self, mdb_connection, project):

        run_dbt(["run"])

        queries = get_queries(mdb_connection)

        expected = '''
                    create or replace table `int1`.`schem`.`predict`
                    select * from (
                                select a, bc from ddd where name > latest
                    )
                    join TEST_PREDICTOR_NAME
        '''
        expected = sql_line_format(expected)
        assert expected in queries
