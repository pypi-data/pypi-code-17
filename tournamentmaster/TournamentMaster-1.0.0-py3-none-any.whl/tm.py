#! /usr/bin/env python
#
# This file is part of TournamentMaster.
# Copyright (C) 2017  Simon Chen
#
# TournamentMaster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TournamentMaster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TournamentMaster. If not, see <http://www.gnu.org/licenses/>.

import configparser
import os.path
from itertools import cycle
from time import perf_counter

import click
import chess
import chess.uci

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'engines.cfg'))


@click.group()
def cli():
    pass


@cli.command(name='game')
@click.argument('w_eng')
@click.argument('b_eng')
@click.argument('time', type=int)
@click.option('--inc', default=0)
@click.option('--use_book', is_flag=True)
@click.option('--use_tablebase', is_flag=True)
@click.option('--draw_plies', default=10)
@click.option('--draw_thres', default=5)
@click.option('--win_plies', default=8)
@click.option('--win_thres', default=650)
def play_game(w_eng, b_eng, time, inc, use_book, use_tablebase,
              draw_plies, draw_thres, win_plies, win_thres):
    """ Play an engine-vs-engine game. Return 1, 0, or -1, corresponding to
        white win, draw, or black win.

        w_eng and b_eng must correspond to the name of a section in
        the config file.

        time (in seconds) and inc (in milliseconds) define the time control.

        if use_book, use the opening book defined in the config file.

        if use_tablebase, use a tablebase to adjudicate positions

        draw_plies, draw_thres, win_plies, win_thres are used to adjudicate
        the game.
    """
    if not (w_eng in config and b_eng in config):
        raise ValueError('Invalid engine names.')

    engines = [chess.uci.popen_engine(os.path.join(
        config.get('GLOBAL', 'basepath'),
        engine,
        config.get(engine, 'exe')
    )) for engine in (w_eng, b_eng)]

    info = [chess.uci.InfoHandler(), chess.uci.InfoHandler()]
    for engine, handler in zip(engines, info):
        engine.info_handlers.append(handler)

    board = chess.Board()
    w_time = time * 1000
    b_time = time * 1000
    draw_count = 0
    win_count = 0

    for index, engine in enumerate(engines):
        engine.uci()
        engine.setoption(config['DEFAULT'])
        engine.setoption(config[b_eng if index else w_eng])
        engine.ucinewgame()

    for engine, handler in cycle(zip(engines, info)):
        engine.position(board)
        current_player = board.turn

        start = perf_counter()
        move, _ = engine.go(wtime=w_time, btime=b_time, winc=inc, binc=inc)
        time_spent = round((perf_counter() - start) * 1000)
        board.push(move)

        score = handler.info["score"][1].cp
        if score is None:
            mate = handler.info["score"][1].mate
            if mate > 0:
                score = 9999
            elif mate < 0:
                score = -9999

        if current_player == chess.WHITE:
            w_time += inc - time_spent
            if w_time <= 0:
                print('white ran out of time')
                result = -1
                break
        else:
            b_time += inc - time_spent
            if b_time <= 0:
                print('black ran out of time')
                result = 1
                break

        if abs(score) <= draw_thres:
            draw_count += 1
        else:
            draw_count = 0

        if abs(score) >= win_thres:
            win_count += 1
        else:
            win_count = 0

        if draw_count == draw_plies:
            print('draw agreed')
            result = 0
            break

        if win_count == win_plies and score < 0:
            if current_player == chess.WHITE:
                print('white resigns')
                result = -1
                break
            else:
                print('black resigns')
                result = 1
                break

        if board.is_game_over(claim_draw=True):
            print('game ended normally')
            encodings = {'1-0': 1, '0-1': -1, '1/2-1/2': 0}
            result = encodings[board.result(claim_draw=True)]
            break

    for engine in engines:
        engine.quit()
    return result


if __name__ == '__main__':
    cli()
