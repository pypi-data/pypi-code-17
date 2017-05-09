#-*- coding: utf-8 -*-
"""
@file
@brief Parse with Mokadi'sgrammar.
"""
import io
import sys
from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from .mokadi_exceptions import MokadiException


def print_level_order(node, indent=0):
    """
    Displays a tree for the parsed text.

    @param      node        output of ``parser.parse()``
    @return                 string (see below)

    Example of results:

    ::

        MOKADIbruitdetoilette - <Parse>
           MOKADI - <Mokadi>
              MOKADI - <TerminalNodeImpl>
           bruit - <Expression_stmt>
              bruit - <Expression>
                 bruit - <Anything_stmt>
                    bruit - <Word_name_ext>
                       bruit - <Word_name>
                          bruit - <TerminalNodeImpl>
           de - <ErrorNodeImpl>
           toilette - <ErrorNodeImpl>
    """
    rows = []
    cl = str(type(node)).split(".")[-1].strip("'><")
    if cl.endswith("Context"):
        cl = cl[:-7]
    rows.append('{0}{1} - <{2}>'.format('   ' * indent, node.getText(), cl))
    if hasattr(node, "getChildren"):
        for child in node.getChildren():
            rows.append(print_level_order(child, indent + 1))
    return "\n".join(rows)


def run_parse(parser):
    """
    Parses the script and intercept standard output and error.

    @param      parser      parser, output of @see fn parse_scope
    @return                 stdout, stderr, tree

    Unfortunately, it is not multithreaded.
    It should be done in another way than by replacing *sys.stdout* and *sys.stderr*.
    """
    stdout = io.StringIO()
    stderr = io.StringIO()
    kout = sys.stdout
    kerr = sys.stderr
    sys.stdout = stdout
    sys.stderr = stderr
    tree = parser.parse()
    sys.stdout = kout
    sys.stderr = kerr
    out = stdout.getvalue()
    err = stderr.getvalue()
    if len(err) > 0:
        mes = print_level_order(tree)
        raise SyntaxError("Mokadi parsing error:\n" + err + "\nTREE\n" + mes)
    return out, err, tree


def parse_mokadi(content, MokadiGrammarParser, MokadiGrammarLexer):
    """
    Parse a sentance with mokadi language.

    @param      MokadiGrammarParser parser for a specific language
    @param      MokadiGrammarLexer  lexer for a specific language
    @param      content             string
    @return                         instance of @see cl MokadiGrammarParser
    """
    if isinstance(content, str):
        # we assume it is a string
        content = InputStream(content)
    lexer = MokadiGrammarLexer(content)
    stream = CommonTokenStream(lexer)
    parser = MokadiGrammarParser(stream)
    return parser


def get_tree_string(MokadiGrammarListener, tree, parser, script=None):
    """
    returns a string which shows the parsed tree

    @param      MokadiGrammarListener   listener to use
    @param      tree                    from @see fn parse_code
    @param      parser                  the parser used to build the tree
    @param      format                  None or a class ParseTreeListener
    @return                             string or C# code in Scope script (scope instructions are replace by blank lines)
    """

    class TreeStringListener(MokadiGrammarListener):

        """
        this class is an attempt to run through the tree
        but it is not complete
        """

        def __init__(self, parser):
            """
            constructor

            @param      parser      parser used to parse the code
            """
            MokadiGrammarListener.__init__(self)
            self.buffer = None
            self.level = -1
            self.parser = parser
            self.solution = []
            self.text_type = []

        @property
        def Result(self):
            """
            results
            """
            return self.solution

        def visitTerminal(self, node):
            """
            event
            """
            t = self.get_type(node.parentCtx, True)
            self.buffer[self.level].append((node.getText(), t))
            self.text_type.append((node.getText(), t))

        def visitErrorNode(self, node):
            """
            event
            """
            buffer = []
            text = ("    " * self.level) + "error: " + str(node)
            buffer.append(text)
            buffer.append(" ***" + str(node))
            buffer.append(" ***" + str(type(node)))
            buffer.append(" ***" + str(node.__dict__))
            buffer.append(" ###" + str(node.symbol))
            buffer.append(" ###" + str(type(node.symbol)))
            buffer.append(" ###" + str(node.symbol.__dict__))
            buffer.append(" ---" + str(node.parentCtx))
            buffer.append(" ---" + str(type(node.parentCtx)))
            buffer.append(" ---" + str(node.parentCtx.__dict__))
            raise MokadiException("\n".join(buffer))

        def istypeof(self, ch):
            """
            Annotation a specific node of the grammar.

            @param      ch      context, node
            @return             string or None

            This function is not efficient, it should be rewritten with
            a kind a dictionary.
            """
            if isinstance(ch, self.parser.ParseContext):
                return ":P:"
            if isinstance(ch, self.parser.MokadiContext):
                return ":MOKADI:"
            if isinstance(ch, self.parser.Slides_stmtContext):
                return ":slide_exp:"
            if isinstance(ch, self.parser.SlidesContext):
                return ":slide:"
            if isinstance(ch, self.parser.Word_nameContext):
                return ":word:"
            if isinstance(ch, self.parser.Word_name_extContext):
                return ":word:"
            if isinstance(ch, self.parser.OperatorContext):
                return ":op:"
            if isinstance(ch, self.parser.Verb_voirContext):
                return ":verb_voir:"
            if isinstance(ch, self.parser.Mail_stmtContext) or \
                    isinstance(ch, self.parser.MailsContext):
                return ":mails:"
            if isinstance(ch, self.parser.QuestionContext):
                return ":question:"
            if isinstance(ch, self.parser.NewsContext):
                return ":news:"
            if isinstance(ch, self.parser.News_queryContext):
                return ":query:"
            if isinstance(ch, self.parser.AproposContext):
                return ":apropos:"
            if isinstance(ch, self.parser.News_stmtContext):
                return ":news:"
            if isinstance(ch, self.parser.Time_indicationContext):
                return ":time_indication:"
            if isinstance(ch, self.parser.Integer_numberContext):
                return ":int:"
            if isinstance(ch, self.parser.Integer_number_stringContext):
                return ":int:"
            if isinstance(ch, self.parser.Number_nameContext):
                return ":int:"
            if isinstance(ch, self.parser.Questions_markContext):
                return ":question_mark:"
            if isinstance(ch, self.parser.Stop_wordsContext):
                return ":stopword:"
            if isinstance(ch, self.parser.PresentationContext):
                return ":presentation:"
            if isinstance(ch, self.parser.Emotion_stmtContext):
                return ":emotion:"
            if isinstance(ch, self.parser.HumeurContext):
                return ":emotion:"
            if isinstance(ch, self.parser.Possessif_meContext):
                return ":a_moi:"
            if isinstance(ch, self.parser.Anything_stmtContext):
                return ":anything:"
            if isinstance(ch, self.parser.With_bodyContext):
                return ":entier:"
            if isinstance(ch, self.parser.EntierContext):
                return ":entier:"
            if isinstance(ch, self.parser.NumeroContext):
                return ":numero:"
            if isinstance(ch, self.parser.DefinitionContext):
                return ":definition:"
            if isinstance(ch, self.parser.SynonymeContext):
                return ":synonym:"
            if isinstance(ch, self.parser.Expression_stmtContext) or \
                    isinstance(ch, self.parser.ExpressionContext):
                return ":expression:"
            return None

        def get_type(self, ctx, children=False, exc=True):
            """
            Extract the type of a context.

            @param      ctx         ctx
            @param      children    look into the children
            @param      exc         raise an exception if not found
            @return                 type as a string
            """
            t = self.istypeof(ctx)
            if t is not None:
                return t
            if children:
                ctxi = ctx
                while ctxi is not None:
                    for ch in ctxi.getChildren():
                        t = self.istype(ch)
                        if t is not None:
                            return t
                    ctxi = ctxi.parentCtx

            # error
            if exc:
                keep = [ctx]
                ctxi = ctx
                while ctxi is not None:
                    for ch in ctxi.getChildren():
                        keep.append(ch)
                    ctxi = ctxi.parentCtx
                mes = "\n".join(str(type(_)) for _ in keep)
                raise MokadiException("Unable to get type of \n" + mes)
            return None

        def enterEveryRule(self, ctx):
            """
            event
            """

            ty = self.get_type(ctx)
            text = ctx.getText()
            # text = self.parser._input.LT(1).text
            li = []
            if self.level == -1:
                self.buffer = []
            else:
                self.buffer[self.level].append(li)
            self.buffer.append(li)
            li.append(("enter", text, ty, ctx.start.line, ctx.start.column))
            self.level += 1

        def exitEveryRule(self, ctx):
            """
            event
            """
            ty = self.get_type(ctx)
            text = ctx.getText()
            self.buffer[self.level].append(
                ("leave", text, ty, ctx.start.line, ctx.start.column))
            self.level -= 1
            if self.level == -1:
                self.solution.append(self.buffer.copy())
            self.buffer.pop()

    walker = ParseTreeWalker()
    listen = TreeStringListener(parser)
    walker.walk(listen, tree)
    return listen.Result, listen.text_type
