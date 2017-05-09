"""
@file
@brief Helpers with grammar for mokadi.
"""
from .mokadi_parser import get_tree_string, parse_mokadi, run_parse
from .mokadi_exceptions import MokadiException


def interpret(sentance, MokadiGrammarParser, MokadiGrammarLexer, MokadiGrammarListener):
    """
    Interpret a sentance and returns a list of word.

    @param      MokadiGrammarParser     parser for a specific language
    @param      MokadiGrammarLexer      lexer for a specific language
    @param      MokadiGrammarListener   listener for a specific language
    @param      sentance                any string
    @return                             list of tuple (word, kind)
    """
    parser = parse_mokadi(sentance, MokadiGrammarParser, MokadiGrammarLexer)
    stdout, stderr, tree = run_parse(parser)
    if stderr and len(stderr) > 0:
        raise MokadiException(
            "Unable to parse '{0}'\nOUT\n{1}\nERR\n{2}".format(sentance, stdout, stderr))
    res, simple = get_tree_string(
        MokadiGrammarListener, tree, parser, sentance)
    return simple
