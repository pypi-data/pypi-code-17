"""
A Pygments_ style based on the blackboard theme of TextMate_.

.. _Pygments: http://pygments.org
.. _TextMate: https://macromates.com
"""
from pygments.style import Style
from pygments.token import Token, Comment, Name, Keyword, Generic, Number
from pygments.token import Operator, String, Text, Error

white            = '#ffffff'
bright_orange    = '#f26512'
yolk_yellow      = '#f8d734'
lemon_yellow     = '#BBF34E'
bright_green     = '#62d04e'
dark_green       = '#0B3222'
dark_red         = '#370B22'
medium_grey      = '#AEAEAE'
really_dark_blue = '#0d152c'
dark_blue        = '#181f35'
medium_blue      = '#172247'
light_blue       = '#84A7C1'
vivid_blue       = '#36428a'

class BlackboardStyle(Style):
    color = white
    background_color = really_dark_blue
    highlight_color = vivid_blue

    styles = {
        Text: white,

        Keyword: yolk_yellow,
        Keyword.Constant: lemon_yellow,
        #Keyword.Declaration
        #Keyword.Namespace
        #Keyword.Pseudo
        #Keyword.Reserved
        Keyword.Type: light_blue,

        #Name
        #Name.Attribute
        Name.Builtin: light_blue,
        #Name.Builtin.Pseudo
        Name.Class: bright_orange,
        Name.Constant: lemon_yellow,
        #Name.Decorator
        #Name.Entity
        #Name.Exception
        Name.Function: bright_orange,
        #Name.Label
        #Name.Namespace
        #Name.Other
        #Name.Tag
        #Name.Variable
        #Name.Variable.Class
        #Name.Variable.Global
        #Name.Variable.Instance

        #Literal
        #Literal.Date
        String: bright_green,
        #String.Backtick
        #String.Char
        #String.Doc
        #String.Double
        #String.Escape
        #String.Heredoc
        #String.Interpol
        #String.Other
        #String.Regex
        #String.Single
        #String.Symbol

        Number: lemon_yellow,
        #Number.Float
        #Number.Hex
        #Number.Integer
        #Number.Integer.Long
        #Number.Oct

        #Operator
        #Operator.Word

        #Punctuation

        Comment: medium_grey,
        #Comment.Multiline
        #Comment.Preproc
        #Comment.Single
        #Comment.Special

        #Generic
        #Generic.Deleted
        Generic.Emph: 'italic',
        #Generic.Error
        #Generic.Heading
        #Generic.Inserted
        #Generic.Output
        #Generic.Prompt
        Generic.Strong: 'bold',
        #Generic.Subheading
        #Generic.Traceback

        #Token
        #Token.Other
    }
