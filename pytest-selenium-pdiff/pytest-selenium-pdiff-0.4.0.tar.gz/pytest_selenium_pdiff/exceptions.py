class MissingScreenshot(AssertionError):
    def __init__(self, screenshot_name, screenshot_path, *args, **kwargs):
        message = 'Cannot find the screenshot named ' \
                  '"{}" at {}, screenshot capture is disabled.'

        message = message.format(screenshot_name,
                                 screenshot_path
                                 )

        super(MissingScreenshot, self).__init__(message, *args, **kwargs)


class ScreenshotMismatch(AssertionError):
    def __init__(self, screenshot_name, expected_screenshot, actual_screenshot, *args, **kwargs):
        message = 'Expected "{}" to match reference screenshot "{}".'.format(
            actual_screenshot,
            expected_screenshot,
        )

        self.screenshot_name = screenshot_name
        self.expected_screenshot = expected_screenshot
        self.actual_screenshot = actual_screenshot

        super(ScreenshotMismatch, self).__init__(message, *args, **kwargs)


class ScreenshotMismatchWithDiff(AssertionError):
    def __init__(self, screenshot_name, expected_screenshot, actual_screenshot, screenshot_comparison, *args, **kwargs):
        message = 'Expected "{}" to match reference screenshot "{}", highlighted differences "{}".'.format(
            actual_screenshot,
            expected_screenshot,
            screenshot_comparison,
        )

        self.screenshot_name = screenshot_name
        self.expected_screenshot = expected_screenshot
        self.actual_screenshot = actual_screenshot
        self.screenshot_comparison = screenshot_comparison

        super(ScreenshotMismatchWithDiff, self).__init__(message, *args, **kwargs)


class InvalidCropOrMasks(AssertionError):
    def __init__(self,  coordinates, *args, **kwargs):
        message = 'invalid coordinates {}'

        message = message.format(coordinates)

        super(AssertionError, self).__init__(message, *args, **kwargs)
