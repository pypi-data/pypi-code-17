# stdlib

# pyramid
from pyramid.threadlocal import get_current_request
from pyramid.decorator import reify

# pyramid_debugtoolbar
from pyramid_debugtoolbar.panels import DebugPanel
from pyramid_debugtoolbar.utils import STATIC_PATH
from pyramid_debugtoolbar.utils import ROOT_ROUTE_NAME

# local
from .utils import get_sqlalchemy_panel

# ==============================================================================


_ = lambda x: x


class SqlalchemyCsvDebugPanel(DebugPanel):
    """
    Panel that displays a link to SQLACSV download
    """
    name = 'sqlalchemy-csv'
    template = 'pyramid_debugtoolbar_api_sqlalchemy:templates/sqlalchemy_csv.dbtmako'
    title = _('SQLAlchemy Queries CSV')
    nav_title = _('SQLAlchemy CSV')

    def __init__(self, original_request):
        self.token = original_request.registry.pdtb_token
        self.pdtb_id = original_request.pdtb_id

    @reify
    def _sqlalchemy_panel(self):
        # utility for when we can't explicitly access the request
        request = get_current_request()
        sqlalchemy_panel = get_sqlalchemy_panel(request.toolbar_panels.values())
        return sqlalchemy_panel

    @property
    def has_content(self):
        sqlalchemy_panel = self._sqlalchemy_panel
        if sqlalchemy_panel and sqlalchemy_panel.queries:
            return True
        return False

    @property
    def nav_subtitle(self):
        sqlalchemy_panel = self._sqlalchemy_panel
        if sqlalchemy_panel and sqlalchemy_panel.queries:
            return len(sqlalchemy_panel.queries)
        return ''

    def render_content(self, request):
        sqlalchemy_panel = get_sqlalchemy_panel(request.toolbar_panels.values())
        if not sqlalchemy_panel:
            return 'No `sqlalchemy` panel in request.'
        if not sqlalchemy_panel.queries:
            return 'No queries in executed in request.'
        # our template might want to reference this for button visibility
        self.data = sqlalchemy_panel.data
        return super(SqlalchemyCsvDebugPanel, self).render_content(request)

    def render_vars(self, request):
        return {'route_url': request.route_url,
                'static_path': request.static_url(STATIC_PATH),
                'root_path': request.route_url(ROOT_ROUTE_NAME),
                'pdtb_id': self.pdtb_id,
                }
