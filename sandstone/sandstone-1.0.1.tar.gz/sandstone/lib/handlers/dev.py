import logging
import simplepam
from sandstone.lib.handlers.base import BaseHandler
from sandstone import settings



class DevLoginHandler(BaseHandler):

    def get(self):
        self.render('lib/templates/login.html')

    def post(self):
        un = self.get_argument('username')
        self.set_secure_cookie('user', un)
        self.redirect(settings.URL_PREFIX+"/")
