

class BaseError(Exception):

    def __init__(self, code, description, status=None, body=None):
        self.body = body
        self.description = description
        self.code = code
        self.status = status

    def map(self):
        _map = {
            'description': self.description,
            'code': self.code
        }
        if self.body is not None:
            _map['body'] = self.body
        if self.status is not None:
            _map['status'] = self.status
        return _map

    @classmethod
    def init_with(cls, attributes):
        return cls(
            code=attributes.get('code'),
            description=attributes.get('description'),
            status=attributes.get('status'),
            body=attributes.get('body')
        )