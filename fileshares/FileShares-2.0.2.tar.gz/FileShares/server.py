import pickle
import os
from termcolor import cprint, colored
from time import sleep
from socketserver import ThreadingTCPServer, BaseRequestHandler
from struct import unpack, pack
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from collections import Iterable
from functools import partial
from concurrent.futures import ThreadPoolExecutor

from .base import Dir, IO,Encry, FileNotFoundErr
from .config import loger, ENV, PATH_DEL

def send_msg(fp, cmd, data, key=b'what#@!$THeFuck!@$You'):
    if not isinstance(data, bytes):
        data = pickle.dumps(data)
    l = len(data)
    loger.debug(colored("l: %d" % l,'yellow'))
    fp.send(cmd + pack('>I', l))
    for i in Encry.stream(data, key):
        fp.send(bytes([i]))

    


def read_msg(fp, key=b'what#@!$THeFuck!@$You'):
    cmd = fp.recv(1)
    rl, = unpack(">I", fp.recv(4))
    data = fp.recv(rl)
    l = len(data)
    while l < rl:
    
        per = float(l / rl) *100
        print(colored("read continue: %%%.3f" % per ,'magenta'),end='\r')
        data += fp.recv(rl-l)
        l = len(data)
    print(colored('read ok ','green'),end='\r')
    data = bytes(Encry.stream(data, key))
    return cmd, l, data



class ServerHandler(BaseRequestHandler):
    io = None
    root = os.path.abspath(os.path.curdir)
    key=b'what#@!$THeFuck!@$You'
    tmp_downloads = set()
    tmp_hash = set()

    def handle(self):
        cmd, l, data = read_msg(self.request)
        loger.debug(b"cmd : " + cmd)
        if cmd == b'f':
            self.save_file(data)
        elif cmd == b'm':
            self.mkdir(data)
        elif cmd == b'l':
            # loger.debug(data[:5])
            if data[:5] == b'check':
                self.list()
                loger.debug(colored("sync check", "yellow"))
                return
            else:
                ha_s = [f for f in pickle.loads(data)]
                files = [ff for ff in [self.ready_file(f) for f in ha_s] if ff]
                
                send_msg(self.request, b'z', files)

                for h in ha_s:
                    if h in ServerHandler.tmp_hash:
                        ServerHandler.tmp_hash.remove(h)
                loger.debug(colored("sync : finished", "red"))

                return

        send_msg(self.request, b'z', b'ok')


#############################################
#### function area ##########################
#############################################

    @staticmethod
    def SRun(ip='', port=20000, key=b'what#@!$THeFuck!@$You', root=None):
        ServerHandler.io = IO()
        ServerHandler.key = key
        if root:
            ServerHandler.root = root

        serv = ThreadingTCPServer(('', 20000), ServerHandler)
        serv.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serv.serve_forever()

    def mkdir(self, data):
        dirs = pickle.loads(data)
        for d in dirs:
            try:
                os.makedirs(d)
            except FileExistsError:
                pass

    def save_file(self, data):
        head_l, = unpack(">I", data[:4])
        head = pickle.loads(data[4:4 + head_l])

        if  PATH_DEL not in head.path:
            if ENV[0][:3] == "win":
                head.path = head.path.replace("/","\\")
            else:
                head.path = head.path.replace("\\","/")

            if head.path.startswith("."+PATH_DEL):
                head.path = head.path[2:]

        dirs_path = os.path.dirname(head.path)

        if not os.path.exists(dirs_path):
            try:
                os.makedirs(dirs_path)
            except FileExistsError:
                pass
            except FileNotFoundError:
                pass

        loger.debug("save file : " + head.path)
        try:
            with open(os.path.join(ServerHandler.root, head.path), 'wb') as fp:
                fp.write(data[4 + head_l:])
        except PermissionError:
            loger.warning(colored("write file[%s] no permission!" % head.path))

    def ready_file(self, file_hash):
        loger.debug(colored("Search: "+ file_hash, 'red'))
        file = ServerHandler.io[file_hash]
        if os.path.exists(file):
            if os.path.basename(file).startswith("."):
                return None

            if os.path.isfile(file):
                data = b''
                with open(file, 'rb') as fp:
                    data = fp.read()

                file_path = os.path.abspath(file)
                path = file_path.replace(ServerHandler.root, '.')
                loger.debug("send file's path: %s | root: %s" % (path, ServerHandler.root))
                header = pickle.dumps(Header(os.path.basename(path), path))
                header_l = pack(">I", len(header))
                # return header_l + header + data
                return header_l + header + data
                # return True

        else:
            raise FileExistsError("no such file")

    def list(self):
        try:
            d = Dir(ServerHandler.root, ServerHandler.io) 
        except OSError as e:
            cprint(ServerHandler.io.items, "red")
            raise e
        hash_list = set(d.all())
        c_l = []
        for h in hash_list:
            if h in ServerHandler.tmp_hash:
                c_l.append(h)
            else:
                ServerHandler.tmp_hash.add(h)
        for h in c_l:
            hash_list.remove(h)
        send_msg(self.request, b'z', hash_list)


class Header:

    def __init__(self, name, path):
        self.name = name
        self.path = path


class Client:
    server_info = ('127.0.0.1', 20000)
    root = os.path.abspath(os.path.curdir)
    io = IO()
    key=b'what#@!$THeFuck!@$You'

    def __init__(self, root=None, ip=None, port=None, key=None):
        if ip and port:
            Client.server_info = (ip, port)

        if root:
            if os.path.exists(root):
                Client.root = os.path.abspath(root)

        if key:
            if isinstance(key, bytes):
                Client.key = key
            elif isinstance(key, str):
                Client.key = key.encode('utf8','ignore')

    def send_file(self, file):

        if os.path.exists(file):

            if os.path.isfile(file):
                data = b''
                with open(file, 'rb') as fp:
                    data = fp.read()

                file_path = os.path.abspath(file)
                path = file_path.replace(Client.root, '.')
                header = pickle.dumps(Header(os.path.basename(path), path))
                header_l = pack(">I", len(header))
                loger.info("ready: " + file)
                c,l,r = self.cmd(b'f', header_l + header + data)
                return file,r

        else:
            raise FileExistsError("no such file")

    def save_file(self, data):
        head_l, = unpack(">I", data[:4])
        head = pickle.loads(data[4:4 + head_l])
        if  PATH_DEL not in head.path:
            if ENV[0][:3] == "win":
                head.path = head.path.replace("/","\\")
            else:
                head.path = head.path.replace("\\","/")


        dirs_path = os.path.dirname(head.path)
        loger.debug("   file : " + dirs_path)
        if not os.path.exists(dirs_path):
            try:
                os.makedirs(dirs_path)
            except FileNotFoundError as e:
                loger.warning(colored("failed mkdir : %s" %  dirs_path,'red'))


                # return False
        e = os.path.join(Client.root, head.path)
        cprint("abs : %s" % os.path.abspath(e),"blue")
        with open(e, 'wb') as fp:
            fp.write(data[4 + head_l:])
        cprint("Save done: %s" %  e ,'red')

    def check(self):
        c, rl, res = self.cmd(b'l', b'check')
        
        hash_set = pickle.loads(res)
        hash_set_local = set(Dir(Client.root, Client.io).all())

        need_download_hash = hash_set - hash_set_local
        loger.debug("D : "+colored(need_download_hash, "green"))
        c, rl, res = self.cmd(b'l', need_download_hash)
        # loger.debug("need got: %d , got: %d" %(rl, len(res)))
        files = pickle.loads(res)
        c = 0
        loger.debug("ready to save %d " % len(files))
        # loger.debug(files)
        for f in files:
            self.save_file(f)
            c += 1
            

    def cmd(self, cmd, data):
        key = Client.key
        D = cmd
        
        if isinstance(data, bytes):
            l = len(data)
            D += pack('>I', l)
            loger.debug("encrypting data")
            data = bytes(Encry.stream(data, key))
            D += data
        else:
            data = pickle.dumps(data)
            loger.debug("encrypting data")
            data = bytes(Encry.stream(data, key))
            l = len(data)
            D += pack('>I', l)
            D += data
        
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(Client.server_info)

            sl = s.send(D)
            cmd = s.recv(1)
            rl, = unpack('>I', s.recv(4))
            res = s.recv(rl)
            l = len(res)
            while l < rl:
                per = float(l / rl) * 100
                print(colored("read continue: %%%.3f" % per ,'magenta'),end='\r')
                res += s.recv(rl-l)
                l = len(res)
            print(colored('read ok ','green'),end='\r')
            res = bytes(Encry.stream(res, key))
            return cmd, rl, res
        except OSError as e:
            loger.error(e)
            loger.error(Client.server_info)
        finally:
            s.close()



class Monitor:

    def __init__(self, root, inter = 3, workers=6, key=None,ip=None, port=None):
        if not os.path.isdir(root):
            raise FileNotFoundErr("no such dir found :" + root)

        self.root = root
        self.io = IO()
        self.exe = ThreadPoolExecutor(workers)
        self.client = Client(root=root,ip=ip,port=port, key=key)
        self.tmp_upload = set()
        self.inter = inter

    def done(self, future):
        url,res = future.result()
        loger.debug(colored("[ok] "+ url +" "+ res.decode(),'magenta'))
        if url in self.tmp_upload:
            self.tmp_upload.remove(url)
        self.old_d = set(Dir(self.root, self.io).all())

    def check_uploads(self, old_d):

        # loger.debug("tmp upload {}".format(self.tmp_upload))
        d = set(Dir(self.root, self.io).all())
        # loger.debug(d)
        # loger.debug(old_d)
        new_s =  d - old_d
        loger.debug("N : " + colored(new_s,"blue"))
        loger.debug(colored("upload : %d " % len(new_s), "green"))
        for f in new_s:
            file = self.io[f]
            if os.path.exists(file) and file not in self.tmp_upload:
                self.tmp_upload.add(file)
                fm  = self.exe.submit(self.client.send_file, file)
                fm.add_done_callback(self.done)
                
            
    def run(self):
        self.old_d = set()
        while 1:
            try:
                
                self.check_uploads(self.old_d)
                self.client.check()
                    
            except TypeError as e:
                loger.error(e)
            sleep(self.inter)

