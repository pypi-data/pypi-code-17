#!/usr/bin/env python3
from microquest.game import Game
import click

def main():
	g = Game()

	@click.group()
	def cli():
		pass
	# init
	@cli.command()
	def init():
		"""init the game"""
		g.init()

	# status
	@cli.command()
	def status():
		"""get player status"""
		g.char.printStatus()

	# add
	@cli.command()
	@click.argument('key')
	@click.argument('description', required=False)
	@click.argument('value', required=False, default=50, type=int)
	def add(key, description=None, value=50):
		"""add a quest"""
		g.add(key, description, value)

	# quests
	@cli.command()
	@click.option('--skeys', is_flag=True, help='sort by keys')
	def quests(skeys):
		"""print quests"""
		g.printQuests(skeys)

	# rm
	@cli.command()
	@click.argument('key')
	def rm(key):
		"""remove a quest"""
		g.remove(key)

	# do
	@cli.command()
	@click.argument('key')
	@click.option('--silent', is_flag=True, help='no output')
	def do(key, silent):
		"""do a quest"""
		g.action('do', key, silent)

	# buy
	@cli.command()
	@click.argument('key')
	@click.option('--silent', is_flag=True, help='no output')
	def buy(key, silent):
		"""buy something"""
		g.action('buy', key, silent)

	# complete
	@cli.command()
	@click.argument('key')
	@click.option('--silent', is_flag=True, help='no output')
	def complete(key, silent):
		"""complete a quest, remove it"""
		g.action('complete', key, silent)

	# skip
	@cli.command()
	@click.argument('key')
	@click.option('--silent', is_flag=True, help='no output')
	def skip(key, silent):
		"""skip a quest"""
		g.action('skip', key, silent)


	# fail
	@cli.command()
	@click.argument('key')
	@click.option('--silent', is_flag=True, help='no output')
	def fail(key, silent):
		"""fail a quest, remove it"""
		g.action('fail', key, silent)

	# log
	@cli.command()
	@click.argument('count', default=10, required=False, type=int)
	def log(count=10):
		"""print log"""
		g.char.printLog(count)

	# print lvl table
	@cli.command()
	@click.argument('max', default=100, required=False, type=int)
	def table(max):
		"""print xp table"""
		g.printXPTable(max)

	# import quests file
	@cli.command()
	@click.argument('questfile', required=True, type=click.Path(exists=True))
	def importq(questfile):
		"""import a quest file"""
		g.importQuests(questfile)

	cli()
