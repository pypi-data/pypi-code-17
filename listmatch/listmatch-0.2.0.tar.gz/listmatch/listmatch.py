# -*- coding: utf-8 -*-
from itertools import chain

from listmatch.util import (
    MatchSummary,
    explain_none,
    make_fluent_func,
    pairwise
)


class Possibilities(object):
    def __init__(self, *possibilities):
        self.possibilities = possibilities

    def __iter__(self):
        return iter(self.possibilities)

    def __repr__(self):
        return 'Possibilities({})'.format(repr(self.possibilities))


class State(object):
    def __init__(self):
        self.epsilon = []  # epsilon-closure
        self.matcher = explain_none(lambda x: False)
        self.next_state = None
        self.is_end = False


class StateMap(object):
    def __init__(self, states):
        self.states = {}
        for state, info_path in states:
            self.add_state(state, info_path)

    def add_state(self, state, info_path):
        if state in self.states:
            self.states[state] += info_path
            return
        self.states[state] = info_path
        for eps in state.epsilon:
            self.add_state(eps, info_path)

    def __iter__(self):
        return iter(self.states.items())


class StateSet(object):
    def __init__(self, states):
        self.states = set()
        for state in states:
            self.add_state(state)

    def add_state(self, state):
        if state in self.states:
            return
        self.states.add(state)
        for eps in state.epsilon:
            self.add_state(eps)

    def __iter__(self):
        return iter(self.states)


def maybe_convert_to_nfa(arg):
    if isinstance(arg, NFA):
        return arg
    return atom(arg)


class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        end.is_end = True

    def match(self, target, explain):
        return (
            self.match_explain(target)
            if explain else self.match_no_explain(target)
        )

    def match_explain(self, target):
        states = StateMap([(self.start, [[]])])

        for elem in target:
            next_state_list = []
            for state, info_path in states:
                match_info = state.matcher(elem, explain=True)
                if match_info.is_match:
                    next_state_list.append((state.next_state, [
                        info_path + [match_info.explanation]
                        for info_path in info_path
                    ]))
            states = StateMap(next_state_list)

        matched = any(True for s, info_path in states if s.is_end)
        final_paths = chain.from_iterable(
            info_path
            for s, info_path in states
            if s.is_end
        )

        return MatchSummary(
            matched,
            Possibilities(*final_paths)
        )

    def match_no_explain(self, target):
        states = StateSet([self.start])

        for elem in target:
            states = StateSet(
                state.next_state
                for state in states
                if state.matcher(elem, explain=False).is_match
            )

        return MatchSummary(any(True for s in states if s.is_end))

    def __repr__(self):
        return self.repr

    def __add__(self, other):
        return concat(self, maybe_convert_to_nfa(other))

    def __radd__(self, other):
        return concat(maybe_convert_to_nfa(other), self)

    def __or__(self, other):
        return options(self, maybe_convert_to_nfa(other))

    def __ror__(self, other):
        return options(maybe_convert_to_nfa(other), self)


class Atom(NFA):
    def __init__(self, arg):
        if not callable(arg):
            @explain_none
            def matcher(x):
                return (x == arg)
        else:
            matcher = arg
        start, end = State(), State()
        start.matcher = matcher
        start.next_state = end
        self.repr = 'atom({})'.format(repr(arg))
        super().__init__(start, end)


class Concat(NFA):
    def __init__(self, *args):
        nfas = [maybe_convert_to_nfa(arg) for arg in args]
        if len(nfas) == 0:
            state = State()
            super().__init__(state, state)
        elif len(nfas) == 1:
            super().__init__(nfas[0].start, nfas[0].end)
        else:
            for nfa1, nfa2 in pairwise(nfas):
                nfa1.end.is_end = False
                nfa1.end.epsilon.append(nfa2.start)
            super().__init__(nfas[0].start, nfas[-1].end)
        self.repr = 'concat({})'.format(
            ', '.join(
                repr(arg)
                for arg in args
            )
        )


class Options(NFA):
    def __init__(self, *args):
        nfas = [maybe_convert_to_nfa(arg) for arg in args]
        start, end = State(), State()
        start.epsilon = [nfa.start for nfa in nfas]
        for nfa in nfas:
            nfa.end.epsilon.append(end)
            nfa.end.is_end = False
        super().__init__(start, end)
        self.repr = 'options({})'.format(
            ', '.join(
                repr(arg)
                for arg in args
            )
        )


def _rep(nfa, at_least_once):
    start, end = State(), State()
    start.epsilon = [nfa.start]
    if not at_least_once:
        start.epsilon.append(end)
    nfa.end.epsilon.extend([end, nfa.start])
    nfa.end.is_end = False
    return (start, end)


class ZeroOrMore(NFA):
    def __init__(self, arg):
        nfa = maybe_convert_to_nfa(arg)
        start, end = _rep(nfa, at_least_once=False)
        super().__init__(start, end)
        self.repr = 'zero_or_more({})'.format(repr(arg))


class OneOrMore(NFA):
    def __init__(self, arg):
        nfa = maybe_convert_to_nfa(arg)
        start, end = _rep(nfa, at_least_once=True)
        super().__init__(start, end)
        self.repr = 'one_or_more({})'.format(repr(arg))


class Maybe(NFA):
    def __init__(self, arg):
        nfa = maybe_convert_to_nfa(arg)
        nfa.start.epsilon.append(nfa.end)
        super().__init__(nfa.start, nfa.end)
        self.repr = 'maybe({})'.format(repr(arg))


atom = make_fluent_func(Atom)
concat = make_fluent_func(Concat)
maybe = make_fluent_func(Maybe)
one_or_more = make_fluent_func(OneOrMore)
options = make_fluent_func(Options)
zero_or_more = make_fluent_func(ZeroOrMore)
