from .log import Pane, L
from .lib import File, Files
from Niff import payloads
from copy import copy
import os
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

    f = language_api.ls()
    p.add_c(f.fs)

    def change(pane, key):
        item = File.got(pane.cur)
        pane.bottom_bar(item.name,item.time, item.size, item.perm, "| ",language_api.pwd)

    
    def up_down(pane, key):
        item = File.got(pane.cur)
        if item.name.endswith("/") or item.name.endswith("\\"):
            # language_api.cd(item.name)
            pane.set_c(1,language_api.ls(item.name).fs)
        else:
            try:
                pane.del_c(1)
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
            language_api.cd(pane.cur)
            father.append(copy(pane.columns[0]))
            sub = language_api.ls().fs
            try:
                pane.del_c(1)

            except:
                pass
            pane.del_c(0)
            pane.add_c(sub)
        change(pane, key)
    
    def l(pane, key):
        global father
        global father_loc
        # item = File.got(pane.cur)
        if language_api.pwd in language_api.disks:
            return
        cur = copy(pane.columns[0])
        language_api.cd("..")
        try:
            pane.del_c(1)
        except:
            pass
        pane.del_c(0)
        if father:
            pane.add_c(father.pop())
            
        else:
            pane.add_c(language_api.ls().fs)

        if father_loc:
            pane.loc = father_loc.pop()
        else:
            pane.loc = [0,0]

        if len(pane.locs) > 1:

            pane.locs = pane.locs[1:]
        else:
            pane.locs = [pane.loc[1]]
        
        change(pane, key)

    def search(pane, key):
        # old = 
        key_map = pane.key_map.copy()
        key_map_after = pane.key_map_after.copy()
        key_map_before = pane.key_map_before.copy()
        key_map_move = pane.key_map_move.copy()

        pane.key_map
        pane.bottom_bar("start search >>")

        def search_listen(pane, k):
            not_found_search_str = ''
            if k == '\n':
                pane.key_map = key_map
                pane.key_map_after = key_map_after
                pane.key_map_before = key_map_before
                pane.key_map_move = key_map_move
                pane.bottom_bar("search mode exit.")
                return

            dirs = pane.columns[pane.loc[0]]
            if hasattr(pane, 'search_str'):
                pane.search_str += k
            else:
                pane.search_str = k

            # deal with special char
            if ord(k) == 127:
                pane.search_str = pane.search_str[:-2]

            
            

            loc = copy(pane.loc)
            s_str = pane.search_str
            found = False
            for i,d in enumerate(dirs):
                if s_str in d:
                    loc[1] = i
                    found = True

            if not found:
                not_found_search_str = pane.search_str
                pane.search_str = ''
                if pane.search_str == 'exit':
                    pane.key_map = key_map
                    pane.key_map_after = key_map_after
                    pane.key_map_before = key_map_before
                    pane.key_map_move = key_map_move
            else:
                if loc[1] > pane.loc[1]:
                    for i in range(loc[1] - pane.loc[1]):
                        pane.move("down")
                    change(pane, k)
                elif loc[1] < pane.loc[1]:
                    for i in range(pane.loc[1] - loc[1]):
                        pane.move("up")
                    change(pane, k)

            if not found:
                pane.bottom_bar("search not found " + "("+ not_found_search_str + ") >>" )
            else:
                pane.bottom_bar("search > ", pane.search_str)
                


            # change(pane, k)
        pane.key_map_after =  dict()
        pane.key_map = dict()
        pane.key_map_before = dict()
        pane.key_map_move = dict()
        [pane.set_on_keyboard_listener(i, search_listen) for i in 'qwertyuiopasdfghjklzxcvbnm1234567890`~!@#$%^&*()-=_+.\n']
        pane.set_on_keyboard_listener('\x7f', search_listen)
        

            

            # change(pane)




    p.set_after_keyboard_listener('k', up_down)
    p.set_after_keyboard_listener('j', up_down)
    p.set_after_keyboard_listener('h', l)
    p.set_on_keyboard_listener('l', r)

    # for kinds of modes
    p.set_on_keyboard_listener('f', search)

    p.on_keyboard()

