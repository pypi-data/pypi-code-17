#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2007-2012 Etienne Robillard <erob@gthcfoundation.org>
# All rights reserved.
# <LICENSE=ISC>


__all__ = ['HTTPException', 'HTTPClientError', 'HTTPServerError', 'HTTPNotFound', 'HTTPUnauthorized']

class HTTPException(BaseException):
    pass
class HTTPClientError(HTTPException):
    pass
class HTTPUnauthorized(HTTPClientError):
    pass
class HTTPNotFound(HTTPClientError):    
    pass
class HTTPServerError(HTTPException):
    pass

