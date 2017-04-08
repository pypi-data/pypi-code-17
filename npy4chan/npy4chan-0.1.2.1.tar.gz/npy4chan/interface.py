from requests import *

class FourChanAPI:
	def __init__(self):
		self.baseurl="https://a.4cdn.org/{}"
		self.boards = get(self.getURL("boards.json")).json()["boards"]
		self.boards = {b["board"]: b["title"] for b in self.boards}

	def getURL(self,method):
		return self.baseurl.format(method)

	def getPosts(self,board,page=1):
		return get(self.getURL("{}/{!s}.json".format(board,page))).json()

	def getThread(self,board,threadno):
		return get(self.getURL("{}/thread/{!s}.json".format(board,threadno))).json()

	def getArchived(self,board):
		return get(self.getURL("{}/archive.json".format(board))).json()
