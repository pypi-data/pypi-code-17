#!/usr/bin/env python3
from microquest.game import Game
import argcomplete
import argparse
import os
import pydoc
import sys


def main():
	# confirm if loss of xp
	def confirm(action):
		if action.xp < 0:
			ok = input(f'You would lose {- action.xp} xp, are you sure? (y/N) ')
			if ok.lower() != 'y':
				print('aborted')
				sys.exit(0)
		return action
	# add a quest
	def add(args):
		if g.add(args.key, args.description or args.key, args.value):
			print(f"quest {args.key} added")

	# list quests
	def quests(args):
		if args.pager:
			pydoc.pager(g.getQuestsTable(args.skeys))
		else:
			print(g.getQuestsTable(args.skeys))

	# remove a quests
	def rm(args):
		g.remove(args.key)	

	# print status		
	def status(args):
		print(g.char.getStatus())

	# init game
	def init(args):
		g.init()
		print(g.char.getStatus())

	# do
	def do(args):
		"""do a quest"""
		# autobuy
		q = g.getQuest(args.key)
		action = 'do'
		if q.value < 0:
			action = 'buy'
		
		r = confirm(g.action(action, args.key, multiplier=args.multiplier)).apply()
		if not args.silent:
			print(r)
			print(g.char.getStatus())
	
	# buy
	def buy(args):
		r = confirm(g.action('buy', args.key, multiplier=args.multiplier)).apply()
		if not args.silent:
			print(r)
			print(g.char.getStatus())

	# complete
	def complete(args):
		r = confirm(g.action('complete', args.key, multiplier=args.multiplier)).apply()
		if not args.silent:
			print(r)
			print(g.char.getStatus())

	# skip
	def skip(args):
		r = confirm(g.action('skip', args.key, multiplier=args.multiplier)).apply()
		if not args.silent:
			print(r)
			print(g.char.getStatus())
	# fail
	def fail(args):
		r = confirm(g.action('fail', args.key, multiplier=args.multiplier)).apply()
		if not args.silent:
			print(r)
			print(g.char.getStatus())

	# print log
	def log(args):
		if args.pager:
			pydoc.pager(g.char.getLog(args.count))
		else:
			print(g.char.getLog(args.count))

	# print xp table
	def table(args):
		if args.pager:
			pydoc.pager(g.getXPTable(args.max))
		else:
			print(g.getXPTable(args.max))
	
	# import quests file
	def importq(args):
		# check if file exits
		if not os.path.isfile(args.questfile):
			sys.stderr.write(f'not a file: {args.questfile}\n')
			sys.exit(1)
		g.importQuests(args.questfile)

	# halp
	def halp(args):
		parser.print_help()
		sys.stderr.write('use -h for help\n')
		sys.exit(1)

	# start here
	g = Game()

	# create arguments parser
	parser = argparse.ArgumentParser()
	parser.set_defaults(func=halp)
	subparsers = parser.add_subparsers(title='subcommands',
		help='additional help')

	# init
	parser_init = subparsers.add_parser('init', help='init game', aliases=['i'])
	parser_init.set_defaults(func=init)

	# importq
	parser_importq = subparsers.add_parser('importq', help='import a quest file', aliases=['I'])
	parser_importq.add_argument('questfile', type=str, help='path to quest file')
	parser_importq.set_defaults(func=importq)

	# status
	parser_status = subparsers.add_parser('status', help='get player status', aliases=['S'])
	parser_status.set_defaults(func=status)

	# log
	parser_log = subparsers.add_parser('log', help='print log', aliases=['l'])
	parser_log.add_argument('count', nargs='?', type=int, default=10)
	parser_log.add_argument('--pager', help='send to pager', action='store_true')
	parser_log.set_defaults(func=log)

	# table
	parser_table = subparsers.add_parser('table', help='print xp table', aliases=['t'])
	parser_table.add_argument('max', nargs='?', type=int, default=100)
	parser_table.add_argument('--pager', help='send to pager', action='store_true')
	parser_table.set_defaults(func=table)

	# add subcommand
	parser_add = subparsers.add_parser('add', help='add a quest', aliases=['a'])
	parser_add.add_argument('key', type=str, help='quest key')
	parser_add.add_argument('description', nargs='?', type=str, help='quest description', default=None)
	parser_add.add_argument('value', nargs='?', type=int, help='quest value', default=50)
	parser_add.set_defaults(func=add)

	# quests subcommand
	parser_quests = subparsers.add_parser('quests', help='list quests', aliases=['q'])
	parser_quests.add_argument('--skeys', help='sort by keys', action='store_true')
	parser_quests.add_argument('--pager', help='send to pager', action='store_true')
	parser_quests.set_defaults(func=quests)

	# rm subcommand
	parser_rm = subparsers.add_parser('rm', help='remove a quest', aliases=['r'])
	parser_rm.add_argument('key', type=str, help='quest key')
	parser_rm.set_defaults(func=rm)

	# do
	parser_do = subparsers.add_parser('do', help='do/buy a quest', aliases=['d'])
	parser_do.add_argument('key', type=str, help='quest key')
	parser_do.add_argument('--silent', help='no output', action='store_true')
	parser_do.add_argument('--multiplier', type=float, default=1.0, required=False)
	parser_do.set_defaults(func=do)

	# buy
	parser_buy = subparsers.add_parser('buy', help='buy something', aliases=['b'])
	parser_buy.add_argument('key', type=str, help='key')
	parser_buy.add_argument('--silent', help='no output', action='store_true')
	parser_buy.add_argument('--multiplier', type=float, default=1.0, required=False)
	parser_buy.set_defaults(func=buy)

	# complete
	parser_complete = subparsers.add_parser('complete', help='complete a quest', aliases=['c'])
	parser_complete.add_argument('key', type=str, help='quest key')
	parser_complete.add_argument('--silent', help='no output', action='store_true')
	parser_complete.add_argument('--multiplier', type=float, default=1.0, required=False)
	parser_complete.set_defaults(func=complete)

	# skip
	parser_skip = subparsers.add_parser('skip', help='skip a quest', aliases=['s'])
	parser_skip.add_argument('key', type=str, help='quest key')
	parser_skip.add_argument('--silent', help='no output', action='store_true')
	parser_skip.add_argument('--multiplier', type=float, default=1.0, required=False)
	parser_skip.set_defaults(func=skip)

	# fail
	parser_fail = subparsers.add_parser('fail', help='fail a quest', aliases=['f'])
	parser_fail.add_argument('key', type=str, help='quest key')
	parser_fail.add_argument('--silent', help='no output', action='store_true')
	parser_fail.add_argument('--multiplier', type=float, default=1.0, required=False)
	parser_fail.set_defaults(func=fail)

	# auto-complete
	argcomplete.autocomplete(parser)
	args = parser.parse_args()
	args.func(args)
