from microquest.char import Character
from microquest.quest import Quest

import sys
import configparser
import os
from tabulate import tabulate
import appdirs
import click
import re

class Game:
	BASEPATH = os.path.join(appdirs.user_config_dir(), 'microquest')
	def __init__(self):
		self.defaultcharpath = os.path.join(self.BASEPATH, 'char.ini')
		self.defaultquestspath = os.path.join(self.BASEPATH, 'quests.ini')
		self.quests = self.loadQuests(self.defaultquestspath)

		# attempt to load default character
		self.char = Character.load(self.defaultcharpath)

		# init if no char
		if self.char == None:
			self.init()

		

	# init a configuration
	def init(self):
		"""make path"""
		if not os.path.isdir(self.BASEPATH):
			os.makedirs(self.BASEPATH, mode=0o770)

		# ask for info
		nick = input('Nick? ') 
		char_class = input('class? (i.e. wizard) ')
		self.char = Character(nick=nick, char_class=char_class, coins=0, xp=0, savefp=self.defaultcharpath)
		self.char.save()
		
		self.quests = []
		
	# char action quest
	def action(self, action, questkey, silent=False, multiplier=1):
		if not questkey in self.quests:
			sys.stderr.write(f"{questkey} do no exists\n")
			sys.exit(1)

		quest = self.quests[questkey]

		if action in ['do', 'complete']:
			self.char.do(quest, complete=action=='complete', silent=silent, multiplier=multiplier)
		elif action in ['skip', 'fail']:
			self.char.skip(quest, fail=action=='fail', silent=silent, multiplier=multiplier)
		elif action == 'buy':
			self.char.buy(quest, silent=silent, multiplier=multiplier)

	# parse a date
	def parseDate(datestring):
		return dateutil.parser.parse(datestring)
		

	# load quests
	def loadQuests(self, f=None):
		quests = {}
		if f==None:
			f = self.defaultquestspath
		if not os.path.isfile(f):
			return quests

		cfg = configparser.ConfigParser()
		cfg.read(f)
		for key in cfg.sections():
			quest = Quest(
				key=key,
				description=cfg[key]['description'],
				value = int(cfg[key]['value']),
				savefp = f
			)
			quests[quest.key] = quest

		return quests
	
	# import quest file
	def importQuests(self, f):
		newQuests = self.loadQuests(f)
		for key, quest in newQuests.items():
			quest.savefp = self.defaultquestspath
			quest.save()

	# print xp table
	def printXPTable(self, count=100):
		headers = ['lvl', 'xp', 'xp diff']
		lines = [[1, 0, 0]]
		prev_xp = 0
		for lvl in range(2, count+1):
			xp = Character.getXPForLevel(lvl)
			diff = xp - prev_xp
			prev_xp = xp
			lines.append([lvl, xp, diff])
		print(tabulate(lines, headers=headers))



	# add a quest
	def add(self, key, description=None, value=50):
		quest = Quest(key=key, description=description, value=int(value), savefp= self.defaultquestspath)
		if quest.save():
			print(f'quest {key} added.')

	# remove a quest
	def remove(self, key, verbose=True):
		if key not in self.quests:
			sys.stderr.write(f'{key} does not exists')
			sys.exit(1)
		q = self.quests[key]
		q.delete(verbose)

	# return list of quests
	# sorted by value desc
	def printQuests(self, skeys=False):
		headers = ['KEY','DESCRIPTION','VALUE']
		lines = []
		list = []
		for key, quest in self.quests.items():
			list.append(quest)

		if skeys:
			list = sorted(list, key=lambda quest: quest.key)	
		else:
			list = sorted(list, key=lambda quest: quest.value, reverse=True)	

		for q in list:
			lines.append([q.key, q.description, q.value])
		print(tabulate(lines, headers=headers))
	
	# check if a quest key exists
	def checkExists(self, key):
		if not key in self.quests:
			sys.stderr.write(f'quest {key} does not exists\n')
			sys.exit(1)
		else:
			return True

	# return a quest
	def getQuest(self, key):
		self.checkExists(key)
		return {
			'key': key,
			'value': int(self.quests[key]['value']),
			'description' : self.quests[key]['description']
		}
