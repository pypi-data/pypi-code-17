class Response(object):
    def __init__(self, status_code, body=None, err_message=None):
        """
        :type status_code: int
        :type body: bbridge_sdk.entity.response.bbridge_entity.BBridgeEntity | dict | None
        :type err_message: str | None
        """
        self.__status_code = status_code
        self.__body = body
        self.__err_message = err_message

    @property
    def body(self):
        return self.__body

    @property
    def status_code(self):
        return self.__status_code

    @property
    def err_message(self):
        return self.__err_message
