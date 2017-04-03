#!/usr/bin/python
# -*- coding: utf-8 -*-

import struct
import ctypes
import serial
from PyQt5 import QtCore


class Status(ctypes.BigEndianStructure):
    """
    Cryostream sends bytes in big endian >
    Description of the packet is at:
    http://www.oxcryo.com/serialcomms/700series/cs_status.html
    """
    _fields_ = (
        ('PacketSize', ctypes.c_ubyte),
        ('PacketType', ctypes.c_ubyte),
        ('GasSetPoint', ctypes.c_ushort),
        ('GasTemp', ctypes.c_ushort),
        ('GasError', ctypes.c_short),
        ('RunMode', ctypes.c_ubyte),
        ('PhaseId', ctypes.c_ubyte),
        ('RampRate', ctypes.c_ushort),
        ('TargetTemp', ctypes.c_ushort),
        ('EvapTemp', ctypes.c_ushort),
        ('SuctTemp', ctypes.c_ushort),
        ('Remaining', ctypes.c_ushort),
        ('GasFlow', ctypes.c_ubyte),
        ('GasHeat', ctypes.c_ubyte),
        ('EvapHeat', ctypes.c_ubyte),
        ('SuctHeat', ctypes.c_ubyte),
        ('LinePressure', ctypes.c_ubyte),
        ('AlarmCode', ctypes.c_ubyte),
        ('RunTime', ctypes.c_ushort),
        ('ControllerNumber', ctypes.c_ushort),
        ('SoftwareVersion', ctypes.c_ubyte),
        ('EvapAdjust', ctypes.c_ubyte),
        ('TurboMode', ctypes.c_ubyte),
        ('HardwareType', ctypes.c_ubyte),
        ('ShutterState', ctypes.c_ubyte),
        ('ShutterTime', ctypes.c_ubyte),
        ('UnusedOne', ctypes.c_ubyte),
        ('UnusedTwo', ctypes.c_ubyte),
        ('UnusedThree', ctypes.c_ushort),
        ('UnusedFour', ctypes.c_ushort),
    )

    def __init__(self, buffer):
        if len(buffer) > ctypes.sizeof(self):
            raise ValueError('The size of buffer is to big for the structure')
        ctypes.memmove(ctypes.addressof(self), buffer, len(buffer))


class Cryostream(QtCore.QObject):
    sigStatus = QtCore.pyqtSignal(dict)
    sigError = QtCore.pyqtSignal(str)

    AlarmMessages = (
        'No alarms exist',
        'Stop button has been pressed',
        'Stop command received',
        'End phase complete',
        'Purge phase complete',
        'Temp error > 5 K',
        'Back pressure > 0.5 bar',
        'Evaporator reduction at max',
        'Self-check fail',
        'Gas flow < 2 l/min',
        'Temp error > 25 K',
        'Sensor detects wrong gas type',
        'Unphysical temperature reported',
        'Suct temperature out of range',
        'Invalid ADC reading',
        'Degradation of power supply',
        'Heat sink overheating',
        'Power supply overheating',
        'Power failure',
        'Refrigerator stage is too cold',
        'Refrigerator stage failed to reach base in time',
        'Cryodrive is not responding',
        'Cryodrive reports an error',
        'No nitrogen available',
        'No helium available',
        'Vacuum gauge is not responding',
        'Vacuum is out of range',
        'RS232 communication error',
        'Coldhead temp > 315 K',
        'Coldhead temp > 325 K',
        'Wait for End to complete',
        'Do not open the cryostat',
        'Disconnect Xtal sensor',
        'Cryostat is open',
        'Cryostat open for more than 10 min',
        'Sample temp > 320 K',
        'Sample temp > 325 K',
    )
    RunModeMessages = (
        'Initialization: running through system checks',
        'Some failure in system checks: check the screen',
        'System checks OK, awaiting for commands',
        'Gas is flowing',
        'Special commissioning mode',
        'System has shut down cleanly',
        'System has shut down due to hardware error',
    )
    Phases = (
        'Ramp',
        'Cool',
        'Plat',
        'Hold',
        'End',
        'Purge',
        'DeletePhase',
        'LoadProgram',
        'SaveProgram',
        'Soak',
        'Wait',
    )
    HardwareType = (
        'System unknown',
        'Regular system, no Cryoshutter',
        'Plus system, no Cryoshutter',
        'Regular system fitted with Cryoshutter',
        'Plus system fitted with Cryoshutter',
    )
    SizePacketV1 = 32
    TypePacketV1 = 1
    SizePacketV2 = 42
    TypePacketV2 = 2
    StartUpRunMode = 0
    StartUpFailRunMode = 1
    StartUpOkRunMode = 2
    RunRunMode = 3
    SetUpRunMode = 4
    ShutdownOkRunMode = 5
    ShutdownFailRunMode = 6
    RestartCommand = 10
    RampCommand = 11
    PlatCommand = 12
    HoldCommand = 13
    CoolCommand = 14
    EndCommand = 15
    PurgeCommand = 16
    PauseCommand = 17
    ResumeCommand = 18
    StopCommand = 19
    TurboCommand = 20
    SetStatusFormatCommand = 40
    SerialPortTimeout = 2
    SerialPortPollTimeout = 500

    def __init__(self):
        super().__init__()
        self.buffer = b''
        self.sport = serial.Serial()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.poll)

    def isConnected(self):
        return self.timer.isActive()

    def start(self, device):
        if self.isConnected():
            return
        try:
            self.sport = serial.Serial(device, timeout=self.SerialPortTimeout)
        except serial.SerialException as err:
            self.sigError.emit(f'Cryostream error: {str(err)}')
        else:
            self.timer.start(self.SerialPortPollTimeout)
            self.send(self.SetStatusFormatCommand, 1)

    def pause(self):
        self.send(self.PauseCommand)

    def resume(self):
        self.send(self.ResumeCommand)

    def cstop(self):
        self.send(self.StopCommand)

    def restart(self):
        self.send(self.RestartCommand)

    def turboOn(self):
        self.send(self.TurboCommand, 1)

    def turboOff(self):
        self.send(self.TurboCommand, 0)

    def cool(self, target):
        self.send(self.CoolCommand, int(target * 100))

    def ramp(self, rate, target):
        self.send(self.RampCommand, rate, int(target * 100))

    def plat(self, duration):
        self.send(self.PlatCommand, duration)

    def hold(self):
        self.send(self.HoldCommand)

    def end(self, rate):
        self.send(self.EndCommand, rate)

    def purge(self):
        self.send(self.Purge)

    def stop(self):
        self.buffer = b''
        self.sport.close()
        self.timer.stop()

    def unpackStatus(self, buffer):
        s = Status(buffer)
        d = {
            'TargetTemp': s.TargetTemp / 100,
            'SampleTemp': s.GasTemp / 100,
            'GasError': s.GasError / 100,
            'GasSetPoint': s.GasSetPoint / 100,
            'GasHeat': s.GasHeat,
            'EvapHeat': s.EvapHeat,
            'SuctHeat': s.SuctHeat,
            'GasFlow': s.GasFlow / 10,
            'EvapTemp': s.EvapTemp / 100,
            'SuctTemp': s.SuctTemp / 100,
            'LinePressure': s.LinePressure / 100,
            'AlarmCode': s.AlarmCode,
            'AlarmMessage': self.AlarmMessages[s.AlarmCode] if s.AlarmCode < len(self.AlarmMessages) else 'Unknown',
            'RunTime': s.RunTime,
            'Running': s.RunMode == self.RunRunMode,
            'Phase': self.Phases[s.PhaseId] if s.RunMode == self.RunRunMode else self.RunModeMessages[s.RunMode],
            'RampRate': s.RampRate,
            'Remaining': s.Remaining,
            'HardwareType': self.HardwareType[s.HardwareType],
            'TurboMode': bool(s.TurboMode),
        }
        if s.PacketType == self.TypePacketV2:
            d['HardwareType'] = self.HardwareType[s.HardwareType + 1],
        self.sigStatus.emit(d)

    def poll(self):
        self.buffer += self.sport.read(self.sport.in_waiting)
        while len(self.buffer) >= self.SizePacketV2:
            # the first two bytes are PacketSize == 32(42) and PacketType == 1(2)
            # we need to carry about them to separate the packets, since those could be broken sometimes
            s, t = struct.unpack('>2B', self.buffer[:2])
            if s == self.SizePacketV1 and t == self.TypePacketV1:
                limit = self.SizePacketV1
            elif s == self.SizePacketV2 and t == self.TypePacketV2:
                limit = self.SizePacketV2
            else:
                self.buffer = self.buffer[1:]
                continue
            self.unpackStatus(self.buffer[:limit])
            self.buffer = self.buffer[limit:]

    def send(self, command, *params):
        if self.isConnected():
            packet = struct.pack('>B', command)
            for v in params:
                t = '>B' if command in (self.SetStatusFormatCommand, self.TurboCommand) else '>H'
                packet += struct.pack(t, v)
            header = struct.pack('>B', len(packet) + struct.calcsize('>B'))
            self.sport.write(header + packet)
