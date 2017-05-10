# stdlib
import csv
import time
import StringIO

# pyramid
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.exceptions import NotFound

# pyramid_debugtoolbar
from pyramid_debugtoolbar.utils import find_request_history

# lcoal
from .utils import get_sqlalchemy_panel


# ==============================================================================


@view_config(route_name='debugtoolbar.sqlalchemy_api_csv')
def sqlalchemy_api_csv(request):

    history = find_request_history(request)
    try:
        last_request_pair = history.last(1)[0]
    except IndexError:
        last_request_pair = None
        last_request_id = None
    else:
        last_request_id = last_request_pair[0]

    request_id = request.matchdict.get('request_id', last_request_id)
    toolbar = history.get(request_id, None)

    if not toolbar:
        raise NotFound

    sqla_panel = get_sqlalchemy_panel(toolbar.panels)
    if not sqla_panel:
        raise NotFound

    csvfile = StringIO.StringIO()
    csvwriter = csv.writer(csvfile)
    for query in sqla_panel.data['queries']:
        csvwriter.writerow((query['duration'],
                            query['raw_sql'],
                            query['parameters'],
                            ))
    csvfile.seek(0)
    as_csv = Response(content_type = 'text/csv',
                      body_file = csvfile,
                      status = 200,
                      )
    as_csv.headers['Content-Disposition'] = str('attachment; filename= sqlalchemy-%s.csv' % request_id)
    return as_csv
