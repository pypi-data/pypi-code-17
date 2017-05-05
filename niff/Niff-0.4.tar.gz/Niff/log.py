import platform
import sys,os
from termcolor import colored
from contextlib import contextmanager
from .keyboard import on_keyboard_ready
from copy import copy
from string import ascii_letters, printable, digits, ascii_lowercase, ascii_uppercase
PY = platform.python_version()[:2]

ALL_KEY = printable + '\x7f'
ALL_KEY = ALL_KEY.replace('\t','').replace('\x0b','').replace('\x0c','').replace('\r','')

def L(*contents, **kargs):
    on = ''
    c = ''
    end = '\n'
    column = ''
    row = ''
    if 'on' in kargs:
        on = kargs['on']
    if 'color' in kargs:
        c = kargs['color']
    if 'end' in kargs:
        end = kargs['end']
    
    if 'c' in kargs:
        column = kargs['c']

    if 'r' in kargs:
        row = kargs['r']

    res = ' '.join([str(i) for i in contents])
    if c:
        if on:
            res = colored(res, c, on)
        else:
            res = colored(res, c)

    if row and column:
        with LogControl.jump(row,column):
            sys.stdout.write(res + end)
            sys.stdout.flush()
            return len(res+end)
    # if 'el' in kargs and 'c' in kargs and 'r' in kargs:
        
    sys.stdout.write(res + end)
    sys.stdout.flush()
    return len(res+end)

class Column:

    def __init__(self, *args):
        self.c = args
        max_len = 0
        count = 0
        for i in args:
            count += 1
            if len(i) > max_len:
                max_len = len(i)
        self.max_len = max_len
        self.count = count
        self.val = [('%-' + str(max_len) + 's') % i for i in self.c] 
    
    def __getitem__(self,k):
        return self.val[k]

    def __setitem__(self,k,v):
        if len(v) > self.max_len:
            self.max_len = len(v)

        self.val[k] = ('%-' + str(self.max_len) +'s') % v

    def add(self,v):
        if len(v) > self.max_len:
            self.max_len = len(v)
        self.val.append(('%-' + str(self.max_len) +'s') % v)
        self.count += 1

    def find(self, val):
        for i,v in enumerate(self.val):
            if val == v:
                return i
        return -1


class Pane:
    """
    this is a ui class template. 
     include three mode:
        dir mode
        cmd mode (need to implement)
        search mode
    """
    DIR_MODE = 1
    CMD_MODE = 2
    SEARCH_MODE = 4

    def __init__(self):
        
        self.mark = dict()
        self.size = LogControl.got_size()

        self.lines = ['%s' for i in range(self.size[0])]
        self.columns =[]
        self.loc = [0,0]
        self.max_row = 0
        self.cc = 1
        self.now_w = 0

        self.locs = []
        self.key_map = dict()
        self.key_map_after = dict()
        self.key_map_before = dict()
        self.key_map_move = dict()
        self.mode = Pane.DIR_MODE

        self.bak_key_map = dict()
        self.columns_show_attrs = dict()


        [self.set_before_keyboad_listener(i, Pane.DIR_MODE, self.on_count)  for  i in '123456789']
        [self.set_move_keyboard_listener(i, Pane.DIR_MODE, self.on_move) for i in 'hjkl' ]
        [self.set_on_keyboard_listener(i, Pane.SEARCH_MODE, self.on_search) for i in ALL_KEY ]
        self.set_on_keyboard_listener('f', Pane.DIR_MODE, self.on_search_mode_listener)

        # self.key_map_move['j'] = move

    def on_count(self, panel, key):
        self.cc = int(key)

    def change_mode(self, mode):
        # save now mode keymap
        # for k in self.key_map:
        #     if not self.key_map[k][0]  & mode:
        #         self.bak_key_map[self.mode] = 


        if mode not in [1,2,4]:
            raise Exception("only suport mode : \nDIR_MODE = 1 \nCMD_MODE = 2 \nSEARCH_MODE = 4 ")
        self.mode = mode

    def on_move(self, pane, ch):
        if ch == "j":
            di = 'down'
            
        if ch == 'k':
            di = 'up'
        
        if ch == 'h':
            di = 'left'
        
        if ch == 'l':
            di = 'right'
        for i in range(self.cc):
            pane.move(di)

    def on_search_mode_listener(self, pane, k):
        pane.change_mode(Pane.SEARCH_MODE)
        pane.bottom_bar("start search >>")


    def on_search(self, pane, k):
        not_found_search_str = ''
        if k == '\n':
            pane.change_mode(Pane.DIR_MODE)
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
            
        else:
            if loc[1] > pane.loc[1]:
                for i in range(loc[1] - pane.loc[1]):
                    pane.move("down")
                # change(pane, k)
            elif loc[1] < pane.loc[1]:
                for i in range(pane.loc[1] - loc[1]):
                    pane.move("up")
                # change(pane, k)

        if not found:
            pane.bottom_bar("search not found " + "("+ not_found_search_str + ") >>" )
        else:
            pane.bottom_bar("search > ", pane.search_str)
    

    def move(self,d):
        if d == 'up':
            if self.loc[1] != 0:
                self.loc[1] -= 1
                self.locs[self.loc[0]] -= 1
                return True
        elif d == 'down':
            if self.loc[1] != self.columns[self.loc[0]].count -1:
                self.loc[1] += 1
                self.locs[self.loc[0]] += 1
                return True

        elif d == 'left':
            if self.loc[0] != 0:
                self.loc[0] -= 1
                self.loc[1] = self.locs[self.loc[0]]
                return True
                # self.locs[self.loc[0]] = self.loc[1]
                # if self.loc[1] >  self.columns[self.loc[0] ].count:
                    # self.loc[1] = self.columns[self.loc[0] ].count - 1
                    # self.locs[self.loc[0]] = self.columns[self.loc[0] ].count - 1

        elif d == 'right':
            if self.loc[0] != len(self.columns) - 1:
                self.loc[0] += 1
                self.loc[1] = self.locs[self.loc[0]]
                return True
                # self.locs[self.loc[0]] = self.loc[1]
                # if self.loc[1] >  self.columns[self.loc[0] ].count:
                    # self.loc[1] = self.columns[self.loc[0] ].count - 1
                    # self.locs[self.loc[0]] = self.columns[self.loc[0] ].count -1 


    @property
    def h(self):
        return self.size[0] -2

    @property
    def w(self):
        return self.size[1]

    def add_r(self,l):
        
        for i,c in enumerate(self.columns):
            try:
                c.add(l[i])
            except IndexError:
                self.add_c(Column(l[i]))
        self.max_row += 1



    def __setitem__(self,x_y,v):
        c = self.columns[x_y[0]]
        c[x_y[1]] = v

        if len(v) > c.max_len:
            self.now_w -= c.max_len
            c.max_len = len(v)
            self.now_w += c.max_len


    def __getitem__(self,x_y):
        if isinstance(x_y, list):
            return self.columns[x_y[0]][x_y[1]]
        elif isinstance(x_y, int):
            return self.columns[x_y]
        elif isinstance(x_y, str):
            raise IndexError("not such key")

        


    def add_c(self, c):
        if not isinstance(c, Column):
            c = Column(*c)
        self.columns.append(c)
        self.locs.append(0)
        if c.count > self.max_row:
            self.max_row = c.count

        self.now_w += c.max_len

    def del_c(self,n):
        self.now_w -= self.columns[n].max_len

        del self.columns[n]
        del self.locs[n]
        self.max_row = 0
        for c in self.columns:
            if self.max_row < c.count:
                self.max_row = c.count
        if self.loc[0] == n:
            self.loc = [0,0]
    
    def loc_to(self,n, val):
        dirs = self[n]
        i = dirs.find(val)
        if i < 0:
            i = 0
        self.locs[n] =  i


    def set_c(self, n, c):
        
        if not isinstance(c, Column):
            c = Column(*c)
        if c.count > self.max_row:
            self.max_row = c.count
        
        if n ==  len(self.columns):
            self.add_c(c)
        elif n < len(self.columns): 
            self.now_w -= self.columns[n].max_len
            self.columns[n] = c
            self.locs[n] = 0
        self.now_w += c.max_len

    def set_c_attr(self, n, color=None, on=None,attrs=[],width=None):
        if width == 'to_right':
            width = self.w - self.now_w - 2
        elif isinstance(width, int):
            pass
        
        
        self.columns_show_attrs[n] = {
                'color':color,
                'on':on,
                'attrs':attrs,
                'width':width
        }
        

    @property
    def cur(self):
        try:
            return self.columns[self.loc[0]][self.loc[1]].strip()
        except IndexError as e:
            L(self.loc,self.columns[self.loc[0]], color='red')
            raise e

    def cur_column(self, c):
        return self.columns[c][self.locs[c]].strip()

    def bottom_bar(self, *contents, color='red'):
        L(" "* (self.w - 4),r=self.h+1, c=1, end='')
        L(*contents, r=self.h+1,c=1,color='red',end='')

    def show(self, d = ' | '):

        with LogControl.jump(0,0):
            for i in range(self.h):
                l = ''
                
                for ic,c in enumerate(self.columns):
                    try:
                        if self.locs[ic] >= self.h:
                            m = c[i + self.locs[ic] - self.h + 1]

                            if self.h == i+1:
                                if ic == self.loc[0]:
                                    m = colored(m,'red',attrs=['underline'])
                                else:
                                    m = colored(m,'white','on_blue')
                            if ic in self.columns_show_attrs:
                                c = self.columns_show_attrs[ic]['color']
                                on = self.columns_show_attrs[ic]['on']
                                attr = self.columns_show_attrs[ic]['attrs']
                                width = self.columns_show_attrs[ic]['width']

                                m = colored(m, c, on, attrs=attr)
                                if width:
                                    m += ' ' * (width -20)

                        else:
                            m = c[i]
                            if self.locs[ic] == i:
                                if ic == self.loc[0]:
                                    m = colored(m,'red',attrs=['underline'])
                                else:
                                    m = colored(m,'white','on_blue')

                            if ic in self.columns_show_attrs:
                                c = self.columns_show_attrs[ic]['color']
                                on = self.columns_show_attrs[ic]['on']
                                attr = self.columns_show_attrs[ic]['attrs']
                                width = self.columns_show_attrs[ic]['width']
                                m = colored(m, c, on, attrs=attr)
                                if width:
                                    m += ' ' * (width -20)
     
                        l = l  + m + d

                        if len(l) > self.w:
                            l = l[self.w - len(l):]
                    except IndexError:
                        l = l + ('%-' + str(c.max_len) + 's') % ' ' + d
                padding = ' ' * (self.w - len(l) - 1)
                print(l + padding)
        # with LogControl.jump(0,self.h+1):
        # L(self.loc,r=self.h+1,c=60, end='')

    def _call(self, events, k):
        """
         to call function which  map to key.
        """

        if events:
            for mode, func in events:
                if func and mode & self.mode:
                    return func(self, k)

    def on_call(self, k):
        """
        happend after pressdown but before change anything.
        """
        events =  self.key_map.get(k)
        return self._call(events, k)
        # return self._call(mode, f, k)

    def after_call(self,k):
        """
        happend after change something.
        """
        events = self.key_map_after.get(k)
        return self._call(events, k)

    def before_call(self, k):
        """
        happend before on_call
        """
        
        events = self.key_map_before.get(k)
        return self._call(events, k)
        

    def move_call(self, k):   
        """
        special happend to 'hjkl' to handle move cursor.
        """
        events = self.key_map_move.get(k)
        return self._call(events, k)

    def clear(self):
        os.system("tput cl")

    def set_before_keyboad_listener(self, k, m, f):
        fun_map = self.key_map_before.get(k, set())
        fun_map.add((m,f))
        self.key_map_before[k] = fun_map

    def set_on_keyboard_listener(self, k, m, f):
        """
            set k ,f 
                f(self)
        """
        fun_map = self.key_map.get(k, set())
        fun_map.add((m,f))
        self.key_map[k] = fun_map
        # self.key_map[k] = 

    def set_after_keyboard_listener(self,k, m,f):
        
        fun_map = self.key_map_after.get(k, set())
        fun_map.add((m,f))
        self.key_map_after[k] = fun_map

    def set_move_keyboard_listener(self, k, m,f):
        fun_map = self.key_map_move.get(k, set())
        fun_map.add((m,f))
        self.key_map_move[k] = fun_map


    def on_keyboard(self, d=' ' + colored('|','blue') + ' '):
        LogControl.save()
        
        self.show(d)
        with on_keyboard_ready():
            try:
                cc = 1
                while 1:

                    ch = sys.stdin.read(1)
                    # self.clear()
                    if not ch or ch == chr(4):
                        break
                    # if self.mode & Pane.DIR_MODE:
                    self.before_call(ch)
                    self.on_call(ch)
                    
                    # if self.mode & Pane.DIR_MODE:
                    self.move_call(ch)
                    
                    self.after_call(ch)

                    # show main content. 
                    # then to display other info.
                    self.show(d)

                    # L(ord(ch), r=self.h+1, c=self.w-3,color='blue',end='')

            except (KeyboardInterrupt, EOFError):
                pass

        LogControl.load()



    # def add_columns(self, c):
        # for i in c:
            # 
    



class LogControl:
    INFO = 0x08
    ERR = 0x00
    OK = 0x04
    WRN = 0x02
    FAIL = 0x01
    LOG_LEVEL = 0x04

    SIZE = tuple([ int(i) for i in os.popen("tput lines && tput cols ").read().split()])

    @staticmethod
    def got_size():
        SIZE = tuple([ int(i) for i in os.popen("tput lines && tput cols ").read().split()])
        return SIZE

    @staticmethod
    def save(p='civis'):
        """
        civis set will let p hidden.
        cnorm set will let p display.
        """
        os.system("tput sc  && tput civis && tput " + p)

    @staticmethod
    def load():
        """
        civis set will let p hidden.
        cnorm set will let p display.
        """
        os.system("tput rc  && tput cnorm ")


    @staticmethod
    @contextmanager
    def jump(line, col):
        """
        @cur can set cursor display or hidden
        @line, @col: cursor to jump.
        """
        try:
            # if not cur:
            #     os.system("tput civis")
            os.system(" tput cup %d %d  " % (line, col))
            
            yield
        finally:
            # os.system("tput rc")
            pass



    @staticmethod
    def cl(line):
        os.system("tput sc  && tput cnorm  && tput cup %d 0 && tput el  && tput rc && tput cnorm")

    @staticmethod
    def loc(line, col, el=False):
        os.system("tput cup %d %d " % (line, col))
        if el:
            os.system("tput el")


# class Display:

#     def __init__(self, cur, *args,  r=1):
#         self.l = args
#         self.count = len(args)
#         self.pages = 0
#         str_l = 0
#         for s in args:
#             if len(s) > str_l:
#                 str_l = len(s)
#         self.max_len = str_l
#         self.cur = cur
#         self.key_map = dict()
#         self.last = None
#         self.next = None
#         self.root = None
#         self.r_guest = r

#     def bar(self,r,c,l,color='red',on='on_green'):
#         L(' '* l, color=color,on=on,r=r,c=c,end='')
#         L(' '* (LogControl.got_size()[0] - l), end='')

#     def move(self,di):
#         if di == 'up':
#             if self.cur != 0:
#                 self.cur -=1
#         elif di == 'down':
#             if self.cur != self.count - 1:
#                 self.cur += 1

#     def set_key_listener(self, key, func):
#         self.key_map[key] = func


#     def call(self, key,item):
#         f = self.key_map.get(key)
#         if f:
#             return f(item,self)



# class Card(Display):

#     def show(self, r_shift,mark='cu'):
#         if mark == 's':
#             self.bar(1, r_shift, self.max_len+1)
#         elif mark == 'p':
#             pass
#         elif mark == 'cu':
#             self.bar(1, r_shift, self.max_len+1, on='on_red')

#         l = LogControl.got_size()[0]
#         if self.count < l -2:
#             for i,v in enumerate(self.l + tuple([' '*self.max_len for i in range(l - self.count)])):
#                 if i == self.cur:
#                     # os.system("tput el")
#                     L(v , color='white',on='on_blue',c=r_shift,r=i+2, end='')
#                     L(' '* (l - len(v)),end='')

#                     continue
#                 L(v  ,c=r_shift,r=i+2, end='')
#                 L( ' '* (l - len(v)), end='')
#         else:
#             ff = self.l[self.pages:self.pages + LogControl.got_size()[0] - 2]
#             for i,v in enumerate(ff):
#                 if i == self.cur - self.pages :
#                     L(v, color='white',on='on_blue',c=r_shift,r=i+2, end='')
#                     continue
#                 L(v,c=r_shift,r=i+2, end='')


#     def cl(self):
#         os.system("tput cl ")


#     def key_show(self,init_f):

#         r_shift = init_f
#         self.show(r_shift)
#         with on_keyboard_ready():
#             try:
#                 cc = 1
#                 while 1:
#                     ch = sys.stdin.read(1)
#                     if not ch or ch == chr(4):
#                         break
#                     if ch in '123456789':
#                         cc = int(ch)

#                     if ch == 'j':
#                         # self.cl()
#                         for i in range(cc):
#                             self.move("down")
#                             if self.cur > LogControl.got_size()[0] - 3:
#                                 self.cl()
#                                 self.pages += 1

#                     elif ch == 'k':
#                         # self.cl()
#                         for i in range(cc):
#                             self.move("up")
#                             if self.cur > LogControl.got_size()[0] - 2:
#                                 self.cl()
#                                 if self.pages != 0:
#                                     self.pages -= 1


#                     # if ch == "l":
#                         # self.cur = 1
#                     if ch in 'jklh':
#                         self.show(r_shift)

#                     exit = self.call(ch, self.l[self.cur])
#                     if exit:
#                         break

                    
#             except (KeyboardInterrupt, EOFError):
#                 pass

# CC = 0
# def ranger():
    
#     LogControl.save()
#     f = os.listdir(".")
#     cu = Card(0,*f)
#     Card.father = cu
#     cu.cl()
#     cu.root = "."
#     p = None
#     s = None

#     def j(path, cu):
#         pp = os.path.join(cu.root, path)
#         if os.path.isdir(pp):
#             s = Card(-1, r=cu.max_len + cu.r_guest+ 5, *os.listdir(pp))
#             s.show(s.r_guest, mark='s')
#         # if cu.last:
#             # cu.last.show(1, mark='p')


#     def r(path, cu):
#         global CC
#         cu.cl()
        
#         pp = os.path.join(cu.root,path)
#         L(pp,r=0,c=0,end='')
#         if os.path.isdir(pp):
            
#             s = Card(0,r=5 + cu.max_len + 3,*os.listdir(pp))
#             cu.next = s
#             s.last = cu
#             s.root = pp
#             cu.show(1,mark='p')
#             cu = s
#             tmp = s
            
#             cu.key_map = cu.last.key_map
#             # if cu.r_guest + cu.max_len < LogControl.got_size()[1]:
#             #     while 1:
#             #         if tmp:
#             #             # L(tmp.root,tmp.r_guest, r=LogControl.got_size()[0],c=1,color='yellow',end='')
#             #             tmp.show(tmp.r_guest)
#             #             tmp = tmp.last
#             #         else:
#             #             break
#             #     cu.key_show(cu.r_guest)
#             # else:
#             #     cu.cl()
#             #     tmp = Card.father
#             #     now = 1
#             #     cc = 0
#             #     while 1:
#             #         if tmp:
#             #             # L(tmp.root,tmp.r_guest, r=LogControl.got_size()[0],c=1,color='yellow',end='')
                        
#             #             tmp = tmp.next
#             #             if tmp and cc > CC:
#             #                 CC += 1
#             #                 tmp.show(tmp.max_len + now)
#             #                 now += tmp.max_len
#             #             cc += 1
#             #         else:
#             #             break
#             #     cu.key_show(cu.r_guest)
#             cu.key_show(cu.r_guest)

#             return True

#     def l(path, cu):
        
#         cu.cl()
#         cu = cu.last
#         tmp = cu
#         co = 1
#         while 1:
#             if tmp:
#                 # L(tmp.root,tmp.r_guest, r=LogControl.got_size()[0],c=1,color='yellow',end='')
#                 tmp.show(tmp.r_guest)
#                 tmp = tmp.last
#             else:
#                 break
#             co += 1
#         if cu.r_guest < LogControl.got_size()[1]:
#             cu.key_show(cu.r_guest)
#         # cu.key_show(10)
#         return True

#     cu.set_key_listener('l', r)
#     cu.set_key_listener('h', l)
#     cu.set_key_listener('j', j)
#     cu.set_key_listener('k', j)
#     cu.key_show(1)
#     LogControl.load()

# # def range2(ls=os.path.listdir, cd=os.path.join):
#     # p = Pane()
#     # root = "."
#     # cu = ls(root)
#     # p.add_c(cu)

#     # pa = None
#     # sub = ls(p.cur)
#     # p.add_c(sub)

#     # def r():
#         # pass












# def test():
#     ls = os.listdir
#     p = Pane()
#     p.add_c(Column(*ls("..")))
#     p.add_c(Column(*ls(".")))
    
#     p.on_keyboard()


    
    



