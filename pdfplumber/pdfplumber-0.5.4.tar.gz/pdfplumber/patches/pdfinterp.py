from pdfminer.pdfinterp import (
    PDFGraphicState,
    PDFPageInterpreter,
    PDFInterpreterError,
)

from pdfminer.pdfcolor import (
    LITERAL_DEVICE_GRAY,
    LITERAL_DEVICE_RGB,
    LITERAL_DEVICE_CMYK,
)

import spectra
def pdfcolor_to_hex(c):
    if c is None: return None
    if isinstance(c, (tuple, list)):
        if len(c) == 1:
            s = spectra.rgb(c[0], c[0], c[0])
        elif len(c) == 3:
            s = spectra.rgb(*c)
        else:
            s = spectra.cmyk(*c)
    else:
        s = spectra.rgb(c, c, c)
    return s.hexcode

# PDFGraphicState
def __init__(self):
    self.linewidth = 0
    self.linecap = None
    self.linejoin = None
    self.miterlimit = None
    self.dash = None
    self.intent = None
    self.flatness = None

    # stroking color
    self.scolor = None

    # non stroking color
    self.ncolor = None
    return

def copy(self):
    obj = PDFGraphicState()
    obj.linewidth = self.linewidth
    obj.linecap = self.linecap
    obj.linejoin = self.linejoin
    obj.miterlimit = self.miterlimit
    obj.dash = self.dash
    obj.intent = self.intent
    obj.flatness = self.flatness
    obj.scolor = self.scolor
    obj.ncolor = self.ncolor
    return obj

@property
def scolor_hex(self):
    return pdfcolor_to_hex(self.scolor)

@property
def ncolor_hex(self):
    return pdfcolor_to_hex(self.ncolor)
    
PDFGraphicState.__init__ = __init__
PDFGraphicState.copy = copy
PDFGraphicState.scolor_hex = scolor_hex
PDFGraphicState.ncolor_hex = ncolor_hex

# PDFPageInterpreter
def do_G(self, gray):
    self.graphicstate.scolor = gray
    self.do_CS(LITERAL_DEVICE_GRAY)
    return

# setgray-non-stroking
def do_g(self, gray):
    self.graphicstate.ncolor = gray
    self.do_cs(LITERAL_DEVICE_GRAY)
    return

# setrgb-stroking
def do_RG(self, r, g, b):
    self.graphicstate.scolor = (r, g, b)
    self.do_CS(LITERAL_DEVICE_RGB)
    return

# setrgb-non-stroking
def do_rg(self, r, g, b):
    self.graphicstate.ncolor = (r, g, b)
    self.do_cs(LITERAL_DEVICE_RGB)
    return

# setcmyk-stroking
def do_K(self, c, m, y, k):
    self.graphicstate.scolor = (c, m, y, k)
    self.do_CS(LITERAL_DEVICE_CMYK)
    return

# setcmyk-non-stroking
def do_k(self, c, m, y, k):
    self.graphicstate.ncolor = (c, m, y, k)
    self.do_cs(LITERAL_DEVICE_CMYK)
    return

# setcolor
def do_SCN(self):
    if self.scs:
        n = self.scs.ncomponents
    else:
        if settings.STRICT:
            raise PDFInterpreterError('No colorspace specified!')
        n = 1
    self.graphicstate.scolor = self.pop(n)
    return

def do_scn(self):
    if self.ncs:
        n = self.ncs.ncomponents
    else:
        if settings.STRICT:
            raise PDFInterpreterError('No colorspace specified!')
        n = 1
    self.graphicstate.ncolor = self.pop(n)
    return

def __init__(self, rsrcmgr, device):
    self.rsrcmgr = rsrcmgr
    self.device = device
    self.device.interpreter = self

PDFPageInterpreter.__init__ = __init__
PDFPageInterpreter.do_G = do_G
PDFPageInterpreter.do_g = do_g
PDFPageInterpreter.do_RG = do_RG
PDFPageInterpreter.do_rg = do_rg
PDFPageInterpreter.do_K = do_K
PDFPageInterpreter.do_k = do_k
PDFPageInterpreter.do_SCN = do_SCN
PDFPageInterpreter.do_scn = do_scn
