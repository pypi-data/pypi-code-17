#coding: utf-8


from setuptools import setup,find_packages
import os
from datetime import date



# 项目名称
NAME = 'DjangoQiniu'

# 版本号，必须填，pipy要求该字段
VERSION = __import__(NAME).__version__

# 作者
AUTHOR = 'NunchakusHuang'

# 作者邮箱
AUTHOR_EMAIL = 'hynever@qq.com'

# 维护人员
MAINTAINER = "NunchakusHuang"

# 维护人员邮箱
MAINTAINER_EMAIL = "hynever@qq.com"

# github账号
GITHUB_USERNAME = "NunchakusHuang"

# 项目简短描述
try:
	SHORT_DESCRIPTION = __import__(NAME).__short_description__
except:
	SHORT_DESCRIPTION = u'没有简短描述'

# 长描述
try:
	LONG_DESCRIPTION = open('README.rst', 'rb').read().decode("utf-8")
except:
	LONG_DESCRIPTION = u'没有长描述'

# 把DjangoQiniu中所有的子包都包含进来，find_packages会把子包也找到
PACKAGES = [NAME] + ["%s.%s" % (NAME,p) for p in find_packages(NAME)]

# 包含包中的数据文件
INCLUDE_PACKAGE_DATA = True
PACKAGE_DATA = {
	"":["*.*"]
}

# 仓库的名称
REPOSITORY_NAME = os.path.basename(os.getcwd())

# 仓库的地址（github地址）
REPOSITORY_URL = "https://github.com/{0}/{1}".format(GITHUB_USERNAME,REPOSITORY_NAME)

# 下载的URL
DOWNLOAD_URL = "https://github.com/{0}/{1}/tarball/{2}".format(GITHUB_USERNAME,REPOSITORY_NAME,str(date.today()))


# 许可证
try:
	LICENSE = __import__(NAME).__license__
except:
	LICENSE = ""

# 支持的平台
PLATFORMS = ["Windows","MacOS","Unix"]

# 分类器
CLASSIFIERS = [
	# 当前开发状态
	"Development Status :: 5 - Production/Stable",
	# 面向的群体
	"Intended Audience :: Developers",
	# 许可证书
	"License :: OSI Approved :: BSD License",
	# 自然语言
	"Natural Language :: Chinese (Simplified)",
	# 操作系统
	"Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: Unix",
    # 编程语言
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
]

# 依赖包
try:
	fp = open("requirements.txt","rb")
	INSTALL_REQUIRES = [line.strip() for line in f.readline().decode('utf-8')]
except:
	INSTALL_REQUIRES = []


# 调用setup方法，把之前设置的变量写进去
setup(
	name = NAME,
	description = SHORT_DESCRIPTION,
	long_description = LONG_DESCRIPTION,
	version = VERSION,
	author = AUTHOR,
	author_email = AUTHOR_EMAIL,
	maintainer = MAINTAINER,
	maintainer_email = MAINTAINER_EMAIL,
	packages = PACKAGES,
	include_pcakage_data = INCLUDE_PACKAGE_DATA,
	package_data = PACKAGE_DATA,
	url = REPOSITORY_URL,
	download_url = DOWNLOAD_URL,
	classifiers = CLASSIFIERS,
	platforms = PLATFORMS,
	license = LICENSE,
	install_requires = INSTALL_REQUIRES
)


"""
常用的分类器
--------
::

Frequent used classifiers List = [
    "Development Status :: 1 - Planning",
    "Development Status :: 2 - Pre-Alpha",
    "Development Status :: 3 - Alpha",
    "Development Status :: 4 - Beta",
    "Development Status :: 5 - Production/Stable",
    "Development Status :: 6 - Mature",
    "Development Status :: 7 - Inactive",

    "Intended Audience :: Customer Service",
    "Intended Audience :: Developers",
    "Intended Audience :: Education",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Financial and Insurance Industry",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Legal Industry",
    "Intended Audience :: Manufacturing",
    "Intended Audience :: Other Audience",
    "Intended Audience :: Religion",
    "Intended Audience :: Science/Research",
    "Intended Audience :: System Administrators",
    "Intended Audience :: Telecommunications Industry",

    "License :: OSI Approved :: BSD License",
    "License :: OSI Approved :: MIT License",
    "License :: OSI Approved :: Apache Software License",
    "License :: OSI Approved :: GNU General Public License (GPL)",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",

    "Natural Language :: English",
    "Natural Language :: Chinese (Simplified)",

    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: Unix",
    
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 2 :: Only",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3 :: Only",
]
"""


