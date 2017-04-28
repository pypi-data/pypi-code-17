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
from datetime import date
from importlib import import_module

import click
import chess
import chess.uci
import chess.pgn
import chess.polyglot
import chess.syzygy

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'engines.ini'))
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'tm.ini'))
FORMATS = ('roundrobin', )


@click.group()
def cli():
    pass


@cli.command()
@click.argument('engines', nargs=-1)
@click.option('--time', type=int, required=True)
@click.option('--inc', default=0)
@click.option('tournament_format', '--format',
              type=click.Choice(FORMATS), default='roundrobin')
@click.option('--rounds', default=1)
@click.option('use_book', '--book/--no-book', default=True)
@click.option('use_tablebase', '--tb/--no-tb', default=True)
@click.option('--draw-plies', default=10)
@click.option('--draw-thres', default=5)
@click.option('--win-plies', default=8)
@click.option('--win-thres', default=650)
@click.option('pgn_path', '--pgn', type=click.Path(resolve_path=True),
              required=True)
@click.option('--verbose-pgn', is_flag=True)
@click.option('--event', default='?')
@click.option('--site', default='?')
def new(engines, time, inc, tournament_format, rounds,
        draw_plies, draw_thres, win_plies, win_thres,
        use_book, use_tablebase, pgn_path, verbose_pgn, event, site):
    """Run a new tournament"""
    manager = import_module(tournament_format)
    tournament = manager.new_tournament(engines, rounds)

    for round_no, (white, black) in tournament:
        tournament.update(play_game(
            w_eng=white, b_eng=black,
            time=time, inc=inc,
            use_book=use_book, use_tablebase=use_tablebase,
            draw_plies=draw_plies, draw_thres=draw_thres,
            win_plies=win_plies, win_thres=win_thres,
            event=event, site=site, round_no=str(round_no),
            pgn_path=pgn_path, verbose_pgn=verbose_pgn
        ))


def play_game(w_eng, b_eng, time, inc, use_book, use_tablebase,
              draw_plies, draw_thres, win_plies, win_thres,
              pgn_path, verbose_pgn, event, site, round_no):
    """
    Play an engine-vs-engine game.
    Append the resulting PGN to "./{event}.png" and
    return 1, 0, or -1, corresponding to white win, draw, or black win.

    w_eng and b_eng must correspond to the name of a section in
    the config file.

    time (in seconds) and inc (in milliseconds) define the time control.

    if use_book, use the opening book defined in the config file.

    if use_tablebase, use a tablebase to adjudicate positions.

    draw_plies, draw_thres, win_plies, win_thres are used to adjudicate
    the game.

    if verbose_pgn, save (eval, depth, time) info as pgn comments.

    event, site, round_no are used as pgn headers.
    """
    if not (w_eng in config and b_eng in config):
        raise ValueError('Invalid engine names.')

    engines = [chess.uci.popen_engine(os.path.join(
        config.get('TournamentMaster', 'basepath'),
        engine,
        config.get(engine, 'exe')
    )) for engine in (w_eng, b_eng)]

    info = [chess.uci.InfoHandler(), chess.uci.InfoHandler()]
    for engine, handler in zip(engines, info):
        engine.info_handlers.append(handler)

    board = chess.Board()
    pgn = chess.pgn.Game()
    pgn_node = pgn.root()
    w_time = time * 1000
    b_time = time * 1000
    draw_count = 0
    win_count = 0

    if use_tablebase:
        tb = chess.syzygy.open_tablebases(config.get('TournamentMaster',
                                                     'syzygypath'))

    for index, engine in enumerate(engines):
        engine.uci()
        engine.setoption(config['DEFAULT'])
        engine.setoption(config[b_eng if index else w_eng])
        engine.ucinewgame()

    if use_book:
        book_depth = config.getint('TournamentMaster', 'bookdepth')
        with chess.polyglot.open_reader(config.get('TournamentMaster',
                                                   'bookpath')) as book:
            while board.fullmove_number <= book_depth:
                try:
                    move = book.weighted_choice(board).move()
                    board.push(move)
                    pgn_node = pgn_node.add_variation(move)
                except IndexError:
                    break
        if board.turn == chess.BLACK:
            engines.reverse()
            info.reverse()

    for engine, handler in cycle(zip(engines, info)):
        if use_tablebase:
            wdl = tb.get_wdl(board)
            if wdl is not None:
                if abs(wdl) == 2:
                    result = 1 if (board.turn == chess.WHITE) ^ (wdl < 0) else -1
                else:
                    result = 0
                print('tablebase position')
                break

        engine.position(board)
        current_player = board.turn

        start = perf_counter()
        move, _ = engine.go(wtime=w_time, btime=b_time, winc=inc, binc=inc)
        time_spent = round((perf_counter() - start) * 1000)
        board.push(move)

        score = handler.info['score'][1].cp
        mate = handler.info['score'][1].mate

        comment = ''
        if verbose_pgn:
            if score is None:
                score_str = f'{"+" if mate >= 0 else "-"}M{mate}'
            else:
                score_str = f'{score / 100:+.2f}'
            depth = str(handler.info.get('depth', '0'))
            comment = f'{score_str}/{depth} {time_spent / 1000:.2f}s'
        pgn_node = pgn_node.add_variation(move, comment)

        if score is None:
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

        if draw_count >= draw_plies:
            print('draw agreed')
            result = 0
            break

        if win_count >= win_plies and score < 0:
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

    if use_tablebase:
        tb.close()

    pgn.headers['Event'] = event
    pgn.headers['Site'] = site
    pgn.headers['Round'] = round_no
    pgn.headers['White'] = w_eng
    pgn.headers['Black'] = b_eng
    pgn.headers['Date'] = str(date.today())
    pgn.headers['Result'] = ('1/2-1/2', '1-0', '0-1')[result]
    print(' '.join((pgn.headers["White"],
                    pgn.headers["Result"][:3],
                    pgn.headers["Black"])))

    print(f'writing pgn to {pgn_path}')
    with open(pgn_path, 'a') as f:
        pgn.accept(chess.pgn.FileExporter(f))

    return result


if __name__ == '__main__':
    cli()
