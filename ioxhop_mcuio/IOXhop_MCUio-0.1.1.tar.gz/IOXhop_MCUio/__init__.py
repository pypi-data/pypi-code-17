from smbus import SMBus
import time

_devAddr = 0x08
Wire = None

LOW = INPUT = 0
HIGH = OUTPUT = 1

A0, A1, A2, A3, A4, A5 = [14, 15, 16, 17, 18, 19]

def begin(devAddr, ch = 1):
	global Wire
	_devAddr = devAddr
	Wire = SMBus(1)

def _i2cWrite(addr, value):
	Wire.write_byte_data(_devAddr, addr, value)

def _i2cRead(addr):
	return Wire.read_byte_data(_devAddr, addr)

def mode(pin, mode):
	_i2cWrite(pin+1, 0x01 if mode == OUTPUT else 0x0)

def set(pin, lavel):
	_i2cWrite(pin + 21, 0x01 if lavel == HIGH else 0x0)

def get(pin):
	return HIGH if _i2cRead(pin+21) == 0x01 else LOW

def Aget(pin):
	if (pin - 14 + 41) < 41:
		return 0xFFFF
	
	adc = Wire.read_i2c_block_data(_devAddr, (pin - 14) * 2 + 41, 2)
	return adc[0]|adc[1]<<8

def pwm(pin, value):
	addr = 0
	if pin == 3:
		addr = 53
	elif pin == 5:
		addr = 54
	elif pin == 6:
		addr = 55
	elif pin == 9:
		addr = 56
	elif pin == 10:
		addr = 57
	elif pin == 11:
		addr = 58
	_i2cWrite(addr, value)

def tone(pin, frequency):
	
	Wire.write_i2c_block_data(_devAddr, 59, [(frequency>>8)&0xFF, 60, frequency&0xFF, 61, (pin&0x0F)|0x10])

def Dtone(pin):
	_i2cWrite(61, pin&0x0F)
