import os

import mock as mock
import pytest

from pytest_selenium_pdiff import exceptions, screenshot_matches, settings


def setup_selenium_session(selenium, tmpdir):
    selenium.implicitly_wait(5)
    selenium.set_window_size(1200, 800)
    selenium.get('./tests/fixtures/page1.html')

    settings['ALLOW_SCREENSHOT_CAPTURE'] = True
    settings['SCREENSHOTS_PATH'] = str(tmpdir.join('screenshots/'))
    settings['PDIFF_PATH'] = str(tmpdir.join('pdiff/'))


def test_screenshot_matches__raises_when_capture_is_disabled(selenium, tmpdir):
    setup_selenium_session(selenium, tmpdir)

    settings['ALLOW_SCREENSHOT_CAPTURE'] = False

    with pytest.raises(exceptions.MissingScreenshot):
        assert screenshot_matches(selenium, 'testing')


def test_screenshot_matches__screenshots_saved_when_capture_is_enabled(selenium, tmpdir):
    setup_selenium_session(selenium, tmpdir)

    settings['USE_IMAGEMAGICK'] = True
    settings['USE_PERCEPTUALDIFF'] = False

    assert screenshot_matches(selenium, 'testing')
    assert os.path.exists(os.path.join(settings['SCREENSHOTS_PATH'], 'testing.png')) is True

    assert screenshot_matches(selenium, 'subdir/testing')
    assert os.path.exists(os.path.join(settings['SCREENSHOTS_PATH'], 'subdir/testing.png')) is True


def test_screenshot_matches__switches_between_backends(selenium, tmpdir):
    setup_selenium_session(selenium, tmpdir)

    screenshot_matches(selenium, 'testing')

    settings['USE_IMAGEMAGICK'] = True
    settings['USE_PERCEPTUALDIFF'] = False

    with mock.patch('sh.compare') as mock_compare:
        result = mock.MagicMock()
        result.exit_code = 0
        result.stderr = b'0'

        mock_compare.return_value = result
        screenshot_matches(selenium, 'testing')

        assert mock_compare.called

    settings['USE_IMAGEMAGICK'] = False
    settings['USE_PERCEPTUALDIFF'] = True

    with mock.patch('sh.perceptualdiff') as mock_pdiff:
        result = mock.MagicMock()
        result.exit_code = 0
        mock_pdiff.return_value = result

        screenshot_matches(selenium, 'testing')

        assert mock_pdiff.called


def test_screenshot_matches__raises_when_mismatch_detected(selenium, tmpdir):
    setup_selenium_session(selenium, tmpdir)

    screenshot_matches(selenium, 'testing')
    selenium.get('./tests/fixtures/page1-changed.html')
    selenium.find_element_by_tag_name('body').text.index("It has a second paragraph.")

    with pytest.raises(exceptions.ScreenshotMismatchWithDiff):
        assert screenshot_matches(selenium, 'testing')

    captured_path = os.path.join(settings['PDIFF_PATH'], 'testing.captured.png')
    pdiff_path = os.path.join(settings['PDIFF_PATH'], 'testing.diff.png')

    assert os.path.exists(captured_path)
    assert os.path.exists(pdiff_path)


def test_screenshot_matches__raises_when_images_are_different_sizes(selenium, tmpdir):
    setup_selenium_session(selenium, tmpdir)

    screenshot_matches(selenium, 'testing-size')

    selenium.set_window_size(1200, 900)
    selenium.get('./tests/fixtures/page1-changed.html')
    selenium.find_element_by_tag_name('body').text.index("It has a second paragraph.")

    with pytest.raises(exceptions.ScreenshotMismatch):
        assert screenshot_matches(selenium, 'testing-size')

    captured_path = os.path.join(settings['PDIFF_PATH'], 'testing-size.captured.png')
    pdiff_path = os.path.join(settings['PDIFF_PATH'], 'testing-size.diff.png')

    assert os.path.exists(captured_path)
    assert os.path.exists(pdiff_path) is False
