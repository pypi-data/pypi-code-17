#!/usr/bin/env python
# -*- coding: utf-8 -*-
from copy import deepcopy

from pytest_selenium_pdiff import *


def test_pytest_report_header():
    old_settings = deepcopy(settings)

    settings['USE_IMAGEMAGICK'] = True
    settings['USE_PERCEPTUALDIFF'] = True

    assert 'ImageMagick' in pytest_report_header(None)

    settings['USE_IMAGEMAGICK'] = False

    assert 'perceptualdiff' in pytest_report_header(None)

    settings['USE_PERCEPTUALDIFF'] = False

    with pytest.raises(Exception) as e:
        pytest_report_header(None)

    settings.update(old_settings)
