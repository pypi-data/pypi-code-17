import microquest
import math
import sys

class Action(object):
	def __init__(self, char, action, quest, multiplier):
		self.char = char
		self.quest = quest
		self.action = action
		self.multiplier = multiplier
		self.xp = 0
		self.coins = 0

		# do /complete action
		if self.action in ['do', 'complete']:
			if quest.value < 0:
				sys.stderr.write(f"You cannot {self.action}: {quest.description}\n")
				sys.exit(1)
			self.xp = math.floor(self.quest.value * multiplier)

		# buy action
		if self.action == 'buy':
			# can buy?
			if quest.value > 0:
				sys.stderr.write(f"You cannot {self.action}: {quest.description}\n")
				sys.exit(1)

			if self.char.coins < - self.quest.value:
				self.xp = math.floor(self.quest.value * 2 * self.multiplier)
			else:
				self.coins = math.floor(self.quest.value * self.multiplier)


		# skip / fail action
		if self.action in ['skip', 'fail']:
			if quest.value < 0:
				sys.stderr.write(f"You cannot {self.action}: {quest.description}\n")
				sys.exit(1)
			if self.char.coins < - self.quest.value:
				self.xp = math.floor(- self.quest.value * 2 * self.multiplier)
			else:
				self.coins = math.floor(- self.quest.value * self.multiplier)

	def __str__(self):
		return f"{self.char.nick} {self.action} {self.quest.key}"

	# transpose from action to past verb
	def getVerb(self):
		translate = {
			'buy': 'bought',
			'do': 'did',
			'fail': 'failed',
			'skip': 'skipped',
			'complete': 'completed',
		}
		assert self.action in translate
		return translate[self.action]
		
	def removeQuest(self):
		return self.action in ['fail', 'complete']

	def prettyResults(self):
		# return f"{self.char.nick} {self.action} {self.quest.key}"
		lines = []
		info = []

		# win/lose lvl
		if self.levelDiff() < 0:
			lines.append(f"{self.char.getName()} lost {- self.levelDiff()} level!")
		elif self.levelDiff() > 0:
			lines.append(f"{self.char.getName()} attained level " + str(self.char.getLevelForXp(self.char.xp + self.xp)))

		# main info
		mult = '' if self.multiplier == 1.0 else f' (x{self.multiplier:g})'
		info.append(f"{self.char.getName()} {self.getVerb()}: {self.quest.description}{mult}")

		# coin
		if self.coins < 0:
			info.append(f"spending {- self.coins} coins")
		elif self.coins > 0:
			info.append(f"obtaining {self.coins} coins")

		# xp
		if self.xp < 0:
			info.append(f"losing {- self.xp} xp")
		elif self.xp > 0:
			info.append(f"gaining {self.xp} xp")
		
		lines.append(', '.join(info))

		return '\n'.join(lines)
		
	def levelDiff(self):
		lvl = self.char.getLVL()
		new_lvl = self.char.getLevelForXp(self.char.xp + self.xp)
		return new_lvl - lvl
		
	def apply(self):
		r = self.prettyResults()
		self.char.log(r)
		self.char.coins += self.coins	
		self.char.xp += self.xp	
		if self.char.xp < 0:
			self.char.xp = 0
		self.char.save()
		if self.removeQuest():
			self.quest.delete()
		return r
