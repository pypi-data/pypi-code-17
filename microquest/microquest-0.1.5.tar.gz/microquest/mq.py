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
	def do(key):
		"""do a quest"""
		g.action('do', key)

	# buy
	@cli.command()
	@click.argument('key')
	def buy(key):
		"""buy something"""
		g.action('buy', key)

	# complete
	@cli.command()
	@click.argument('key')
	def complete(key):
		"""complete a quest, remove it"""
		g.action('complete', key)

	# skip
	@cli.command()
	@click.argument('key')
	def skip(key):
		"""skip a quest"""
		g.action('skip', key)


	# fail
	@cli.command()
	@click.argument('key')
	def fail(key):
		"""fail a quest, remove it"""
		g.action('fail', key)

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
