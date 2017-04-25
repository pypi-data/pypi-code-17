# mad/xmpp.py
#
#

""" XMPP bot class. """

from .bot import Bot
from .event import Event
from .utils import stripped

import logging
import time
import os

def init(event):
    bot = XMPP()
    bot.start()
    return bot

class XMPP(Bot):

    cc = ""

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def connect(self, user="", pw=""):
        fn = os.path.expanduser("~/.sleekpass")
        pww = ""
        try:
            f = open(fn, "r")
            pww = f.read()
            f.close()
        except:
            logging.error("missing sleekpass file, create one with password in ~/.sleekpass")
            return
        self._connect(user or self.cfg.user, pw or pww)

    def connected(self, data):
        self._connected.ready()

    def disconnected(self, data):
        self._connected.clear()
        pass

    def event(self):
        e = self._queue.get()
        if e:
            e.btype = self.type
        return e

    def exception(self, data):
        self._error = data

    def failedauth(self, data):
        logging.error("# failed auth %s" % data)

    def failure(self, data):
        logging.error("# failure %s" % data)
        self._error = data

    def invalid_cert(self, data):
        logging.debug("# invalid cert")

    def iqed(self, data):
        logging.warn("# Iq %s:%s %s" % (self.cfg.server, self.cfg.port, data))

    def messaged(self, data):
        from .space import kernel
        logging.debug("< %s" % data)
        m = Event()
        m.update(data)
        if m.type == "error":
            logging.error("^ %s" % m.error)
            return
        m.cc = ""
        m["from"] = str(m["from"])
        if self.cfg.user in m["from"]:
            logging.debug("! ignore %s %s" % (m.type, m["from"]))
            return
        m.origin = m["from"]
        m.btype = self.type
        m.server = self.cfg.server
        m.channel = m.origin
        m.to = m.origin
        m.element = "message"
        m.txt = m["body"]
        if '<delay xmlns="urn:xmpp:delay"' in str(data):
            logging.debug("! ignore %s" % m.origin)
            return
        logging.info("< %s %s" % (stripped(m.origin), m.txt))
        kernel.put(m)

    def pinged(self, event):
        self._connected.ready()

    def presenced(self, data):
        from .space import kernel
        logging.debug("< %s" % data)
        o = Event()
        o.cc = ""
        o.update(data)
        o.id = self.id()
        o.origin = o["from"]
        if "txt" not in o:
            o.txt = ""
        o.element = "presence"
        username = o.origin
        if o.type == 'subscribe':
            pres = Event({'to': o["from"], 'type': 'subscribed'})
            self.client.send_presence(dict(pres))
            pres = Event({'to': o["from"], 'type': 'subscribe'})
            self.client.send_presence(dict(pres))
        elif o.type == "unavailable" and username != self.cfg.username and username in self.channels:
            self.channels.remove(username)
        elif o.origin != self.cfg.user and username != self.cfg.username and username not in self.channels:
            self.channels.append(username)
        o.txt = o.type
        logging.info("< presence %s" % stripped(o.origin))
        kernel.put(o)

    def register(self, key, value):
        self.client.add_event_handler(key, value)

    def resume(self): pass

    def say(self, jid, txt):
        txt = str(txt)
        self.client.send_message(jid, txt)
        logging.info("%s %s" % (stripped(jid), txt))

    def session_start(self, data):
        self.client.send_presence()

    def start(self, *args, **kwargs):
        self.launch(self.sleek)
        self.connect()
        super().start(*args, **kwargs)

    def stop(self):
        self._queue.put(None)
        self.client.disconnect()
        super().stop()

    def sleek(self):
        self._connected.wait()
        self.client.process(block=True)

    def _connect(self, user, pw):
        self.makeclient(user, pw)
        self.client.reconnect_max_attempts = 2
        logging.warn("# connect %s" % self.cfg.user)
        if self.cfg.openfire:
            self.client.connect((self.cfg.server, self.cfg.port), use_ssl=True)
        else:
            self.client.connect((self.cfg.server, self.cfg.port))
        if self.cfg.noresolver:
            self.client.configure_dns(None)
        self.register_fd(self.client.socket)

    def makeclient(self, jid, password):
        try:
            import sleekxmpp.clientxmpp
            import sleekxmpp
        except ImportError:
            logging.warn("sleekxmpp is not installed")
        self.client = sleekxmpp.clientxmpp.ClientXMPP(jid, password)
        self.register("session_start", self.session_start)
        self.register("message", self.messaged)
        self.register("iq", self.iqed)
        self.register("ssl_invalid_cert", self.invalid_cert)
        self.register('disconnected', self.disconnected)
        self.register('connected', self.connected)
        self.register('presence_available', self.presenced)
        self.register('presence_dnd', self.presenced)
        self.register('presence_xa', self.presenced)
        self.register('presence_chat', self.presenced)
        self.register('presence_away', self.presenced)
        self.register('presence_unavailable', self.presenced)
        self.register('presence_subscribe', self.presenced)
        self.register('presence_subscribed', self.presenced)
        self.register('presence_unsubscribe', self.presenced)
        self.register('presence_unsubscribed', self.presenced)
        self.register('groupchat_message', self.messaged)
        self.register('groupchat_presence', self.presenced)
        self.register('groupchat_subject', self.presenced)
        self.register('failed_auth', self.failedauth)
        self.client.exception = self.exception
        self.client.use_signals()
