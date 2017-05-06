# -*- coding: utf-8 -*-
"""
    Flask-WTF-FlexWidgets - A flask extension that provides customizable WTF widgets and macros.

    Author: Bill Schumacher <bill@servernet.co>
    License: LGPLv3
    Copyright: 2017 Bill Schumacher, Cerebral Power
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.
"""
from setuptools import setup  # , find_packages

requirements = ['Flask', 'Flask-WTF']


setup(
    name="Flask-WTF-FlexWidgets",
    version="0.1.24",
    author="Bill Schumacher",
    author_email="bill@servernet.co",
    description="A flask extension that provides customizable WTF widgets and macros.",
    license="LGPLv3",
    keywords="flask wtf widget",
    url="https://github.com/bschumacher/Flask-WTF-FlexWidgets",
    install_requires=requirements,
    # packages=find_packages(),
    # setup_requires=requirements,
    # tests_require=[],
)
