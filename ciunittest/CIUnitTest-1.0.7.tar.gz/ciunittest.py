import time
import unittest
import json
import decimal
import traceback


class _TextTestResult(unittest.TestResult):
    r"""
    A test result class that contains a structure remembering the results
    of a unit test.

    Used by JsonTestRunner.
    """

    SUCCESS = 1
    ERROR = 2
    FAILURE = 3

    def __init__(self, on_start):
        unittest.TestResult.__init__(self)
        self._on_start = on_start
        self.results = []

    def _print_type(self, resultType):
        r"""
        Display a humanly readable type corresponding to the type of the test
        result.
        """
        if resultType == self.SUCCESS:
            return 'success'

        if resultType == self.ERROR:
            return 'error'

        if resultType == self.FAILURE:
            return 'failure'

    def getDescription(self, test):
        r"""
        Retrieve the description of a test, if any.
        """
        return test.shortDescription()

    def startTest(self, test):
        r"""
        Start a test after recording the start time.
        """
        self._on_start(test)
        test.startTime = time.time()
        unittest.TestResult.startTest(self, test)

    def addSuccess(self, test):
        r"""
        Add an object describing a passed test.
        """
        unittest.TestResult.addSuccess(self, test)
        stopTime = time.time()
        startTime = test.startTime
        self.results.append({
            'type': self._print_type(self.SUCCESS),
            'description': self.getDescription(test),
            'name': str(test),
            'spentMilliseconds': round(stopTime - startTime, 5),
        })

    def _addErrorOrFailure(self, test, err, resultType):
        r"""
        Add an object describing a test resulted in an error or a failure.
        """
        stopTime = time.time()
        startTime = test.startTime
        errorType, errorBody, errorTraceback = err
        rawTraceback = traceback.extract_tb(errorTraceback)
        processedTraceback = [
            {'file': c[0], 'line': c[1], 'in': c[2], 'run': c[3]}
            for c
            in rawTraceback
        ]

        self.results.append({
            'type': self._print_type(self.FAILURE),
            'description': self.getDescription(test),
            'name': str(test),
            'spentMilliseconds': round(stopTime - startTime, 5),
            'error': {
                'type': str(errorType),
                'message': str(errorBody),
                'top': processedTraceback,
            }
        })

    def addError(self, test, err):
        r"""
        Add an object describing a test resulted in an error.
        """
        unittest.TestResult.addError(self, test, err)
        self._addErrorOrFailure(test, err, self.ERROR)

    def addFailure(self, test, err):
        r"""
        Add an object describing a test resulted in a failure.
        """
        unittest.TestResult.addFailure(self, test, err)
        self._addErrorOrFailure(test, err, self.FAILURE)


class _TestRunner:
    def __init__(self):
        self._on_start = lambda test: None

    @property
    def on_start(self):
        return self._on_start

    @on_start.setter
    def on_start(self, value):
        self._on_start = value

    def _run(self, tests):
        result = _TextTestResult(self._on_start)
        startTime = time.time()
        tests(result)
        stopTime = time.time()
        timeTaken = round(stopTime - startTime, 5)
        report = {
            'results': result.results,
            'spentMilliseconds': timeTaken
        }

        return report


class ObjectTestRunner(_TestRunner):
    """
    A test runner which displays the errors in a form of an object.
    """

    def run(self, tests):
        """
        Run the given test case or test suite.

        Example:
            suite = unittest.TestLoader().loadTestsFromTestCase(TestsDemo)
            result = ciunittest.JsonTestRunner().run_raw(suite)
            print('Done %d tests in %d ms.' %
                  (len(result['results']), result['spentMilliseconds']))

        :param suite: The test case or test suite to run.
        :returns: The dict detailing the result of the test case or test suite.
        """
        return self._run(tests)


class JsonTestRunner(_TestRunner):
    """
    A test runner which displays the errors in a JSON format.
    """

    def run(self, tests, formatted=False):
        """
        Run the given test case or test suite and format the response as JSON.

        Example:
            suite = unittest.TestLoader().loadTestsFromTestCase(TestsDemo)
            json = ciunittest.JsonTestRunner().run(suite, formatted=True)
            print(json)

        :param suite: The test case or test suite to run.
        :returns: The JSON detailing the result of the test case or test suite.
        """
        obj = self._run(tests)
        return json.dumps(obj, indent=4 if formatted else None)
