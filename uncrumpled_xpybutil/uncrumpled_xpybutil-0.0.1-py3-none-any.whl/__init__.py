#import xcb, xcb.xproto
import xcffib
import xcffib.xproto as xproto
try:
    conn = xcffib.connect()
    root = conn.get_setup().roots[0].root
except xcffib.ConnectException:
    conn = None
    root = None

