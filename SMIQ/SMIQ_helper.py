#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Instrument wrapper module

Author: Daniel Stadelmann, Tobias Badertscher
"""

import serial
import pyvisa as visa


class PrologixInstrument(object):
    """
    Class for instruments connected via prologix USB-GPIB adapter
    """
    serFd = None
    lineEnd = "\n"

    def __init__(self, gpibAddr, comPort, baud_rate=921600, timeout=0.25, silent=True):
        comPort = "COM18" #  int(comPort[3:]) - 1
        self._silent = silent
        self.gpibAddr = "GPIB25" #  gpibAddr

        if timeout is None:
            timeout = 2
        if PrologixInstrument.serFd is None:
            PrologixInstrument.serFd = serial.Serial(comPort, baudrate=baud_rate, timeout=timeout)
            PrologixInstrument.serFd.write("++mode 1" + self.lineEnd)
            PrologixInstrument.serFd.write("++ifc" + PrologixInstrument.lineEnd)
            # serialInterface.serFd.write("++auto 1"+serialInterface.lineEnd )
            PrologixInstrument.serFd.write("++read_tmo_ms 200" + PrologixInstrument.lineEnd)
            ver = tuple((int(i) for i in self.query('++ver').split()[-1].split('.')))
            if ver != (6, 107):
                raise (RuntimeError("Prologix is of version: %d.%d\n Please Update." % ver))

    def ask(self, cmd):
        return self.query(cmd)

    def query(self, cmd):
        PrologixInstrument.serFd.write('++addr %d' % self.gpibAddr + PrologixInstrument.lineEnd)
        if isinstance(cmd, list):
            for i in cmd:
                if not self._silent:
                    print("Command: \'%s\'" % cmd)
                PrologixInstrument.serFd.write(i + PrologixInstrument.lineEnd)
        else:
            if not self._silent:
                print("Command: \'%s\'" % cmd)
            PrologixInstrument.serFd.write(cmd + PrologixInstrument.lineEnd)
        # serialInterface.serFd.write("++read eoi"+serialInterface.lineEnd)
        PrologixInstrument.serFd.write("++read" + PrologixInstrument.lineEnd)
        retry = 1
        while retry > 0:
            res = PrologixInstrument.serFd.readlines()
            if len(res) > 0:
                if not self._silent:
                    print("Obtained result:")
                retry = 0
                if res[0][0] == '#':
                    sizeLen = int(res[0][1])
                    binSize = int(res[0][2:2 + sizeLen])
                    oRes = res[0][2 + sizeLen:] + res[1] + res[2][0:-1]
                    if binSize != len(oRes):
                        oRes = None
                    res = oRes
                    if not self._silent:
                        print("Obtained binary data of size %d" % binSize)
                else:
                    res = [i.strip('\n\r') for i in res]
                if not self._silent:
                    if len(str(res)) < 100:
                        print(res)
                    else:
                        print("Obtained large chunk of data of length %d" % len(res))
            retry -= 1
        if not isinstance(cmd, list):
            res = res[0]
        return res

    def write(self, cmd):
        PrologixInstrument.serFd.write('++addr %d' % self.gpibAddr + PrologixInstrument.lineEnd)
        if isinstance(cmd, list):
            for i in cmd:
                if not self._silent:
                    print("Command: \"%s\"" % cmd)
                PrologixInstrument.serFd.write(i + PrologixInstrument.lineEnd)
        else:
            PrologixInstrument.serFd.write(cmd + PrologixInstrument.lineEnd)
            if not self._silent:
                print("Command: \"%s\"" % cmd)
        return


class ScpiInstrumentWrapper(object):
    """
    Wrapper for visa/prologix connected instruments supporting SCPI language
    possible ressources are:
        - COM<NR> where '<NR>' is the COM-port number
        - GPIB::<ADDR> where <ADDR> is the GPIB address of the instrument
        - TCPIP::<IPADDR> where <IPADDR> is the ip address of the instrument
        - PROLOGIX::COM<NR>::GPIB::<ADDR> if the instrument is connected via Prologix
          USB-GPIB adapter. <NR> is the COM-port number of the Prologix adapter
          and <ADDR> is the GPIB address of the instrument
        - USB identifiers e.g. 'RSNRP::0x000c::101628'
    """

    def __init__(self, ressource):
        self.ressource = ressource
        if ressource[0:8].lower() == 'prologix':
            # device is connected via prologix adapter
            ressource = ressource.split('::')
            comport = ressource[1]
            gpibAddr = int(ressource[-1])
            self._inst = PrologixInstrument(gpibAddr, comport)
        else:
            # device is connected using a VISA ressource (includes LAN)
            rm = visa.ResourceManager()
            self._inst = rm.open_resource(ressource)
        self.clear()

    def query(self, cmd):
        return self._inst.query(cmd).strip('\n')

    def ask(self, cmd):
        return self.query(cmd)

    def write(self, cmd):
        self._inst.write(cmd)

    def read(self, ):
        return self._inst.read().strip('\n')

    def reset(self):
        """
        perform an instrument reset
        """
        self.write('*RST')
        return

    def clear(self):
        """
        Clear instrument status byte
        """
        self.write('*CLS')
        return

    def getIdent(self):
        """
        Get device ID
        """
        return self.ask('*IDN?')

    def wait(self, timeout=None):
        """
        Wait for operation to complete
        """
        if timeout is not None:
            to = self._inst.timeout
            self._inst.timeout = timeout
            self.ask('*OPC?')
            self._inst.timeout = to
        else:
            self.ask('*OPC?')

    @property
    def timeout(self, ):
        return self._inst.timeout

    @timeout.setter
    def timeout(self, timeout):
        self._inst.timeout = timeout
