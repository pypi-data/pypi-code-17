from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import MyModel

@view_config(route_name='healthcheck', renderer='string')
def healthcheck(request):
    return 'Healthy!'


@view_config(route_name='home', renderer='string')
def my_view(request):
    try:
        query = request.dbsession.query(MyModel)
        result = query.filter(MyModel.id == 1).first()
    except DBAPIError:
        return Response("Can not connect to database", content_type='text/plain', status=500)
    output = "The database says: %s" % result.name
    return output
