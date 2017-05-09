# -*- coding: utf-8 -*-
# @Author: Administrator
# @Date:   2017-05-07 22:58:53
# @Last Modified by:   Administrator
# @Last Modified time: 2017-05-08 09:27:31

from http import HTTPClient

class Client(object):
	def __init__(self,caas_url,username=None,password=None,
		project_id=None,project_name=None,timeout=600,auth_token=None,
		**kwargs):
		'''
			To be optimized before supporting multi tenant
		'''
		if not caas_url:
			caas_url = "default"

		http_client = HTTPClient(caas_url,**kwargs)

		self.projects = projects.ProjectManager(self.http_client)
		self.images = images.ImageManager(self.http_client)
		self.containers = containers.ContainerManager(self.http_client)