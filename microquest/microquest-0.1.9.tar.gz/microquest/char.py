from dateutil.tz import tzlocal
from random import randint
from tabulate import tabulate
from microquest.action import Action
import configparser
import datetime
import dateutil.parser
import humanize
import math
import microquest
import os
import sys
import tailer
class Character:
	def __init__(self, nick=None, xp=0, coins=0, char_class='wizard', savefp=None):
		self.charpath = os.path.join(microquest.game.Game.BASEPATH, 'char.ini')
		self.logpath = os.path.join(microquest.game.Game.BASEPATH, 'log')
		self.nick = nick
		self.xp = xp
		self.coins = coins
		self.char_class= char_class
		self.savefilepath = savefp

	def __str__(self):
		return self.getName()

	# load character
	@staticmethod
	def load(charpath):
		char = None
		try:
			cfg = configparser.ConfigParser()
			cfg.read(charpath)
			char = Character(
				nick = cfg['CHARACTER']['nick'],
				char_class = cfg['CHARACTER']['char_class'],
				coins = int(cfg['CHARACTER']['coins']),
				xp = int(cfg['CHARACTER']['xp']),
				savefp =  charpath
			)
		except:
			return None

		return char

	# save char file
	def save(self):
		try:
			cfg = configparser.ConfigParser()
			cfg['CHARACTER'] = {
				'nick': self.nick,
				'xp': self.xp,
				'coins': self.coins,
				'char_class': self.char_class
			}
			with open(self.charpath, 'w') as cfgfile:
				cfg.write(cfgfile)
		except Exception as e:
			sys.stderr.write(e)
			sys.exit(1)

		return True

	# log messages
	def log(self, msg):
		t = datetime.datetime.now(tzlocal())
		lines = msg.split('\n')
		with open(self.logpath, 'a') as logf:
			for line in lines:
				logf.write(f'{t}\t{line}\n')

	# return needed xp for a given level	
	@staticmethod
	def getXPForLevel(lvl):
		if lvl == 1:
			return 0
		return 50* pow(lvl,2)

	# return level for a given number of xp
	@staticmethod
	def getLevelForXp(xp):
		if xp < 150:
			lvl = 1
		else:
			lvl = math.floor(math.sqrt(xp/50))
		return lvl

	# return nick + rank
	def getName(self):
		return f'{self.nick} the {self.getRank()}'

	# get rank
	def getRank(self):
		# lvl
		lvl = self.getLVL()
		if lvl < 5:
			rank = f'newbie {self.char_class}'
		elif lvl < 10:
			rank = f'apprentice {self.char_class}'
		elif lvl < 20:
			rank = self.char_class
		else:
			rank = f'master {self.char_class}'
		
		# coins
		if self.coins > 5000:
			rank = f'wealthy {rank}'

		return rank

	# return current level
	def getLVL(self):
		return self.getLevelForXp(self.xp)

	# get printable status
	def getStatus(self):
		lvl = self.getLVL()
		lvlxp = self.getXPForLevel(lvl)
		xp = self.xp - lvlxp
		nextlvl = self.getXPForLevel(lvl+1) - lvlxp
		headers = ['nick', 'rank', 'lvl', 'xp', 'coins']
		lines = [[self.nick, self.getRank(), self.getLVL(), f'{xp}/{nextlvl}', self.coins]]
		return tabulate(lines, headers=headers, tablefmt="fancy_grid")

	# do action on quest with multiplier
	def action(self, action, quest, multiplier=1.0):
		return Action(self, action, quest, multiplier)

	# get last log lines
	def getLog(self, count=10):
		now = datetime.datetime.now(tzlocal())
		if not os.path.isfile(self.logpath):
			return
		lines = tailer.tail(open(self.logpath), count)
		output = ''	
		for line in reversed(lines):
			try:
				time = line.split('\t')[0]
				time = dateutil.parser.parse(time)
				msg = '\t'.join(line.split('\t')[1:])
				delta = humanize.naturaldelta(now - time)
				output += f'{delta} ago:\n{msg}\n'
			except:
				sys.stderr.write(f'malformed log line: {line}\n')
		return output
