#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore


class MusstCommand: # SpecCommandA
    def __init__(self, *args, **kwargs):
        SpecCommandA.__init__(self, *args, **kwargs)
        self.queue = []
        self.callback = None

    def runCommand(self, command, callback=None):
        chunk = command, callback,
        self.queue.append(chunk)
        self.checkQueue()

    def checkQueue(self):
        if self.queue:
            command, callback = self.queue.pop(0)
            self.callback = callback
            self.executeCommand(command)

    def replyArrived(self, reply):
        if callable(self.callback):
            self.callback(reply.data)
            self.callback = None
        self.checkQueue()


class Musst(QtCore.QObject):
    idleSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        # self.init_musst_commands = (
        #     stop current program
            # 'musst_comm("ABORT")',
            # 'musst_comm("BTRIG 0")',
            # 'musst_comm("CLEAR")',
            # 'musst_comm("HSIZE 0")',
            # set buffer size
            # 'musst_comm("ESIZE 500000 1")',
            # upload the program
            # 'musst_upload_program("musst", "{0}", 1)'.format(config.musstFirmware),
        # )
        # self.logger = parent.logger
        # self.timer = QtCore.QTimer(self)
        # self.timer.setInterval(500)
        # self.timer.timeout.connect(lambda: self.runCommand('musst_comm("?STATE")', self.checkIdle))
        # self.cmd = None

    def checkIdle(self, value):
        if value == 'IDLE':
            self.timer.abort()
            self.idleSignal.emit()

    def connectToSpec(self):
        return
        # try:
        #     self.cmd = MusstCommand('', '{0}:{1}'.format(config.musstHost, config.musstSession))
        # except SpecClientError:
        #     self.logger.error("Musst could not be connected!")
        # else:
        #     self.reset()

    def reset(self):
        """ (Re)Init the musst """
        callback = None
        for i, musst_command in enumerate(self.init_musst_commands, 1):
            if i == len(self.init_musst_commands):
                callback = self.log
            self.runCommand(musst_command, callback)

    def log(self):
        self.self.logger.info('Musst is connected')

    def setVar(self, var, value, callback=None):
        self.runCommand('musst_comm("VAR {} {:d}")'.format(var, int(value)), callback)

    def runScan(self, opts):
        # points, ct, points2, points3
        return
        # params = {
        #     'STARTDELAY': config.musstTimeout2 * 1e6,
        #     'NPOINTS': points,
        #     'CTIME': ct * 1e6,
        #     'INITDELAY': config.musstTimeout1 * 1e6,
        #     'NPOINTS2': points2,
        #     'NPOINTS2A': points3
        # }
        # for var in params:
        #     self.setVar(var, params[var])
        # self.runCommand('musst_comm("RUN SCAN")')
        # self.timer.start()

    def abort(self):
        return
        self.runCommand('musst_comm("ABORT")',
                        lambda _: self.logger.warn('Musst has been stopped! Message: {}'.format(_)))
        self.closeShutter()

    def openShutter(self):
        self.runCommand('musst_comm("RUN SHUTTER_OPEN")',
                        lambda _: self.logger.info('Shutter is open: {}'.format(_)))

    def closeShutter(self):
        self.runCommand('musst_comm("RUN SHUTTER_CLOSE")',
                        lambda _: self.logger.info('Shutter is closed: {}'.format(_)))

    def trigChannel(self, channel, trigtime=0.1):
        self.runCommand(
            'trigch {:d} {:.2f}'.format(channel, trigtime),
            lambda _: self.logger.info('Musst triggers channel {:d} for {:.2f} seconds: {}'.format(
                channel, trigtime, _)))

    def runCommand(self, command, callback=None):
        if not self.cmd:
            return False
        try:
            self.cmd.runCommand(command, callback)
        except SpecClientError:
            self.logger.error('The connections to MUSST has been lost')
            return False
        return True

    def isConnected(self):
        return False
