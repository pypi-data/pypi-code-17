from .log import Pane, L
from .lib import File, Files
from Niff import payloads
from copy import copy
from string import printable
from termcolor import colored
import os

ALL_KEY = printable + '\x7f'
ALL_KEY = ALL_KEY.replace('\t','').replace('\x0b','').replace('\x0c','').replace('\r','')


father = []
father_loc = []

def ranger(target, passwd, LanguageApiName, charset='utf8'):
    """
    @LanguageApiName : now support php
    """
    p = Pane()
    LanguageApi = getattr(payloads, LanguageApiName)
    language_api = LanguageApi(target, passwd, charset='gbk')
    language_api.init()

    this = language_api.ls()
    f = language_api.ls('..')
    p.add_c(f.fs)
    p.add_c(this.fs)
    p.move('right')
    # p.locs = [0,0]

    def change(pane, key):
        item = File.got(pane.cur)
        pane.bottom_bar(len(pane.locs), len(pane.columns),item.name,item.time, item.size, item.perm, "| ",language_api.pwd)

    
    def up_down(pane, key):
        item = File.got(pane.cur)
        if item.name.endswith("/") or item.name.endswith("\\"):
            # language_api.cd(item.name)
            fs = language_api.ls(item.name).fs
            if fs:
                pane.set_c(2,fs)
            else:
                item.is_dir = False
                try:
                    pane.del_c(2)
                except :
                    pass

        else:
            try:
                pane.del_c(2)
            except :
                pass
        change(pane, key)

    def r(pane, key):
        global father_loc
        global father
        father_loc.append(pane.loc)
        item = File.got(pane.cur)

        if item.name.endswith("/") or item.name.endswith("\\"):
            # language_api.cd(item.name)
            # pane.clear()
            sub = language_api.ls(pane.cur).fs
            if sub:
                language_api.cd(pane.cur)
                fa = copy(pane.columns[0])
                cu = copy(pane.columns[1])
                father.append(fa)
            
                try:
                    pane.del_c(0)
                    pane.del_c(1)
                    pane.del_c(2)
                except:
                    pass
                
                pane.set_c(0, cu)
                pane.add_c(sub)
        up_down(pane, key)
    
    def l(pane, key):
        global father
        global father_loc
        # item = File.got(pane.cur)
        if language_api.pwd in language_api.disks:
            return
        cur = copy(pane.columns[1])
        fa = copy(pane.columns[0])
        language_api.cd("..")
        try:
            pane.del_c(0)
            pane.del_c(1)
            pane.del_c(2)
        except:
            pass
        
        if father:
            # pane.set_c(0, pop())
            pane.set_c(0,father.pop())
            pane.set_c(1,fa)
            pane.set_c(2,cur)
            
        else:
            pane.set_c(0,language_api.ls('..').fs)
            pane.set_c(1,fa)
            pane.set_c(2,cur)

        if father_loc:
            pane.loc = father_loc.pop()
        else:
            pane.loc = [1,0]

        # if len(pane.locs) > 2:

        #     pane.locs = pane.locs[1:]
        # else:
        pane.locs = [0,0,pane.loc[1]]
        fa = language_api.pwd.split(language_api.delta)[-1]
        pane.loc_to(0, fa)
        # up_down(pane, key)
        change(pane, key)

    def on_cmd(pane, key):
        
        pane.change_mode(Pane.CMD_MODE)
        pane.bottom_bar("Enter cmd mode: type'\\n\\n' to exit")
        if not hasattr(pane, 'cmd_str'):
            pane.cmd_str = ''
        # language_api.init()
        def cmd(pane, key):
            if key == '\n':

                if hasattr(pane, 'enter'):
                    pane.change_mode(Pane.DIR_MODE)
                    del pane.enter
                    pane.bottom_bar("Exit cmd mode!")
                    try:
                        pane.del_c(2)
                    except IndexError:
                        pane.del_c(1)

                    change(pane, key)
                    return
                else:
                    setattr(pane, 'enter', '\n')
                

                if hasattr(pane, 'cmd_str'):
                    if pane.cmd_str.startswith("cd"):
                        d = pane.cmd_str.split()[1:]
                        if d:
                            language_api.cd(d[0])
                            pane.cmd_str = ''
                            pane.bottom_bar(language_api.user, language_api.os.split()[0],"|", language_api.pwd, colored(">" + pane.cmd_str, 'cyan',attrs=['underline']), color='yellow')
                            return
                        else:
                            return

                    if len(pane.columns) == 1:
                        fa_res = []
                        pass
                    else:
                        fa_res = pane.columns[len(pane.columns) - 1][1:]
                        pane.del_c(len(pane.columns) - 1)

                    real_content =  language_api.cmd(pane.cmd_str).split("\n")
                    real_content = ['-' * (int(int(pane.w - pane.now_w) / 4) )  + '  Shell. ' + '-' * (int((pane.w - pane.now_w) /4) -1 )] + real_content
                    real_content += ['-' * int((pane.w - pane.now_w)/2) ]
                    real_content += fa_res
                    pane.add_c(real_content)
                    pane.set_c_attr(len(pane.columns) - 1, color='red')
                    
                    
                    pane.cmd_str = ''

                

            else:
                pane.cmd_str += key
                if hasattr(pane, 'enter'):
                    del pane.enter

            if ord(key) == 127:
                pane.cmd_str = pane.cmd_str[:-2]

            pane.bottom_bar(language_api.user, language_api.os.split()[0],"|", language_api.pwd, colored(">" + pane.cmd_str, 'cyan',attrs=['underline']), color='yellow')

        [pane.set_on_keyboard_listener(i, Pane.CMD_MODE, cmd) for i in ALL_KEY ]

    p.set_after_keyboard_listener('k',Pane.DIR_MODE, up_down)
    p.set_after_keyboard_listener('j',Pane.DIR_MODE, up_down)
    p.set_after_keyboard_listener('h',Pane.DIR_MODE, l)
    p.set_on_keyboard_listener('l',Pane.DIR_MODE, r)
    p.set_on_keyboard_listener('c', Pane.DIR_MODE, on_cmd)
    # [p.set_after_keyboard_listener(i, Pane.DIR_MODE | Pane.SEARCH_MODE , change) for i in 'hjkl']

    # for kinds of modes

    p.on_keyboard()

