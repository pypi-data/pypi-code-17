# -*- coding: latin-1 -*-
from jinja2 import TemplateNotFound

from pdbwebtemplate.core.business.password import ChangePasswordBusiness
from pdbwebtemplate.core.coreclassesweb import BaseHandlerSession
from pdbwebtemplate.core.my_jinja import Jinja


class AllPagesRoute(BaseHandlerSession):

    @classmethod
    def get_type_content(cls):
        return 'html'

    def handle(self, received_json_data, response_data):
        pass

    def get(self, param=''):
        user = self.session.get('user')
        if param == 'recuperarsenha':
            self.clear_cache()
            self.session['user'] = None
            user = None

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
        infos_view['created'] = False
        infos_view['updated'] = False
        infos_view['updated_email'] = False
        infos_view['password_changed'] = False

        if self.session.get('password_changed'):
            infos_view['password_changed'] = True
            self.session['password_changed'] = False

        if user:
            infos_view['user'] = user
            infos_view['logged'] = ''
            infos_view['nlogged'] = 'hide'

            if self.session.get('created'):
                infos_view['created'] = True
                self.session['created'] = False
            if self.session.get('updated'):
                infos_view['updated'] = True
                self.session['updated'] = False
            if self.session.get('updated_email'):
                infos_view['updated_email'] = True
                self.session['updated_email'] = False


        else:
            infos_view['user'] = {}
            infos_view['logged'] = 'hide'
            infos_view['nlogged'] = ''

        if param != 'index.html':
            infos_view['root'] = 'index.html'

        self.response.headers['Content-Type'] = 'html'
        outstr = template.render(infos_view)
        self.response.write(outstr)
