"""P22P v0.4 client GUI"""
import Tkinter

from twisted.internet import reactor, tksupport, defer, endpoints, task
import tkMessageBox

import p22p
import p22p.common
import p22p.client


DEFAULT_SERVER = "localhost:" + str(p22p.common.DEFAULT_PORT)


class AbortError(Exception):
    """An Exception raised when something is aborted"""
    pass


class P22PGui(object):
    """The GUI for the P22P client"""
    def __init__(self):
        self.protocol = None
        self.pingloop = None
        
        self.screen = Tkinter.Tk()
        tksupport.install(self.screen)
        self.screen.title("P22P Client")
        self.screen.protocol("WM_DELETE_WINDOW", self.on_close)

        self.show_connect_window()

    def on_close(self):
        """called when the window should be closed"""
        if tkMessageBox.askokcancel(title="Quit?", message="Are you sure you want to quit? All Connections will be closed."):
            self.quit()

    def show_connect_window(self):
        """shows the window asking for the server information"""
        d = defer.Deferred()
        d.addCallback(self.connected)
        d.addErrback(self.handle_acw_error)
        acw = AskConnectWindow(self, d)

    def handle_acw_error(self, f):
        """handles an error in the AskConnectWindow"""
        f.trap(AbortError)
        self.quit()

    def connected(self, protocol):
        self.protocol = protocol
        self.build_window()
        self.start_pinging()

    def build_window(self):
        """builds the window"""
        pass

    def start_pinging(self):
        """starts the regular pinging"""
        self.pingloop = task.LoopingCall(self.do_pings)
        self.pingloop.start(3)

    def do_pings(self):
        """pings the server and the clients"""
        if self.protocol is None:
            return
        self.protocol.ping_server().addCallback(self.got_server_ping)

    def got_server_ping(self, t):
        """Called when the server answered the ping"""
        self.screen.title("P22P Client | Ping: {p} ms".format(p=t*1000))

    def run(self):
        """starts the GUI"""
        reactor.run()

    def quit(self):
        """quits the GUI"""
        if self.protocol is not None:
            self.protocol.disconnect()
            self.protocol = None
        self.screen.quit()
        self.screen.destroy()
        reactor.callLater(0.5, reactor.stop)


class AskConnectWindow(object):
    """A window for connecting to a server"""
    def __init__(self, root, d):
        self.root = root
        self.d = d
        self.setup_window()

    def setup_window(self):
        """creates the window"""
        self.screen = Tkinter.Toplevel(master=self.root.screen)
        self.screen.title("Connect to Server")
        self.screen.protocol("WM_DELETE_WINDOW", self.on_close)
        self.label = Tkinter.Label(master=self.screen, text="Enter the Address of the server:")
        self.entry = Tkinter.Entry(master=self.screen)
        self.button = Tkinter.Button(master=self.screen, text="Connect", command=self.connect)
        self.label.grid(row=0, column=0, columnspan=3)
        self.entry.grid(row=1, column=0, columnspan=2)
        self.entry.delete(0, Tkinter.END)
        self.entry.insert(0, DEFAULT_SERVER)
        self.button.grid(row=1, column=2, columnspan=1)

    def connect(self, e=None):
        """creates the endpoint, closes the window and connects to the server"""
        inp = self.entry.get()
        if len(inp) == 0:
            inp = DEFAULT_SERVER
        ip, port = None, None
        if inp.count(":") == 0:
            # only IP
            ip = inp
            port = p22p.common.DEFAULT_PORT
        elif inp.count(":") == 1:
            # IP:port
            ip, port = inp.split(":")
            try:
                port = int(port)
            except ValueError:
                tkMessageBox.showerror(title="Invalid Input", message="Port must be an integer!")
                return
        if ip is None:
            epstr = inp
        else:
            epstr = "tcp:host={i}:port={p}:timeout=15".format(i=ip, p=port)
        ep = endpoints.clientFromString(reactor, epstr)
        d = endpoints.connectProtocol(ep, p22p.client.P22PClientProtocol())
        d.addCallback(self.connected)
        d.addErrback(self.connect_failed)

    def connected(self, p):
        """called when the connection was successfull"""
        self.quit()
        self.d.callback(p)

    def connect_failed(self, f):
        """called when the connection attempt failed"""
        tkMessageBox.showerror(title="Connection failed", message="Could not connect to server. Reason:\n{e}".format(e=f))

    def on_close(self):
        """called when the window is closed."""
        self.quit()
        self.d.errback(AbortError("Window closed"))

    def quit(self):
        """closes the window"""
        self.screen.destroy()


def main():
    """create and run a GUI"""
    gui = P22PGui()
    gui.run()

    
if __name__ == "__main__":
    main()
