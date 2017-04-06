import pytest

from pytest_selenium_pdiff import exceptions, screenshot_matches, settings


def setup_selenium_session(selenium, tmpdir):
    selenium.implicitly_wait(5)
    selenium.set_window_size(1200, 800)
    selenium.get('./tests/fixtures/page1.html')

    settings['ALLOW_SCREENSHOT_CAPTURE'] = True
    settings['USE_IMAGEMAGICK'] = True
    settings['USE_PERCEPTUALDIFF'] = False
    settings['SCREENSHOTS_PATH'] = str(tmpdir.join('screenshots/'))
    settings['PDIFF_PATH'] = str(tmpdir.join('pdiff/'))


def test_screenshot_cropped(selenium, tmpdir):
    crop_area = (10, 10, 160, 50)
    image_name = 'crop_test'

    setup_selenium_session(selenium, tmpdir)
    # capture the first screenshot
    screenshot_matches(selenium, image_name, crop=crop_area)
    # turn off capture
    settings['ALLOW_SCREENSHOT_CAPTURE'] = False
    # compare with previous
    screenshot_matches(selenium, image_name, crop=crop_area)


def test_screenshot_masked(selenium, tmpdir):
    mask_area = [(180, 0, 600, 75)]
    image_name = 'mask_test'

    setup_selenium_session(selenium, tmpdir)
    # capture the first screenshot
    screenshot_matches(selenium, image_name, masks=mask_area)
    # turn off capture
    settings['ALLOW_SCREENSHOT_CAPTURE'] = False
    # load the different page
    selenium.get('./tests/fixtures/page1-bold.html')
    # compare with previous
    screenshot_matches(selenium, image_name, masks=mask_area)


def test_screenshot_multiple_mask(selenium, tmpdir):
    mask_area = [(180, 0, 600, 75), (0, 50, 800, 125)]
    image_name = 'mask_test'

    setup_selenium_session(selenium, tmpdir)
    # capture the first screenshot
    screenshot_matches(selenium, image_name, masks=mask_area)
    # turn off capture
    settings['ALLOW_SCREENSHOT_CAPTURE'] = False
    # load the different page
    selenium.get('./tests/fixtures/page1-changed.html')
    # compare with previous
    screenshot_matches(selenium, image_name, masks=mask_area)


def test_screenshot_mask_invalid(selenium, tmpdir):
    mask_area = [(3, 2, 1)]
    image_name = 'mask_test'

    setup_selenium_session(selenium, tmpdir)

    with pytest.raises(exceptions.InvalidCropOrMasks):
        screenshot_matches(selenium, image_name, masks=mask_area)


def test_screenshot_crop_invalid(selenium, tmpdir):
    crop_area = (None, 1, 1, None)
    image_name = 'crop_test'

    setup_selenium_session(selenium, tmpdir)

    with pytest.raises(exceptions.InvalidCropOrMasks):
        screenshot_matches(selenium, image_name, crop=crop_area)
