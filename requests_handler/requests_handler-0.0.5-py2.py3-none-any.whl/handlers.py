import arrow
import requests
from logbook import LogRecord, Handler


class RequestsHandler(Handler):
    """
    Handler for logging records to a Restful API.
    
    :param api_url: URL to post records to.
    :param auth: Credentials in format (username, password).
    :param level: Logging level (DEBUG, INFO, ERROR, WARNING, CRITICAL).
    :param filter: Minimum record level to emit.
    :param bubble: Should bubble.
    """

    def __init__(self, api_url: str, auth: tuple, level: str = 'INFO',
                 filter: str = None, bubble: bool = False):
        Handler.__init__(self, level, filter, bubble)
        self.api_url = api_url
        self.auth = auth
        self.log_record_fields = [
            "channel",
            "level",
            "lineno",
            "filename",
            "module",
            "func_name",
            "message",
            "log_time"
        ]

    def emit(self, record: LogRecord):
        log_record = record.to_dict()
        log_record["log_time"] = arrow.utcnow().strftime(
            "%Y-%m-%d %H:%M:%S.%f")
        log_record = {k: v for k, v in log_record.items() if
                      k in self.log_record_fields}

        try:
            requests.post(url=self.api_url, data=log_record,
                          auth=self.auth)
        except Exception as e:
            print(e)


def main():
    pass


if __name__ == '__main__':
    main()
