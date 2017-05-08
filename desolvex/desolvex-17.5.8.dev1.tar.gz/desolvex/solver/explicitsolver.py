# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__author__ = 'christoph.statz <at> tu-dresden.de'

from tqdm import tqdm

from maui.field import Field
from desolvex.helper import ObjectSwapper


class ExplicitSolver(object):

    def __init__(self, actions, stop_criterion, step_wrapper=None, show_progress=True):

        self.__actions = actions
        self.__stop_criterion = stop_criterion
        self.__show_progress = show_progress
        self.__step_wrapper = step_wrapper

    def solve(self):

        if self.__show_progress:
            self.__progress = tqdm(unit='Time Steps', unit_scale=True, miniters=1, desc='Solver Progress:')

        while True:

            if self.__step_wrapper is not None:
                abort = self.__step_wrapper(self.__step)
                if abort:
                    break
            else:
                self.__step()

            if self.__show_progress:

                if self.__progress.total != self.__stop_criterion.int_maximum:
                    self.__progress.total = self.__stop_criterion.int_maximum

                self.__progress.update()

            if self.__stop_criterion.met():
                break

        if self.__show_progress:
            self.__progress.close()

    def __step(self):

        for el in self.__actions:

            func = el[0]

            if len(el) > 1:
                args = el[1:]
            else:
                args = None

            domains = None
            if args is not None:

                for arg in args:
                    if isinstance(arg, Field): # or isinstance(arg, View):
                        domains = arg.partition.domains.keys()
                        break
                    elif isinstance(arg, ObjectSwapper): # TODO: hasattr('swap')
                        if isinstance(arg[0], Field): # or isinstance(arg[0], View):
                            domains = arg[0].partition.domains.keys()
                            break
                    elif isinstance(arg, list):
                        if isinstance(arg[0], ObjectSwapper):
                            if isinstance(arg[0][0], Field):  #or isinstance(arg[0][0], View):
                                domains = arg[0][0].partition.domains.keys()
                                break

                if domains is not None:
                    for domain in domains:
                        domain_args = []
                        for arg in args:
                            if isinstance(arg, Field): # or isinstance(arg, View):
                                domain_args.append(arg.d[domain])
                            elif isinstance(arg, ObjectSwapper):
                                for ar in arg[:]:
                                    if isinstance(ar, Field): # or isinstance(ar, View):
                                        domain_args.append(ar.d[domain])
                                    else:
                                        domain_args.append(ar)
                            elif isinstance(arg, list):
                                if len(arg) < 2:
                                    raise ValueError("At least two list elements expected!")
                                # TODO: Extend to dict(field)!
                                if isinstance(arg[0], ObjectSwapper):
                                    if isinstance(arg[0][0], Field): # or isinstance(arg[0][0], View):
                                        domain_args.append(arg[0][arg[1]].d[domain])
                                    else:
                                        domain_args.append(arg[0][arg[1:]])
                                elif isinstance(arg[0], dict):
                                    if isinstance(arg[0].values()[0], Field): # or isinstance(arg[0].values()[0], View):
                                        domain_args.append(arg[0][arg[1]].d[domain])
                                    else:
                                        domain_args.append(arg[0][arg[1:]])
                                elif isinstance(arg[0], func):
                                    # TODO: Sort out fields and objectswapper!
                                    domain_args.append(arg[0](*arg[1:]))
                                else:
                                    raise ValueError("Expected Field or ObjectSwapper of Function!")
                            else:
                                domain_args.append(arg)
                        func(*domain_args)
                else:
                    domain_args = []
                    for arg in args:
                        if isinstance(arg, ObjectSwapper):
                            for ar in arg[:]:
                                domain_args.append(ar)
                        if isinstance(arg, list):
                            if len(arg) < 2:
                                raise ValueError("At least two list elements expected!")
                                # TODO: Extend to dict(field)!
                            if isinstance(arg[0], ObjectSwapper):
                                domain_args.append(arg[0][arg[1:]])
                            elif isinstance(arg[0], dict):
                                domain_args.append(arg[0][arg[1]])
                            elif isinstance(arg[0], func):
                                domain_args.append(arg[0](*arg[1:]))
                            else:
                                raise ValueError("Expected Field or ObjectSwapper of Function!")
                        else:
                            domain_args.append(arg)

                    func(*domain_args)
            else:
                func()

            if args is not None:
                for arg in args:
                    if isinstance(arg, Field): # or isinstance(arg, View):
                        arg.sync()

        self.__stop_criterion.update()

    def step(self):
        if self.__step_wrapper is not None:
            self.__step_wrapper.step()
        else:
            self.__step()
