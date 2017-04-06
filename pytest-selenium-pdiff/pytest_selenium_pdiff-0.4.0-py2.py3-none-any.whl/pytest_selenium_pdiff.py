import base64
import os

import pytest

from . import exceptions

settings = {
    'SCREENSHOTS_PATH': None,
    'PDIFF_PATH': None,
    'ALLOW_SCREENSHOT_CAPTURE': False,
    'USE_IMAGEMAGICK': False,
    'USE_PERCEPTUALDIFF': False,
}

SCREENSHOT_EXCEPTION_TYPES = (
    exceptions.ScreenshotMismatchWithDiff,
    exceptions.ScreenshotMismatch
)


def pytest_addoption(parser):
    group = parser.getgroup('selenium-pdiff', 'selenium-pdiff')
    group._addoption('--allow-screenshot-capture',
                     help='Allow capturing of missing screenshots.',
                     metavar='bool')
    group._addoption('--screenshots-path',
                     help='Path for captured screenshots.',
                     metavar='str')
    group._addoption('--pdiff-path',
                     metavar='path',
                     help='path to pdiff output')


def pytest_report_header(config):
    if settings['USE_IMAGEMAGICK']:
        return "pytest-selenium-pdiff: using ImageMagick compare util"

    if settings['USE_PERCEPTUALDIFF']:
        return "pytest-selenium-pdiff: using perceptualdiff util"

    raise Exception(
        "pytest-selenium-pdiff: required binary "
        "`perceptualdiff` or `compare` "
        "(from ImageMagick) not found."
    )


def pytest_configure(config):
    settings['SCREENSHOTS_PATH'] = config.getoption('screenshots_path')
    settings['PDIFF_PATH'] = config.getoption('pdiff_path')
    settings['ALLOW_SCREENSHOT_CAPTURE'] = config.getoption('allow_screenshot_capture')

    if 'ALLOW_SCREENSHOT_CAPTURE' in os.environ:
        settings['ALLOW_SCREENSHOT_CAPTURE'] = True

    try:
        from sh import compare
        settings['USE_IMAGEMAGICK'] = True
    except ImportError:
        pass

    try:
        from sh import perceptualdiff
        settings['USE_PERCEPTUALDIFF'] = True
    except ImportError:
        pass


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.extra = getattr(report, 'extra', [])

    if is_failure(report) and call.excinfo:
        exception = call.excinfo.value

        if isinstance(exception, SCREENSHOT_EXCEPTION_TYPES):
            pytest_html = item.config.pluginmanager.getplugin('html')

            if pytest_html is not None:
                report.extra.append(pytest_html.extras.image(
                    get_image_as_base64(exception.expected_screenshot),
                    'PDIFF: Expected'
                ))

                if isinstance(exception, exceptions.ScreenshotMismatchWithDiff):
                    report.extra.append(pytest_html.extras.image(
                        get_image_as_base64(exception.screenshot_comparison),
                        'PDIFF: Comparison'
                    ))

                report.extra.append(pytest_html.extras.image(
                    get_image_as_base64(exception.actual_screenshot),
                    'PDIFF: Actual'
                ))
        else:
            driver = getattr(item, '_driver', None)
            if driver is not None:
                inject_screenshot_for_pytest_selenium(driver, item, report)


def inject_screenshot_for_pytest_selenium(driver, item, report):
    try:
        pytest_html = item.config.pluginmanager.getplugin('html')

        if pytest_html is not None:
            report.extra.append(pytest_html.extras.image(
                driver.get_screenshot_as_base64(),
                'Screenshot'
            ))
    except Exception as e:
        pass


def is_failure(report):
    xfail = hasattr(report, 'wasxfail')

    return (report.skipped and xfail) or (report.failed and not xfail)


def get_image_as_base64(filename):
    with open(filename, 'rb') as fp:
        content = fp.read()
        return base64.b64encode(content).decode('ascii')
