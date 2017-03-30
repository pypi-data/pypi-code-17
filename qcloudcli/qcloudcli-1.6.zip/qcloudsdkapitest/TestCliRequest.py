#!/usr/bin/python
# -*- coding: utf-8 -*-
from qcloudsdkcore.request import Request
class TestCliRequest(Request):

	def __init__(self):
		Request.__init__(self, 'apitest', 'qcloudcliV1', 'TestCli', 'apitest.api.qcloud.com')

