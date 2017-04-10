class BitfusionError(Exception):
  pass

class ClientError(BitfusionError):
  def __init__(self, msg):
    super(ClientError, self).__init__(msg)

class AuthError(BitfusionError):
  def __init__(self):
    super(AuthError, self).__init__('You must login to use this service')

class PermissionError(BitfusionError):
  def __init__(self):
    super(PermissionError, self).__init__('You do not have permission to use this resource')

class APIError(BitfusionError):
  def __init__(self, msg):
    super(APIError, self).__init__(msg)
