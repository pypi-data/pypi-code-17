# -*- coding: utf-8 -*-

import json

class BaseException(Exception):
    @classmethod
    def get_default_response(cls, message, code):
        json_resp = {}
        json_errors = [1]
        json_errors[0] = {'domain': 'global',
                          'reason': message,
                          'message': message}
        json_resp['error'] = json_errors
        json_resp['code'] = code

        return json.dumps(json_resp)

class InvalidParameters(BaseException):
    @classmethod
    def get_json_response400(cls, message):
        return cls.get_default_response(message, 400)

class UserNotFound(BaseException):
    @classmethod
    def get_json_response404(cls, message):
        return cls.get_default_response(message, 404)


class UserInactivated(BaseException):
    @classmethod
    def get_json_response400(cls, message):
        return cls.get_default_response(message, 400)


class InvalidToken(BaseException):
    @classmethod
    def get_json_response400(cls, message):
        return cls.get_default_response(message, 400)

class TokenExpired(BaseException):
    @classmethod
    def get_json_response401(cls, message):
        return cls.get_default_response(message, 401)


class TokenUnauthorized(BaseException):
    @classmethod
    def get_json_response401(cls, message):
        return cls.get_default_response(message, 401)


class InternalServerError(BaseException):
    @classmethod
    def get_json_response500(cls, message):
        return cls.get_default_response(message, 500)

class UserAlreadyExists(BaseException):
    @classmethod
    def get_json_response400(cls, message):
        return cls.get_default_response(message, 400)

class EmailAlreadyUsed(BaseException):
    @classmethod
    def get_json_response400(cls, message):
        return cls.get_default_response(message, 400)

class InvalidCredentials(BaseException):
    @classmethod
    def get_json_response401(cls, message):
        return cls.get_default_response(message, 401)

class InvalidPasswordLength(BaseException):
    @classmethod
    def get_json_response400(cls, message):
        return cls.get_default_response(message, 400)

class FatalErrorException(BaseException):
    @classmethod
    def get_json_response500(cls, message):
        return cls.get_default_response(message, 500)


class InvalidPasswordErrorChars(BaseException):
    @classmethod
    def get_json_response400(cls, message):
        return cls.get_default_response(message, 400)