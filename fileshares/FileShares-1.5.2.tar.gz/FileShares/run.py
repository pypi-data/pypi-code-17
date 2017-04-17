import argparse, os, sys
from termcolor import cprint
from cmd import Cmd
from functools import partial
from .server import ServerHandler, Monitor
from .config import loger, setloglevel
from .daemon import run, stop



class CLI(Cmd):

    def __init__(self):
        super().__init__()
        print(colored("""you need to conifg  \nip\nroot \nport(default 20000) \npasswd(deafult what#@!$THeFuck!@$You) ""","green"))
        self.prompt = colored("~", "red")
        self.port = 20000
        self.passwd = 'what#@!$THeFuck!@$You'
        self.root = os.path.abspath(os.path.curdir)

    def do_server(self, args):
        ServerHandler.SRun(ip=self.ip, port=self.port, key=self.passwd, root=self.root)

    def do_client(self, args):
        m = Monitor(self.root)
        m.run()

    def do_config(self, args):
        try:
            k,v = args.split()
            if k == 'port':
                v = int(v)
            setattr(self, k, v)
        except Exception as e:
            print(colored(e,"red"))


def cmds():
    DOC = """
        stream encrypt fileshares
    """
    parser = argparse.ArgumentParser(usage="how to use this", description=DOC)
    parser.add_argument("-r", "--root", default=None, help="set root")
    parser.add_argument("-s", "--server-mode", default=False, action="store_true", help="set server mode, default client mode")
    parser.add_argument("-k", "--key", default='what#@!$THeFuck!@$You', help="set key")
    parser.add_argument("--start", default=False, action="store_true", help="start server")
    parser.add_argument("--stop", default=False, action="store_true", help="rp shell mode")
    parser.add_argument("--shell", default=False,action="store_true", help="set root")
    parser.add_argument("-i", "--ip", default="0.0.0.0", help="set ip")
    parser.add_argument("-p", "--port", default=20000, type=int, help="set port")
    parser.add_argument("-v", "--verbose", default=1, type=int, help="set verbose")


    return parser.parse_args()

def main():
    args = cmds()
    setloglevel(args.verbose)
    if args.shell:
        c = CLI()
        c.cmdloop()
        sys.exit(0)

    root = os.path.abspath(os.path.curdir)
    key = args.key.encode()
    if args.root:
        if os.path.exists(args.root):
            root = os.path.abspath(args.root)

    run_func = None
    r_str = None
    if args.server_mode:
        r_str = "server_share"
        run_func = partial(ServerHandler.SRun,ip=args.ip, port=args.port, root=root, key=key)
        # run_func()
    else:
        r_str = "client_share"
        print("client mode")
        m = Monitor(root, ip=args.ip, port=args.port, key=key)
        run_func = partial(m.run)
        # m.run()

       
    if args.start:
        run(run_func, r_str)
        sys.exit(0)
    elif args.stop:
        stop(run_func, r_str)
        sys.exit(0)
    loger.debug("run...")
    cprint("root = {}".format(root),"red")
    cprint("ip:port = {}:{}".format(args.ip ,args.port),"red")
    cprint("key = {}".format(key),"red")
    run_func()

