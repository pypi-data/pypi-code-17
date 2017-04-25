import base64
import datetime
import decimal

import pytest
import pytz
import requests

import festung.dbapi
from festung import exceptions
from festung.types import Type


@pytest.fixture
def connection_session():
    with requests.Session() as session:
        yield session


@pytest.fixture(params=['managed', 'external'])
def connection_kwargs(request, connection_session):
    if request.param == 'managed':
        return {}
    elif request.param == 'external':
        return dict(session=connection_session)
    else:
        assert False, "Not all parameters are supported"


@pytest.fixture
def connection(database_url, connection_kwargs):
    conn = festung.dbapi.Connection(database_url, **connection_kwargs)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def cursor(connection):
    cur = connection.cursor()
    try:
        yield cur
    finally:
        cur.close()


class ResponseFixture(object):
    @pytest.fixture(autouse=True)
    def prepare_responses(self, festung):
        if not self.responses:
            return
        for response in self.responses:
            festung.add_json_response(response)

    @property
    def data(self):
        return [response['data'] for response in self.responses]

    @property
    def first(self):
        try:
            return self.data[0]
        except IndexError:
            pass


class ErrorResponseFixture(ResponseFixture):
    # XXX(moritz): This is to circumvent a misbehavior in pytest
    data = None
    first = None


class TestEmptyResponse(ResponseFixture):
    responses = [{'data': [], 'headers': [], 'last_row_id': 0, 'rows_changed': 0}]

    def test_execute(self, festung, cursor):
        query = 'SELECT ?, ?, ?'
        params = ['string', 1, None]
        cursor.execute(query, params)

        [data] = festung.json_requests
        assert data['sql'] == query
        assert data['params'] == params
        assert cursor.lastrowid == self.responses[0]['last_row_id']
        assert cursor.rowcount == self.responses[0]['rows_changed']

    @pytest.mark.parametrize('param,expected_serialialized', [
        (datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.UTC), '1970-01-01T00:00:00+00:00'),
        (datetime.date(1970, 1, 1), '1970-01-01'),
        (datetime.time(0, 0, 0), '00:00:00'),
        (decimal.Decimal('1234.5678'), '1234.5678'),
    ])
    def test_binding_cast(self, festung, cursor, param, expected_serialialized):
        cursor.execute('SELECT 1', [param])
        [data] = festung.json_requests
        [serialized] = data['params']

        assert serialized == expected_serialialized

    def test_password_is_sent(self, cursor, password, festung):
        cursor.execute('SELECT * FROM foo')
        [request] = festung.requests
        assert base64.b64decode(request.headers['Authorization']) == password

    @pytest.mark.parametrize('query_string', ['kdf-iter=4000'], indirect=True)
    def test_kdf_iter_is_sent(self, cursor, query_string, festung):
        cursor.execute('SELECT * FROM foo')
        [request] = festung.requests
        assert request.headers['X-kdf-iter'] == '4000'


class TestMultipleResponses(object):
    def test_executemany(self, festung, cursor):
        for _ in range(3):
            festung.add_json_response(
                {'data': [], 'headers': [], 'last_row_id': 0, 'rows_changed': 3})

        query = 'UPDATE TABLE foo SET foo=?, bar=?, baz=?'
        params_list = [
            ['abc', 1, None],
            ['def', 2, 1.2],
            ['ghi', 3, None],
        ]
        cursor.executemany(query, params_list)
        for params, data in zip(params_list, festung.json_requests):
            assert data['sql'] == query
            assert data['params'] == params

    def test_executemany_with_result(self, festung, cursor):
        festung.add_json_response({
            'data': [[1]],
            'headers': [{'name': 'foo', 'type': 'int'}],
            'last_row_id': 0,
            'rows_changed': 0,
        })
        query = 'SELECT ?'
        params_list = [[1]]
        with pytest.raises(exceptions.ProgrammingError):
            cursor.executemany(query, params_list)

    @pytest.mark.parametrize('given,expected', [
        ('int', Type.NUMBER),
        ('blob', Type.BINARY),
        ('numeric(19, 2)', Type.NUMBER),
        ('dynamic', Type.UNKNOWN),
    ])
    def test_types(self, festung, cursor, given, expected):
        festung.add_json_response({
            'data': [],
            'headers': [{'name': 'foo', 'type': given}],
            'last_row_id': 0,
            'rows_changed': 0,
        })
        query = 'SELECT foo'
        cursor.execute(query)
        assert cursor.description[0].type_code == expected


class TestDummyResponseWithExecutedCursor(ResponseFixture):
    responses = [
        {
            'data': [['a', 1], ['b', 2]],
            'headers': [{'name': 'bar', 'type': 'string'}, {'name': 'baz', 'type': 'int'}],
            'last_row_id': 0,
            'rows_changed': 0,
        },
    ]

    @pytest.fixture(autouse=True)
    def run_query(self, cursor):
        cursor.execute("SELECT * FROM foo")

    def test_fetchone(self, cursor):
        assert cursor.fetchone() == tuple(self.first[0])
        assert cursor.fetchone() == tuple(self.first[1])
        assert cursor.fetchone() is None

    def test_fetchall_same_size_than_response(self, cursor):
        cursor.arraysize = len(self.first)
        assert cursor.fetchmany() == [tuple(row) for row in self.first]

    def test_fetchall_smaller_size_than_response(self, cursor):
        cursor.arraysize = 1
        assert cursor.fetchmany() == [tuple(self.first[0])]

    def test_fetchall_bigger_size_than_response(self, cursor):
        cursor.arraysize = len(self.first) * 10
        assert cursor.fetchmany() == [tuple(row) for row in self.first]


class TestErroneousResponse(ErrorResponseFixture):
    responses = [
        {
            'errors': ['Missing Header "Authorization"'],
            'message': "Invalid use of endpoint.",
        },
    ]

    def test_execute(self, festung, cursor):
        query = 'SELECT 1;'
        with pytest.raises(exceptions.DataError) as excinfo:
            cursor.execute(query)
            e = excinfo.value
            [response] = self.responses
            assert e.message == response['message']
            assert e.errors == response['errors']


class TestCustomMethods(object):
    def test_drop(self, festung, cursor, database, password):
        festung.add_empty_response()
        cursor.drop()
        [request] = festung.requests
        assert request.method == 'DELETE'
        assert not request.get_data()
        assert request.headers['Authorization'] == base64.b64encode(password)
        assert request.path[1:] == database
