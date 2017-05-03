# This file was created automatically by SWIG 1.3.29.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _pylibmpsse
import new
new_instancemethod = new.instancemethod
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'PySwigObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


MPSSE_OK = _pylibmpsse.MPSSE_OK
MPSSE_FAIL = _pylibmpsse.MPSSE_FAIL
MSB = _pylibmpsse.MSB
LSB = _pylibmpsse.LSB
CHUNK_SIZE = _pylibmpsse.CHUNK_SIZE
SPI_RW_SIZE = _pylibmpsse.SPI_RW_SIZE
SPI_TRANSFER_SIZE = _pylibmpsse.SPI_TRANSFER_SIZE
I2C_TRANSFER_SIZE = _pylibmpsse.I2C_TRANSFER_SIZE
LATENCY_MS = _pylibmpsse.LATENCY_MS
TIMEOUT_DIVISOR = _pylibmpsse.TIMEOUT_DIVISOR
USB_TIMEOUT = _pylibmpsse.USB_TIMEOUT
SETUP_DELAY = _pylibmpsse.SETUP_DELAY
BITMODE_RESET = _pylibmpsse.BITMODE_RESET
BITMODE_MPSSE = _pylibmpsse.BITMODE_MPSSE
CMD_SIZE = _pylibmpsse.CMD_SIZE
MAX_SETUP_COMMANDS = _pylibmpsse.MAX_SETUP_COMMANDS
SS_TX_COUNT = _pylibmpsse.SS_TX_COUNT
LOW = _pylibmpsse.LOW
HIGH = _pylibmpsse.HIGH
NUM_GPIOL_PINS = _pylibmpsse.NUM_GPIOL_PINS
NUM_GPIO_PINS = _pylibmpsse.NUM_GPIO_PINS
NULL_CONTEXT_ERROR_MSG = _pylibmpsse.NULL_CONTEXT_ERROR_MSG
IFACE_ANY = _pylibmpsse.IFACE_ANY
IFACE_A = _pylibmpsse.IFACE_A
IFACE_B = _pylibmpsse.IFACE_B
IFACE_C = _pylibmpsse.IFACE_C
IFACE_D = _pylibmpsse.IFACE_D
ONE_HUNDRED_KHZ = _pylibmpsse.ONE_HUNDRED_KHZ
FOUR_HUNDRED_KHZ = _pylibmpsse.FOUR_HUNDRED_KHZ
ONE_MHZ = _pylibmpsse.ONE_MHZ
TWO_MHZ = _pylibmpsse.TWO_MHZ
FIVE_MHZ = _pylibmpsse.FIVE_MHZ
SIX_MHZ = _pylibmpsse.SIX_MHZ
TEN_MHZ = _pylibmpsse.TEN_MHZ
TWELVE_MHZ = _pylibmpsse.TWELVE_MHZ
FIFTEEN_MHZ = _pylibmpsse.FIFTEEN_MHZ
THIRTY_MHZ = _pylibmpsse.THIRTY_MHZ
SIXTY_MHZ = _pylibmpsse.SIXTY_MHZ
SPI0 = _pylibmpsse.SPI0
SPI1 = _pylibmpsse.SPI1
SPI2 = _pylibmpsse.SPI2
SPI3 = _pylibmpsse.SPI3
I2C = _pylibmpsse.I2C
GPIO = _pylibmpsse.GPIO
BITBANG = _pylibmpsse.BITBANG
SK = _pylibmpsse.SK
DO = _pylibmpsse.DO
DI = _pylibmpsse.DI
CS = _pylibmpsse.CS
GPIO0 = _pylibmpsse.GPIO0
GPIO1 = _pylibmpsse.GPIO1
GPIO2 = _pylibmpsse.GPIO2
GPIO3 = _pylibmpsse.GPIO3
GPIOL0 = _pylibmpsse.GPIOL0
GPIOL1 = _pylibmpsse.GPIOL1
GPIOL2 = _pylibmpsse.GPIOL2
GPIOL3 = _pylibmpsse.GPIOL3
GPIOH0 = _pylibmpsse.GPIOH0
GPIOH1 = _pylibmpsse.GPIOH1
GPIOH2 = _pylibmpsse.GPIOH2
GPIOH3 = _pylibmpsse.GPIOH3
GPIOH4 = _pylibmpsse.GPIOH4
GPIOH5 = _pylibmpsse.GPIOH5
GPIOH6 = _pylibmpsse.GPIOH6
GPIOH7 = _pylibmpsse.GPIOH7
ACK = _pylibmpsse.ACK
NACK = _pylibmpsse.NACK
INVALID_COMMAND = _pylibmpsse.INVALID_COMMAND
ENABLE_ADAPTIVE_CLOCK = _pylibmpsse.ENABLE_ADAPTIVE_CLOCK
DISABLE_ADAPTIVE_CLOCK = _pylibmpsse.DISABLE_ADAPTIVE_CLOCK
ENABLE_3_PHASE_CLOCK = _pylibmpsse.ENABLE_3_PHASE_CLOCK
DISABLE_3_PHASE_CLOCK = _pylibmpsse.DISABLE_3_PHASE_CLOCK
TCK_X5 = _pylibmpsse.TCK_X5
TCK_D5 = _pylibmpsse.TCK_D5
CLOCK_N_CYCLES = _pylibmpsse.CLOCK_N_CYCLES
CLOCK_N8_CYCLES = _pylibmpsse.CLOCK_N8_CYCLES
PULSE_CLOCK_IO_HIGH = _pylibmpsse.PULSE_CLOCK_IO_HIGH
PULSE_CLOCK_IO_LOW = _pylibmpsse.PULSE_CLOCK_IO_LOW
CLOCK_N8_CYCLES_IO_HIGH = _pylibmpsse.CLOCK_N8_CYCLES_IO_HIGH
CLOCK_N8_CYCLES_IO_LOW = _pylibmpsse.CLOCK_N8_CYCLES_IO_LOW
TRISTATE_IO = _pylibmpsse.TRISTATE_IO
STARTED = _pylibmpsse.STARTED
STOPPED = _pylibmpsse.STOPPED
class vid_pid(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vid_pid, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vid_pid, name)
    __repr__ = _swig_repr
    __swig_setmethods__["vid"] = _pylibmpsse.vid_pid_vid_set
    __swig_getmethods__["vid"] = _pylibmpsse.vid_pid_vid_get
    if _newclass:vid = property(_pylibmpsse.vid_pid_vid_get, _pylibmpsse.vid_pid_vid_set)
    __swig_setmethods__["pid"] = _pylibmpsse.vid_pid_pid_set
    __swig_getmethods__["pid"] = _pylibmpsse.vid_pid_pid_get
    if _newclass:pid = property(_pylibmpsse.vid_pid_pid_get, _pylibmpsse.vid_pid_pid_set)
    __swig_setmethods__["description"] = _pylibmpsse.vid_pid_description_set
    __swig_getmethods__["description"] = _pylibmpsse.vid_pid_description_get
    if _newclass:description = property(_pylibmpsse.vid_pid_description_get, _pylibmpsse.vid_pid_description_set)
    def __init__(self, *args): 
        this = _pylibmpsse.new_vid_pid(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _pylibmpsse.delete_vid_pid
    __del__ = lambda self : None;
vid_pid_swigregister = _pylibmpsse.vid_pid_swigregister
vid_pid_swigregister(vid_pid)

class mpsse_context(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, mpsse_context, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, mpsse_context, name)
    __repr__ = _swig_repr
    __swig_setmethods__["description"] = _pylibmpsse.mpsse_context_description_set
    __swig_getmethods__["description"] = _pylibmpsse.mpsse_context_description_get
    if _newclass:description = property(_pylibmpsse.mpsse_context_description_get, _pylibmpsse.mpsse_context_description_set)
    __swig_setmethods__["ftdi"] = _pylibmpsse.mpsse_context_ftdi_set
    __swig_getmethods__["ftdi"] = _pylibmpsse.mpsse_context_ftdi_get
    if _newclass:ftdi = property(_pylibmpsse.mpsse_context_ftdi_get, _pylibmpsse.mpsse_context_ftdi_set)
    __swig_setmethods__["mode"] = _pylibmpsse.mpsse_context_mode_set
    __swig_getmethods__["mode"] = _pylibmpsse.mpsse_context_mode_get
    if _newclass:mode = property(_pylibmpsse.mpsse_context_mode_get, _pylibmpsse.mpsse_context_mode_set)
    __swig_setmethods__["status"] = _pylibmpsse.mpsse_context_status_set
    __swig_getmethods__["status"] = _pylibmpsse.mpsse_context_status_get
    if _newclass:status = property(_pylibmpsse.mpsse_context_status_get, _pylibmpsse.mpsse_context_status_set)
    __swig_setmethods__["flush_after_read"] = _pylibmpsse.mpsse_context_flush_after_read_set
    __swig_getmethods__["flush_after_read"] = _pylibmpsse.mpsse_context_flush_after_read_get
    if _newclass:flush_after_read = property(_pylibmpsse.mpsse_context_flush_after_read_get, _pylibmpsse.mpsse_context_flush_after_read_set)
    __swig_setmethods__["vid"] = _pylibmpsse.mpsse_context_vid_set
    __swig_getmethods__["vid"] = _pylibmpsse.mpsse_context_vid_get
    if _newclass:vid = property(_pylibmpsse.mpsse_context_vid_get, _pylibmpsse.mpsse_context_vid_set)
    __swig_setmethods__["pid"] = _pylibmpsse.mpsse_context_pid_set
    __swig_getmethods__["pid"] = _pylibmpsse.mpsse_context_pid_get
    if _newclass:pid = property(_pylibmpsse.mpsse_context_pid_get, _pylibmpsse.mpsse_context_pid_set)
    __swig_setmethods__["clock"] = _pylibmpsse.mpsse_context_clock_set
    __swig_getmethods__["clock"] = _pylibmpsse.mpsse_context_clock_get
    if _newclass:clock = property(_pylibmpsse.mpsse_context_clock_get, _pylibmpsse.mpsse_context_clock_set)
    __swig_setmethods__["xsize"] = _pylibmpsse.mpsse_context_xsize_set
    __swig_getmethods__["xsize"] = _pylibmpsse.mpsse_context_xsize_get
    if _newclass:xsize = property(_pylibmpsse.mpsse_context_xsize_get, _pylibmpsse.mpsse_context_xsize_set)
    __swig_setmethods__["open"] = _pylibmpsse.mpsse_context_open_set
    __swig_getmethods__["open"] = _pylibmpsse.mpsse_context_open_get
    if _newclass:open = property(_pylibmpsse.mpsse_context_open_get, _pylibmpsse.mpsse_context_open_set)
    __swig_setmethods__["endianess"] = _pylibmpsse.mpsse_context_endianess_set
    __swig_getmethods__["endianess"] = _pylibmpsse.mpsse_context_endianess_get
    if _newclass:endianess = property(_pylibmpsse.mpsse_context_endianess_get, _pylibmpsse.mpsse_context_endianess_set)
    __swig_setmethods__["tris"] = _pylibmpsse.mpsse_context_tris_set
    __swig_getmethods__["tris"] = _pylibmpsse.mpsse_context_tris_get
    if _newclass:tris = property(_pylibmpsse.mpsse_context_tris_get, _pylibmpsse.mpsse_context_tris_set)
    __swig_setmethods__["pstart"] = _pylibmpsse.mpsse_context_pstart_set
    __swig_getmethods__["pstart"] = _pylibmpsse.mpsse_context_pstart_get
    if _newclass:pstart = property(_pylibmpsse.mpsse_context_pstart_get, _pylibmpsse.mpsse_context_pstart_set)
    __swig_setmethods__["pstop"] = _pylibmpsse.mpsse_context_pstop_set
    __swig_getmethods__["pstop"] = _pylibmpsse.mpsse_context_pstop_get
    if _newclass:pstop = property(_pylibmpsse.mpsse_context_pstop_get, _pylibmpsse.mpsse_context_pstop_set)
    __swig_setmethods__["pidle"] = _pylibmpsse.mpsse_context_pidle_set
    __swig_getmethods__["pidle"] = _pylibmpsse.mpsse_context_pidle_get
    if _newclass:pidle = property(_pylibmpsse.mpsse_context_pidle_get, _pylibmpsse.mpsse_context_pidle_set)
    __swig_setmethods__["gpioh"] = _pylibmpsse.mpsse_context_gpioh_set
    __swig_getmethods__["gpioh"] = _pylibmpsse.mpsse_context_gpioh_get
    if _newclass:gpioh = property(_pylibmpsse.mpsse_context_gpioh_get, _pylibmpsse.mpsse_context_gpioh_set)
    __swig_setmethods__["trish"] = _pylibmpsse.mpsse_context_trish_set
    __swig_getmethods__["trish"] = _pylibmpsse.mpsse_context_trish_get
    if _newclass:trish = property(_pylibmpsse.mpsse_context_trish_get, _pylibmpsse.mpsse_context_trish_set)
    __swig_setmethods__["bitbang"] = _pylibmpsse.mpsse_context_bitbang_set
    __swig_getmethods__["bitbang"] = _pylibmpsse.mpsse_context_bitbang_get
    if _newclass:bitbang = property(_pylibmpsse.mpsse_context_bitbang_get, _pylibmpsse.mpsse_context_bitbang_set)
    __swig_setmethods__["tx"] = _pylibmpsse.mpsse_context_tx_set
    __swig_getmethods__["tx"] = _pylibmpsse.mpsse_context_tx_get
    if _newclass:tx = property(_pylibmpsse.mpsse_context_tx_get, _pylibmpsse.mpsse_context_tx_set)
    __swig_setmethods__["rx"] = _pylibmpsse.mpsse_context_rx_set
    __swig_getmethods__["rx"] = _pylibmpsse.mpsse_context_rx_get
    if _newclass:rx = property(_pylibmpsse.mpsse_context_rx_get, _pylibmpsse.mpsse_context_rx_set)
    __swig_setmethods__["txrx"] = _pylibmpsse.mpsse_context_txrx_set
    __swig_getmethods__["txrx"] = _pylibmpsse.mpsse_context_txrx_get
    if _newclass:txrx = property(_pylibmpsse.mpsse_context_txrx_get, _pylibmpsse.mpsse_context_txrx_set)
    __swig_setmethods__["tack"] = _pylibmpsse.mpsse_context_tack_set
    __swig_getmethods__["tack"] = _pylibmpsse.mpsse_context_tack_get
    if _newclass:tack = property(_pylibmpsse.mpsse_context_tack_get, _pylibmpsse.mpsse_context_tack_set)
    __swig_setmethods__["rack"] = _pylibmpsse.mpsse_context_rack_set
    __swig_getmethods__["rack"] = _pylibmpsse.mpsse_context_rack_get
    if _newclass:rack = property(_pylibmpsse.mpsse_context_rack_get, _pylibmpsse.mpsse_context_rack_set)
    def __init__(self, *args): 
        this = _pylibmpsse.new_mpsse_context(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _pylibmpsse.delete_mpsse_context
    __del__ = lambda self : None;
mpsse_context_swigregister = _pylibmpsse.mpsse_context_swigregister
mpsse_context_swigregister(mpsse_context)

MPSSE = _pylibmpsse.MPSSE
Open = _pylibmpsse.Open
OpenIndex = _pylibmpsse.OpenIndex
Close = _pylibmpsse.Close
ErrorString = _pylibmpsse.ErrorString
SetMode = _pylibmpsse.SetMode
EnableBitmode = _pylibmpsse.EnableBitmode
SetClock = _pylibmpsse.SetClock
GetClock = _pylibmpsse.GetClock
GetVid = _pylibmpsse.GetVid
GetPid = _pylibmpsse.GetPid
GetDescription = _pylibmpsse.GetDescription
SetLoopback = _pylibmpsse.SetLoopback
SetCSIdle = _pylibmpsse.SetCSIdle
Start = _pylibmpsse.Start
Write = _pylibmpsse.Write
Stop = _pylibmpsse.Stop
GetAck = _pylibmpsse.GetAck
SetAck = _pylibmpsse.SetAck
SendAcks = _pylibmpsse.SendAcks
SendNacks = _pylibmpsse.SendNacks
FlushAfterRead = _pylibmpsse.FlushAfterRead
PinHigh = _pylibmpsse.PinHigh
PinLow = _pylibmpsse.PinLow
SetDirection = _pylibmpsse.SetDirection
WriteBits = _pylibmpsse.WriteBits
ReadBits = _pylibmpsse.ReadBits
WritePins = _pylibmpsse.WritePins
ReadPins = _pylibmpsse.ReadPins
PinState = _pylibmpsse.PinState
Tristate = _pylibmpsse.Tristate
Version = _pylibmpsse.Version
class swig_string_data(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, swig_string_data, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, swig_string_data, name)
    __repr__ = _swig_repr
    __swig_setmethods__["size"] = _pylibmpsse.swig_string_data_size_set
    __swig_getmethods__["size"] = _pylibmpsse.swig_string_data_size_get
    if _newclass:size = property(_pylibmpsse.swig_string_data_size_get, _pylibmpsse.swig_string_data_size_set)
    __swig_setmethods__["data"] = _pylibmpsse.swig_string_data_data_set
    __swig_getmethods__["data"] = _pylibmpsse.swig_string_data_data_get
    if _newclass:data = property(_pylibmpsse.swig_string_data_data_get, _pylibmpsse.swig_string_data_data_set)
    def __init__(self, *args): 
        this = _pylibmpsse.new_swig_string_data(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _pylibmpsse.delete_swig_string_data
    __del__ = lambda self : None;
swig_string_data_swigregister = _pylibmpsse.swig_string_data_swigregister
swig_string_data_swigregister(swig_string_data)

Read = _pylibmpsse.Read
Transfer = _pylibmpsse.Transfer


