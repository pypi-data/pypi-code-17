import re
import argparse
import sys
import string
import operator
import os
import fileinput

def Error(message, number):
    if(len(message) >= 1):
        sys.stderr.write("{} {}\n".format(message,number))
    os._exit(number)

def ExitSuccess(message):
    sys.stdout.write(message)
    os._exit(0)

class Regex:

    def __init__ (self, string):
        self.regex = ""

        self.parse_regex (string)

    def parse_regex (self, string):
        a = ""
        last = ""
        final = ""
        norm, spec, dot = 0 , 1, 2
        stat = norm
        neg = False
        negs = 0
        nqs = True
        dots = 0
        braces = 0
        if(nqs):
            string = re.sub("(\*+)"  ,"*", string)#reduce multiple*
            string = re.sub("(\++)"  ,"+", string)#reduce multiple+
            string = re.sub("(\+\*+)","*", string)#replace + if followed by *
            string = re.sub("(\*\++)","*", string)#delete + if follows *
            string = re.sub("(\*\*+)","*", string)#reduce multiple*which remain
        #print("\nBEGIN:{}".format(string))
        """
        priorities
        ! > *,+ > . > |
        ! is closed by *+ stat == norm elif
        ! is closed by .| stat == norm else
        *+ does not need to by closed by .| works fine
        . is closed by |  stat == norm else
        . is closed at the ned of this for in loop
        """
        #(!abc|
        #([^abc
        for ind,i in enumerate(string):
            if(string[ind-1] in [".", "!", "|"]):
                if(i in [".", "!", "|"] ):
                    Error("Regex error", 4)
            if(neg and i == "|"):
                final += "]|"
                neg = False
                negs -= 1
                continue
            if(dots >= 1):
                if(i in ["|"]):
                    final += ")|"
                    dots -= 1
                    continue

            if(stat == norm):
                if(i == "%"):
                    stat = spec
                #TODO
                elif(i in ["*", "+"]):
                    if(neg and cbraces == braces):
                        final += "]"
                        neg = False
                        negs -= 1
                    final += "+"
                elif(i == "!"):
                    final += "[^"
                    neg = True
                    negs += 1
                    cbraces = braces
                elif(i in ["[", "]", "\\", "^", "$", "{", "}", "?"]):
                    final += "\\" + i
                else:
                    if(i == "("):
                        braces += 1
                    elif(i == ")"):
                        braces -= 1
                    elif(i == "."):
                        if(neg and cbraces == braces):
                            final += "]"
                            neg = False
                            negs -= 1
                        dots += 1
                        final += "("
                        continue
                    final += i
                    if(neg and cbraces == braces):
                        final += "]"
                        neg = False
                        negs -= 1
            elif(stat == spec):
                stat = norm
                #whitespace
                if(i == "s"):
                    final += "\\s"
                #random char
                elif(i == "a"):
                    final += "(\n|.)"
                #digit
                elif(i == "d"):
                    final += "\\d"
                #small letter
                elif(i == "l"):
                    final += "[a-z]"
                #BIG LETTERS
                elif(i == "L"):
                    final += "[A-Z]"
                #case insensitive letters
                elif(i == "w"):
                    final += "[a-zA-Z]"
                #letters and numbers
                elif(i == "W"):
                    final += "[a-zA-Z0-9]"
                #tab
                elif(i == "t"):
                    final += "\\t"
                #newline
                elif(i == "n"):
                    final += "\\n"
                elif(i in [".", "|", "!", "*", "+", "(", ")", "%"]):
                    final += ("\\"+i)
                else:
                    Error("Error in regex", 4)

                if(neg and braces == cbraces):
                    final += "]"
                    negs -= 1
                    neg = False
                continue
        while(dots >= 1):
            final += ")"
            dots -= 1
        while(negs >= 1):
            finla += "]"
            negs -= 1
        if(re.search("\.{2}", final)):
            Error("Regex error", 4)
        
        self.regex = final
        #print("FINAL:{}\n".format(final))

class Tag:

    def __init__ (self, begin, end):
        self.begin_len = len(begin)
        self.end_len = len(end)
        self.beg_tag = begin
        self.end_tag = end

class Rule:

    def __init__(self, line):
        self.regex = ""
        self.tags = []
        self.matches = []
        self.run (line)

    def run (self, line):
        regex, rules = self.parse_line (line)
        self.check_regex(regex)
        self.check_rules(rules)


    def add_match(self, tup):
        occ = [tup[0],tup[1]]
        self.matches.append(occ)

    def check_rules (self, string):
        rulesclear = []
        #print("This rule is: {}".format(string))
        #TODO
        self.check_format_tags (string)
        rules = re.compile("[\,(\t|\ )+]").split(string)
        for i in rules:
            if(len(i) > 0):
                #trim newline char
                if(i[len(i)-1] == '\n'):
                    rulesclear.append(i[:-1])
                else:
                    rulesclear.append(i)

        self.parse_rules (rulesclear)

    @staticmethod
    def check_format_tags (string):
        try:
            ge =re.search("^\w+(\:[0-9A-F]{1,6})?(\,(\t|\ )+\w+(\:[0-9A-F]{1,6})?)*$", string)
        except:
            Error("format file error", 4)
        if(None == ge ):
            Error("Error in format file", 4)

    def parse_line (self, line):
        try:
            linesplit = re.split("\t", line, 1)
            regex = linesplit[0]
            rules = linesplit[1]
            while(rules[0] == '\t'):
                rules = rules[1:]
            rules = re.sub("\t+", "\t", rules)
            return regex, rules
        except:
            Error("Format file error", 4)

    #check if rules are correct
    #@list_rules - list of rules to be checked
    def parse_rules (self, list_rules):
        for rule in list_rules:
            if(re.compile("bold").match(rule)):
                 self.tags.append(Tag ('<b>', '</b>'))
            elif(re.compile("italic").match(rule)):
                 self.tags.append(Tag ('<i>', '</i>'))
            elif(re.compile("underline").match(rule)):
                 self.tags.append(Tag ('<u>', '</u>'))
            elif(re.compile("teletype").match(rule)):
                 self.tags.append(Tag ('<tt>', '</tt>'))
            elif(re.compile("^size\:[1-7]{1}").match(rule)):
                size = rule.split(":")
                size = size[1]
                self.tags.append(Tag ('<font size='+size+'>', '</font>'))
            elif(re.compile("^color\:[0-9A-F]{6}$").match(rule)):
                color = rule.split(":")
                color = color[1]
                self.tags.append(Tag ('<font color=#'+color+'>', '</font>'))
            else:
                Error("Error in format file", 4)


    def check_regex (self, string):
        self.regex = Regex(string)

class Simple_rule:

    def __init__ (self, match, tags):
        self.match = match
        self.tags = tags

class App:

    stdout = True
    use_br = False
    escape = False
    nooverlap = False
    exit_with_infile = False
    infile = ""
    formatfile = ""

    def __init__(self, parser):
        self.open_tags = []
        self.rules = []
        self.applied_rules = []


        self.args (parser)
        self.run()


    def run (self):
        filein = ""
        newword = ""
        simple_rules = []
        if(App.infile):
            try:
                fp = open(App.infile, 'r')
            except:
                Error("Not such file or cannot be opened {}".format(App.infile), 2)

            filein = fp.read()
        else:
            filein = sys.stdin.read()

        #find matches and add to according rule
        try:
            for rule in self.rules:
                #sys.stderr.write(rule.regex.regex)
                for match in (re.finditer(rule.regex.regex, filein, re.MULTILINE)):
                    rule.add_match(match.span())
        except:
            Error("Regex error", 4)


        #divide Rule matches into simple matches for more easy management
        for rule in self.rules:
            for occ in rule.matches:
                simple_rules.append(Simple_rule(occ, rule.tags))

        #apply rules
        position = 0
        output = ""
        for char in filein:
            output += self.apply_rule(char, position, simple_rules)
            position += 1

        #apply tags at the end of input
        output += self.apply_rule("", position, simple_rules)

        #output
        if(App.stdout):
            sys.stdout.write(output)
        else:
            try:
                outfile = open(self.outfile, "w")
                outfile.write(output),
                outfile.close()
            except:
                Error("Output error", 3)


    def exitoverlap(self, newword, tag, readd_items, end):
        out = ""
        if(end):
            for t in reversed(self.open_tags):
                if(t == tag):
                    self.open_tags.remove(tag)
                    break
                out += t.end_tag
                readd_items.append(t)
        else:
            for t in readd_items:
                out += t.beg_tag
            readd_items = []
        return readd_items, out


    def apply_rule(self, char, position, rules):
        newword = ""
        readd_items = []
        #lets close what should be closed
        for rule in reversed(rules):
            if position == rule.match[1]:
                for tag in reversed(rule.tags):
                    if(self.nooverlap):
                        readd_items, r = self.exitoverlap(newword,
                                                                 tag,
                                                                 readd_items, True)
                        newword += r
                    newword += tag.end_tag
                    if(self.nooverlap):
                        readd_items, r = self.exitoverlap(newword, tag,
                                                                 readd_items, False)
                        newword += r
        #lets open what should be open
        for rule in rules:
            if position == rule.match[0]:
                for tag in rule.tags:
                    newword += tag.beg_tag
                    self.open_tags.append(tag)

        newword = self.add_current_char (newword, char)
        #escape tags extension
        return newword

    def add_current_char (self, newword, char):

        if(char == "\n" and self.use_br):
            newword += "<br />"

        if(self.escape):
            if(char == "<"):
                newword += "&lt;"
            elif(char == ">"):
                newword += "&gt;"
            elif(char == "&"):
                newword += "&amp;"
            else:
                newword += char
        else:
            newword += char
        return newword

    def args (self, parser):
        try:
            args = parser.parse_args()
        except SystemExit:
            Error("Wrong arguments used", 1)

        self.args = args
        if(args.displayhelp):
            print(parser.print_help())
            Error("", 0)
        if(args.infile):
            App.infile = args.infile
        if(args.formatfile):
            try:
                fileinfo = os.stat(args.formatfile)
                if(fileinfo.st_size == 0):
                    raise Exception()
                App.formatfile = open(args.formatfile, 'r')
                while True:
                    line = App.formatfile.readline()
                    #skip empty line
                    if( (line) == "\n"):
                        continue
                    if(not line):
                        break
                    rule = Rule (line)
                    self.rules.append(rule)
                App.formatfile.close()
            except:
                App.exit_with_infile = True
        if(args.outfile):
            self.outfile = args.outfile
            App.stdout = False
        if(args.brline):
            App.use_br = True
        if(args.nooverlap):
            App.nooverlap = True
        if(args.escape):
            App.escape = True

def main():
    parser = argparse.ArgumentParser(add_help=False,
    description="""
    This is the bestest description
    """)

    parser.add_argument('-h', '--help', action="store_true",
                        dest="displayhelp", help="display help", default=False)
    parser.add_argument('-f', '--format', action="store", dest="formatfile",
                        help="""set format file.""", default=False)
    parser.add_argument('-i', '--input', action="store", dest="infile",
                        help="set input file", default=None)
    parser.add_argument('-o', '--output', action="store", dest="outfile",
                        help="""set output file""", default=None)
    parser.add_argument('--br', action="store_true", dest="brline", help="""add
                        "br tag""", default=False)
    parser.add_argument('--nooverlap', action="store_true", dest="nooverlap",
                        help="""forbid using overlaping""", default=False)
    parser.add_argument('--escape', action="store_true", dest="escape",
                        help="""escape all html tags properly""", default=False)
    ininfo = App(parser)
if __name__ == "__main__":
    main()

