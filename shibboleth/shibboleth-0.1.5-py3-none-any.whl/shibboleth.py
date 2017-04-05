import cmd
import glob
import os
import re
import sys

from datetime import datetime

DEFAULT_COLORS = {
    '1-now': 31, #red
    '2-next': 34, #blue
    '3-soon': 92, #light green
    '4-later': 32, #green
    '5-someday': 90, #dark gray
    '6-waiting': 95, # light pink?
}
TAG_PATTERN = r'\[(.*)\]'
PRIORITIES = {
    '1':'1-now',
    '2':'2-next',
    '3':'3-soon',
    '4':'4-later',
    '5':'5-someday',
    '6':'6-waiting',
}


class Filename:
    def __init__(self, filename):
        self.tags = []
        tags_found = re.search(TAG_PATTERN, filename)
        if tags_found:
            self.tags.extend(tags_found.groups()[0].split())
        if '1-now' in self.tags:
            self._priority = '1-now'
        elif '2-next' in self.tags:
            self._priority = '2-next'
        elif '3-soon' in self.tags:
            self._priority = '3-soon'
        elif '4-later' in self.tags:
            self._priority = '4-later'
        elif '5-someday' in self.tags:
            self._priority = '5-someday'
        elif '6-waiting' in self.tags:
            self._priority = '6-waiting'
        else:
            self._priority = None
        self.filename = filename

    @property
    def colorized(self):
        filename = self.filename
        for tag in self.tags or []:
            color = DEFAULT_COLORS.get(tag, '32')
            colorized = f'\x1b[{color}m{tag}\x1b[0m'
            filename = filename.replace(tag, colorized)
        return filename

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        if self._priority:
            head, _, tail = self.filename.rpartition(self._priority)
            filename = f'{head}{value}{tail}'
            self.tags.remove(self._priority)
        else:
            head, _, tail = self.filename.rpartition(']')
            filename = f'{head} {value}]{tail}'
        self._priority = value
        self.tags.append(value)
        os.rename(self.filename, filename)
        self.filename = filename


class Shibboleth(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.prompt = f'\N{RIGHTWARDS HARPOON WITH BARB UPWARDS}\x1b[34mshibboleth\x1b[0m:{os.getcwd()}\n>'
        self.selected = None

    def cmdloop(self):
        while True:
            try:
                super().cmdloop()
                break
            except KeyboardInterrupt:
                print()
                print('^C caught - use `q` to quit')

    def postcmd(self, stop, line):
        self.prompt = f'\N{RIGHTWARDS HARPOON WITH BARB UPWARDS}\x1b[34mshibboleth\x1b[0m:{os.getcwd()}\n>'
        if self.selected:
            self.prompt = f'\N{RIGHTWARDS HARPOON WITH BARB UPWARDS}\x1b[34mshibboleth\x1b[0m:{self.selected.colorized}\n>'
        return stop

    def do_cd(self, line):
        try:
            os.chdir(line)
        except Exception as e:
            print(e)

    def complete_cd(self, text, line, begidx, endidx):
        paths = glob.glob(text+'*')
        return paths

    def do_pls(self, line):
        '''
        Priority list - list files in the folder that have the
        specified priority.
        '''
        files = [Filename(name) for name in os.listdir(os.path.curdir)]
        targets = {
            '1': '1-now',
            '2': '2-next',
            '3': '3-soon',
            '4': '4-later',
            '5': '5-someday',
            '6': '6-waiting',
        }
        if line:
            try:
                target = targets[line]
            except KeyError:
                print(f'Unknown priority {line!r}')
                target = None

        for file_ in files:
            if not line or line == '1':
                if '1-now' in file_.tags:
                    print(file_.colorized)
            elif target:
                if target in file_.tags:
                    print(file_.colorized)

    def do_now(self, line):
        self.do_pls(line='1')

    def do_next(self, line):
        self.do_pls(line='2')

    def do_soon(self, line):
        self.do_pls(line='3')

    def do_later(self, line):
        self.do_pls(line='4')

    def do_someday(self, line):
        self.do_pls(line='5')

    def do_waiting(self, line):
        self.do_pls(line='6')

    def do_deselect(self, line):
        self.selected = None

    def do_select(self, line):
        if not line:
            self.do_deselect()
        else:
            if not os.path.isfile(line):
                print(f'Unknown file {line!r}')
            else:
                self.selected = Filename(os.path.abspath(line))

    def complete_select(self, text, line, begidx, endidx):
        paths = glob.glob(text+'*')
        return paths

    def complete_edit(self, text, line, begidx, endidx):
        return complete_select

    def do_priority(self, line):
        if not self.selected:
            print('Select a file first and try again')
        else:
            try:
                self.selected.priority = PRIORITIES[line]
            except KeyError:
                print(f'Unknown priority {line!r}')

    def do_ls(self, line):
        line = os.path.expanduser(line)
        if not line:
            files = os.listdir(os.path.curdir)
        elif os.path.isdir(line):
            files = os.listdir(line)
        else:
            files = glob.glob(line)
        for filename in files:
            print(Filename(filename).colorized)

    def do_show(self, line):
        if not self.selected or line:
            print('Select a file and try again')
        else:
            filename = self.selected.filename if self.selected else line
            print('*'*80)
            with open(filename) as f:
                print(f.read())
            print('*'*80)

    def do_edit(self, line):
        if not self.selected or line:
            print('Select a file and try again')
        else:
            filename = self.selected.filename if self.selected else line

        try:
            editor = os.environ['EDITOR']
        except KeyError:
            print('Set environment EDITOR and try again')
        else:
            os.system(f'{editor} "{filename}"')

    def do_complete(self, line):
        if not self.selected or line:
            print('Select a file and try again')
        else:
            filename = self.selected.filename if self.selected else line
        os.rename(
            filename,
            os.path.join(
                os.path.dirname(filename),
                'completed',
                os.path.basename(filename),
            ),
        )
        self.selected = None

    def do_new(self, line):
        title = line if line else input('Title: ').strip()
        filename = f'{title}[{datetime.now():%Y%m%d~%H%M%S}].md'
        try:
            editor = os.environ['EDITOR']
        except KeyError:
            print('Set environment EDITOR and try again')
        else:
            os.system(f'{editor} "{filename}"')
        self.do_select(filename)

    def do_exit(self, line):
        print('Goodbye!')
        return True

    def do_EOF(self, line):
        print()
        return self.do_exit(line)

    def do__debug(self, line):
        import pdb; pdb.set_trace()

    # Aliases
    do_p = do_priority
    do_e = do_edit
    do_sel = do_select
    do_quit = do_exit
    do_q = do_exit
    complete_sel = complete_select
    complete_e = complete_edit


def colorfy(filename):
    tags_found = re.search(tag_pattern, filename)
    tags = None
    if tags_found:
        tags = tags_found.groups()[0].split()
        for tag in tags:
            color = DEFAULT_COLORS.get(tag, '32')
            colorized = f'\x1b[{color}m{tag}\x1b[0m'
            filename = filename.replace(tag, colorized)
    return filename, tags


def run():
    # I'll never ever write a song about the shibby
    shibby = Shibboleth()
    if sys.argv[1:]:
        shibby.onecmd(' '.join(sys.argv[1:]))
    else:
        shibby.cmdloop()

if __name__ == '__main__':
    run()
