class BitfusionError(Exception):
  pass

class ClientError(BitfusionError):
  pass

class AuthError(BitfusionError):
  pass

class PermissionError(BitfusionError):
  pass

class APIError(BitfusionError):
  pass
