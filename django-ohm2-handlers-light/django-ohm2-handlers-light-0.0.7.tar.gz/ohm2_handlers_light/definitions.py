from django.core.exceptions import ObjectDoesNotExist
from . import settings
from . import errors as ohm2_handlers_light_errors
from . import models as ohm2_handlers_light_models

try:
	from django.utils.deprecation import MiddlewareMixin
except ImportError:
	MiddlewareMixin = object

try:
	import simplejson as json
except Exception:
	import json

import random, string, time

class BaseException(Exception):
	
	def __init__(self, *args, **kwargs):
		self.app = kwargs.get("app", "ohm2_handlers_light")
		self.code = kwargs.get("code", settings.DEFAULT_EXCEPTION_CODE)
		self.message = kwargs.get("message", settings.DEFAULT_EXCEPTION_MESSAGE)
		self.ins_filename = kwargs.get("ins_filename", "")
		self.ins_lineno = kwargs.get("ins_lineno", -1)
		self.ins_function = kwargs.get("ins_function", "")
		self.ins_code_context = kwargs.get("ins_code_context", "")

	
	def regroup(self):
		return {
			"code" : self.code,
			"message" : self.message,
		}

class RunException(BaseException):
	
	def __init__(self, code, message, **kwargs):
		super(RunException, self).__init__(*args, **kwargs)
		pass


class RequestException(BaseException):
	
	def __init__(self, app, code, message, original, **kwargs):
		kwargs["app"] = app
		kwargs["code"] = code
		kwargs["message"] = message
		kwargs["original"] = original
		super(RequestException, self).__init__(**kwargs)
		
		
	


class MiddlewareContext(MiddlewareMixin):

	def __init__(self, *args, **kwargs):
		pass

	@property
	def as_dict(self):
		return self.__dict__


class Device(object):

	is_ios = False
	is_android = False
	is_mobile = False

	is_pc = False
	is_bot = False

	def __init__(self, *args, **kwargs):
		for k, v in kwargs.items():
			setattr(self, k, v)

		if self.is_ios or self.is_android:
			self.is_mobile = True



class EmailHandler(object):

	def __init__(self, *args, **kwargs):
		
		self.to_email = kwargs["to_email"]
		self.from_email = kwargs["from_email"]
		self.subject = kwargs["subject"]

		self.provider = kwargs.get("provider", "Unknown")
		self.html = kwargs.get("html", "")
		self.text = kwargs.get("text", "")
		self.sent = False
		self.read = False
		self.extra = kwargs.get("extra", "")
		

	def save(self):		
		return handlers_models.BaseEmail.objects.create(provider = self.provider,
														to_email = self.to_email,
													    from_email = self.from_email,
													    subject = self.subject,
													    html = self.html,
													    text = self.text,
													    sent = self.sent,
													    read = self.read,
													    extra = self.extra)

	def safe_save(self):
		try:
			return self.save()
		except Exception as e:
			return None	

	def send_html(self, html):
		raise HandlersRunException( **ohm2_handlers_light_errors.NO_EMAIL_HANDLER_PROVIDED )

	def send_text(self, text):
		raise HandlersRunException( **ohm2_handlers_light_errors.NO_EMAIL_HANDLER_PROVIDED )

			