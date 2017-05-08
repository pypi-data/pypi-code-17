from TestResult import TestResultSuccess, TestResultFailure


class TestResultFactory:
    @staticmethod
    def create_success():
        return TestResultSuccess()

    @staticmethod
    def create_failure(reason, traceback=None):
        return TestResultFailure(reason, traceback)

