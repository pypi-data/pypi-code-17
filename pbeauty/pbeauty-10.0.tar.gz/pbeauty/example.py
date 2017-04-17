# -*- coding: utf-8 -*-
'''
本文件由工具自动生成，请勿直接改动
'''
class ErrorMessage(object):
	def __init__(self):
		self.errno=0
		self.msg=""

	def to_json(self):
		return {
			"errno": self.errno,
			"msg": self.msg,
		}

	def from_json(self, js):
		self.errno = js.get("errno", 0)
		self.msg = js.get("msg", "")
		return

class S2C_LoginGate(object):
	def __init__(self):
		self.errmsg=None
		self.player_guid=None
		self.player_name=None

	def to_json(self):
		return {
			"errmsg": self.errmsg,
			"player_guid": self.player_guid,
			"player_name": self.player_name,
		}

	def from_json(self, js):
		errmsg = js.get("errmsg", None)
		if errmsg is not None:
			self.errmsg = ErrorMessage()
			self.errmsg.from_json(errmsg)
		self.player_guid = js.get("player_guid", None)
		self.player_name = js.get("player_name", None)
		return

