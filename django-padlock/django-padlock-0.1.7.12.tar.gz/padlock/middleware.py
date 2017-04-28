# -*- coding: utf-8 -*-

from uuid import uuid4

from django.conf import settings

from django import http

from django.contrib.auth.views import logout_then_login

from django.core.urlresolvers import reverse, reverse_lazy
from django.core.exceptions import ImproperlyConfigured

try:
	from django.utils.deprecation import MiddlewareMixin
except Exception as e:
	MiddlewareMixin = object


import logging
logger = logging.getLogger('django')

def setAndWarning(attrib,value):
	defined = getattr(settings,attrib,None)
	if defined is not None:
		if type(defined) != type(value):
			logger.warning("{0} in settings is not valid type.. set to {1}".format(attrib,value))
			return value
		else:
			return defined
	logger.warning("{0} no defined on settings... set to {1}".format(attrib,value))
	return value

# Lista los paths a omitir, ['*'] omite todos los paths
PADLOCK_SKIP_PATHS = setAndWarning("PADLOCK_SKIP_PATHS",[])

# Establece el tiempo de vida de la cookies (el valor recomendable es >= 120)
PADLOCK_COOKIE_AGE = setAndWarning("PADLOCK_COOKIE_AGE",3600*12)

# Boolean que indica cerrar sesión en caso de intento de romper seguridad
PADLOCK_AUTHBROKEN_LOGOUT = setAndWarning("PADLOCK_AUTHBROKEN_LOGOUT",False)

# URL de redirecionamiento luego de cerrar sesión
# Note que si empieza con '/' o ' http' se usa como string
# de caso contrario se usa como un pattern name
PADLOCK_LOGOUT_REDIRECT_TO = setAndWarning("PADLOCK_LOGOUT_REDIRECT_TO",'/')

# Define el nombre de las cockies
PADLOCK_PREFIX = setAndWarning("PADLOCK_PREFIX",'padlock')

fake_key_pieces = str(uuid4()).split('-')

def getURIRedirect():
	if PADLOCK_LOGOUT_REDIRECT_TO.startswith('/'):
		return PADLOCK_LOGOUT_REDIRECT_TO
	if PADLOCK_LOGOUT_REDIRECT_TO.startswith('?'):
		return PADLOCK_LOGOUT_REDIRECT_TO
	elif PADLOCK_LOGOUT_REDIRECT_TO.startswith('http'):
		return PADLOCK_LOGOUT_REDIRECT_TO
	else:
		return reverse(PADLOCK_LOGOUT_REDIRECT_TO)


def authFailAction(request):
	if PADLOCK_AUTHBROKEN_LOGOUT:
		if request.is_authenticated():
			return logout_then_login(request, getURIRedirect())

	response = http.HttpResponse()
	for keynum,row in enumerate(fake_key_pieces):
		response.delete_cookie(PADLOCK_PREFIX+'_id_%d' % keynum)
		response.delete_cookie('sessionid')
	response.write('<h1>403 | forbidden</h1>')
	response.status_code = 403
	return response



# PADLOCK_SKIP_PATHS = ['/es/','/auth/ingresar/'] or ['*'] for all pages
def locksmith_build_job(response,PadLockKey):
	pieces = PadLockKey.split('-')
	for keynum,row in enumerate(pieces):
		response.set_cookie(PADLOCK_PREFIX+'_id_%d' % keynum,row,max_age=PADLOCK_COOKIE_AGE)
	return response

def locksmith_restore_job(request):
	pieces = []
	for keynum,row in enumerate(fake_key_pieces):
		piece = request.COOKIES.get(PADLOCK_PREFIX+'_id_%d' % keynum,None)
		if piece is None:
			return False
		else:
			pieces.append(piece)

	return '-'.join(pieces,)


class PadLockMiddleware(MiddlewareMixin):

	def process_request(self, request):
		if getattr(request,"user",None) is None:
			return None
		if '*' in PADLOCK_SKIP_PATHS or request.path in PADLOCK_SKIP_PATHS:
			return None

		if request.user.is_authenticated():
			padlock_id = locksmith_restore_job(request)
			if not padlock_id:
				return authFailAction(request)
			if padlock_id != request.session.get(PADLOCK_PREFIX,None):
				return authFailAction(request)

		if request.method == 'POST':
			padlock_id = locksmith_restore_job(request)
			if not padlock_id:
				return authFailAction(request)
			if padlock_id != request.session.get(PADLOCK_PREFIX,None):
				return authFailAction(request)

		return None

	def process_response(self, request, response):
		if getattr(request,"user",None) is None:
			return response
		if '*' in PADLOCK_SKIP_PATHS or request.path in PADLOCK_SKIP_PATHS:
			return response

		if PADLOCK_PREFIX+'_id_0' in request.COOKIES:
			# print("hay un PadLock existente")
			if request.user.is_authenticated():
				if locksmith_restore_job(request) != request.session.get(PADLOCK_PREFIX,False):
					return authFailAction(request)
					# return http.HttpResponseForbidden()
			else:
				if locksmith_restore_job(request) and request.session.get(PADLOCK_PREFIX,None) is None:
					# print("Seteando nuevo PadLock habiendo un padlock Cookie")
					padlock_id = str(uuid4())
					request.session[PADLOCK_PREFIX] = padlock_id
					response = locksmith_build_job(response,padlock_id)
		else:
			if request.method != 'POST':
				# print("Seteando nuevo PadLock")
				padlock_id = str(uuid4())
				request.session[PADLOCK_PREFIX] = padlock_id
				response = locksmith_build_job(response,padlock_id)
			else:
				# print("No se ha Seteando un nuevo PadLock por ser un post directo")
				pass
		return response
