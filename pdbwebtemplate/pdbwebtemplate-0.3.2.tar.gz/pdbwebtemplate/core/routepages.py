# -*- coding: latin-1 -*-
from jinja2 import TemplateNotFound

from pdbwebtemplate.core.business.password import ChangePasswordBusiness
from pdbwebtemplate.core.coreclassesweb import BaseHandlerSession
from pdbwebtemplate.core.web.my_jinja import Jinja


class AllPagesRoute(BaseHandlerSession):
    def get(self, param=''):

        user = self.session.get('user')

        # TODO: improve it....
        param = ChangePasswordBusiness.check_change_pass_attempt(self, param)

        if not '.html' in param:
            page = '{}{}'.format(param, '.html')
        else:
            page = param
        try:
            template = Jinja.get_jinja_object().get_template(page)
            ### TODO: set hooker here
        except TemplateNotFound:
            ### TODO: set hooker here
            template = Jinja.get_jinja_object().get_template('index.html')

        #TODO: review it.....
        infos_view = {}
        infos_view['created'] = 'hide'

        if user:
            infos_view['user'] = user
            infos_view['logged'] = ''
            infos_view['nlogged'] = 'hide'

            if self.session.get('created'):
                infos_view['created'] = ''
                self.session['created'] = False
        else:
            infos_view['user'] = {}
            infos_view['logged'] = 'hide'
            infos_view['nlogged'] = ''

        if param != 'index.html':
            infos_view['root'] = 'index.html'

        outstr = template.render(infos_view)
        self.response.write(outstr)
