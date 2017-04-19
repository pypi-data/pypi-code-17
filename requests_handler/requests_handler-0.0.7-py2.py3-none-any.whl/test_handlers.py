import logbook
from iologger import iologger

from requests_handler import RequestsHandler


def test_handler():
    logger = logbook.Logger("TestLogger")
    requests_handler = RequestsHandler(
        "https://autosweet-data.com/api/v1/logs",
        auth=('admin', 'aut0sw33t'))

    requests_handler.push_application()
    logger.debug("A debug message")
    logger.critical("A critical message!")
    requests_handler.pop_application()


def test_iologger():
    @iologger()
    def my_func(string: str, integer: int) -> str:
        return f"my string was {string} and my integer was {integer}."

    requests_handler = RequestsHandler(
        "https://autosweet-data.com/api/v1/logs",
        auth=('admin', 'aut0sw33t'),
        logger='TestLogger'
    )

    requests_handler.push_application()
    my_func("Abraham", integer=15)
    my_func("Isaac", 0)
    requests_handler.pop_application()


def main():
    pass


if __name__ == '__main__':
    test_iologger()
