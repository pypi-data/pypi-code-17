from dateutil.tz import tzlocal
import humanize
import sys
from random import randint
from tabulate import tabulate
import configparser
import datetime
import dateutil.parser
import math
import microquest
import os
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

	# log and print message
	def log(self, msg, silent=False):
		t = datetime.datetime.now(tzlocal())
		with open(self.logpath, 'a') as logf:
			logf.write(f'{t}\t{msg}\n')
		if not silent:
			print(msg)
			

	# return needed xp for a given level	
	@staticmethod
	def getXPForLevel(lvl):
		if lvl == 1:
			return 0
		return 50* pow(lvl,2)

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
		if self.xp < 150:
			lvl = 1
		else:
			lvl = math.floor(math.sqrt(self.xp/50))
		return lvl

	# print status
	def printStatus(self):
		lvl = self.getLVL()
		lvlxp = self.getXPForLevel(lvl)
		xp = self.xp - lvlxp
		nextlvl = self.getXPForLevel(lvl+1) - lvlxp
		headers = ['nick', 'rank', 'lvl', 'xp', 'coins']
		lines = [[self.nick, self.getRank(), self.getLVL(), f'{xp}/{nextlvl}', self.coins]]
		print(tabulate(lines, headers=headers, tablefmt="fancy_grid"))

	# buy action
	def buy(self, quest, silent=False, multiplier=1.0):
		# price
		value = math.floor(quest.value*multiplier)
		coins = value
		xp = 0

		# can buy?
		if value > 0:
			sys.stderr.write(f"You cannot buy {quest.description}\n")
			sys.exit(1)

		# user lacks coins, using xp?
		if self.coins < - coins:
			y = input(f'You don\'t have enough coins, do you want to lose {-coins*2} xp? (y/N) ')
			# abort
			if y.lower() != 'y':
				print('aborted')
				return
			xp = coins * 2
			coins = 0
		
		msg = ''
		mult = '' if multiplier == 1.0 else f' (x{multiplier:g})'
		if coins < 0:
			self.coins += coins
			self.log(f"{self.getName()} paid {-coins} coins for: {quest.description}{mult}.", silent)
		elif xp < 0:
			self.updateXP(xp)
			self.log(f"{self.getName()} lost {-xp} xp for: {quest.description}{mult}.", silent)
			
		if not silent:
			self.printStatus()
		self.save()

	# skip
	def skip(self, quest, fail=False, silent=False, multiplier=1.0):
		msg = []
		# skip / fail
		verb = 'skipped'
		if fail:
			verb = 'failed'

		if quest.value < 0:
			sys.stderr.write(f'You cannot {verb} {quest.description}\n')
			sys.exit(1)

		# mallus
		value = math.floor(quest.value*multiplier)
		xp = 0
		coins = - value

		# user lacks coins, using xp?
		if self.coins < value:
			y = input(f'You don\'t have enough coins, do you want to lose {-coins*2}xp? (y/N) ')
			# abort
			if y.lower() != 'y':
				print('aborted')
				return
			xp = - value * 2
			coins = 0
		self.coins += coins
		self.updateXP(xp)
			
		# prepare msg
		mult = '' if multiplier == 1.0 else f' (x{multiplier:g})'
		msg.append(f"{self.getName()} {verb}: {quest.description}{mult}")
		if coins != 0:
			msg.append(f'losing {- coins} coins')
		if xp != 0:
			msg.append(f'losing {- xp} xp')
		self.log(', '.join(msg), silent)

		if not silent:
			self.printStatus()

		# fail removes the quest
		if fail:
			quest.delete(False)

		self.save()
		
	# do
	def do(self, quest, complete=False, silent=False, multiplier=1.0):
		msg = []

		# boost?
		if randint(0, 20) == 0:
			msg.append(f'boosted by the great neckbearded god')
			multiplier *=2

		# values
		value = math.floor(quest.value*multiplier)
		xp = value
		coins = math.floor(value*randint(75,100)/100)

		# do / complete
		verb = 'did'
		if complete:
			verb = 'completed'

		if quest.value < 0:
			sys.stderr.write(f'You cannot do {quest.description}\n')
			sys.exit(1)
			
		# print
		mult = '' if multiplier == 1.0 else f' (x{multiplier:g})'
		msg.append(f"{self.getName()} {verb}: {quest.description}{mult}")
		msg.append(f'gaining {xp} xp')
		msg.append(f'obtaining {coins} coins')
		self.log(', '.join(msg) + '.', silent)
		
		# add xp
		self.updateXP(xp)
		
		# add coins
		self.coins += coins

		# print status
		if not silent:
			self.printStatus()

		# remove completed quest
		if complete:
			quest.delete(False)

		self.save()

	# print last log lines
	def printLog(self, count=10):
		now = datetime.datetime.now(tzlocal())
		if not os.path.isfile(self.logpath):
			return
		lines = tailer.tail(open(self.logpath), count)
		
		for line in reversed(lines):
			try:
				time = line.split('\t')[0]
				time = dateutil.parser.parse(time)
				msg = '\t'.join(line.split('\t')[1:])
				delta = humanize.naturaldelta(now - time)
				print(f'{delta} ago:\n{msg}')
			except:
				sys.stderr.write(f'malformed log line: {line}\n')

	# updateXP
	def updateXP(self, val):
		lvl = self.getLVL()
		self.xp += val
		new_lvl = self.getLVL()
	
		#lvlup?
		if lvl < new_lvl:
			self.log(f'{self.nick} attained level {new_lvl}!')
		elif lvl > new_lvl:
			self.log(f'{self.nick} lost a level! now level {new_lvl}')
		self.save
