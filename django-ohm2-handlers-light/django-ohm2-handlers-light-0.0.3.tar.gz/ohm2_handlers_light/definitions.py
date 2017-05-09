from django.core.exceptions import ObjectDoesNotExist
from . import settings
from . import errors as ohm2_handlers_light_errors
from . import models as ohm2_handlers_light_models
import random, string, time

try:
	import simplejson as json
except Exception:
	import json



class BaseException(Exception):
	
	def __init__(self, *args, **kwargs):
		self.identity = self.get_identity()
		self.app = kwargs.get("app", "ohm2_handlers_light")
		self.code = kwargs.get("code", -1)
		self.message = kwargs.get("message", "")
		self.extra = kwargs.get("extra", "")
		
		self.ins_filename = kwargs.get("ins_filename", "")
		self.ins_lineno = kwargs.get("ins_lineno", 0)
		self.ins_function = kwargs.get("ins_function", "")
		self.ins_code_context = kwargs.get("ins_code_context", "")

		if settings.PRINT_EXCEPTIONS and settings.DEBUG:
			print("app = {0}|message = {1}|code = {2}|extra: {3}".format(self.app, self.message, self.code, self.extra))

	def get_random_string(self, length = 10):
		return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))


	def get_identity(self, initial_length = 12):
		full_identity = self.get_random_string(length = 64)
		max_length = len(full_identity)
		for up_to in range(initial_length, max_length + 1):

			tmp_string = full_identity[:up_to]

			try:
				obj = models.BaseError.objects.get(identity = tmp_string)
			except ObjectDoesNotExist:
				obj = None
			except Exception as e:
				continue
			
			if obj == None:
				return tmp_string
		return self.get_random_string(length = initial_length)
			
	def save(self):
		return handlers_models.BaseError.objects.create(identity = self.identity,
														app = self.app,
													    code = self.code,
													    message = self.message,
													    extra = self.extra,
													    ins_filename = self.ins_filename,
													    ins_lineno = self.ins_lineno,
													    ins_function = self.ins_function,
													    ins_code_context = self.ins_code_context)


	def safe_save(self):
		try:
			return self.save()
		except Exception:
			return None

	def regroup(self):
		data = {"code" : self.code, "message" : self.message, "identity" : self.identity}	
		return data	
	
	def to_json(self):
		return json.dumps( self.regroup() )	


class OHM2HandlersLightRunException(BaseException):
	
	def __init__(self, *args, **kwargs):
		super(OHM2HandlersLightRunException, self).__init__(*args, **kwargs)
		if kwargs.get("save", settings.SAVE_RUN_EXCEPTIONS):
			self.safe_save()

class OHM2HandlersLightInputException(BaseException):
	
	def __init__(self, code, message, ins_filename, ins_lineno, ins_function, **kwargs):
		kwargs["code"] = code
		kwargs["message"] = message
		kwargs["ins_filename"] = ins_filename
		kwargs["ins_lineno"] = ins_lineno
		kwargs["ins_function"] = ins_function
		super(OHM2HandlersLightInputException, self).__init__(**kwargs)
		if kwargs.get("save", settings.SAVE_INPUT_EXCEPTIONS):
			self.safe_save()

class OHM2HandlersLightMethodException(BaseException):

	def __init__(self, method, address, **kwargs):
		kwargs["message"] = "invalid method {0} from {1}".format(method, address)
		super(HandlersMethodException, self).__init__(**kwargs)
		if kwargs.get("save", settings.SAVE_METHOD_EXCEPTIONS):
			self.safe_save()
	

class MiddlewareContext(object):

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

			