from functools import wraps
import inspect

def ohm2_handlers_light_safe_request(func, app):

	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
		except Exception as e:
			return (None, e)
		else:
			return (result, None)

	return wrapper