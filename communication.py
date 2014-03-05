# Hashbot Communication Protocol Rev 2
# Copyright (C) 2014 Project Hashbang
# Created by Sultan Qasim Khan

import serial, struct, binascii
from crc16 import calcCrc16

class HashComm(object):
    def __init__(self, port='COM3'):
        self.ser = serial.Serial(port, 115200)
        self.msgId = 0  # Incremented by 2 every time a message is sent

    def putMessage(self, msgType, flags, data):
        # data should be bytes
        ph = struct.pack('<HHHL', msgType, flags, len(data), self.msgId)
        crc = calcCrc16(ph)
        crc = calcCrc16(data, crc)
        header = struct.pack('<HHHHL', crc, msgType, flags, length, self.msgId)
        msg = header + data
        hexMsg = b'#' + binascii.hexlify(msg).upper() + b'!'
        self.ser.write(hexMsg)
        self.msgId += 2

    def getMessage(self):
        # Eat up data until the #
        c = b'!'
        while c != b'#': c = self.ser.read()

        # Read the header
        header = binascii.unhexlify(self.ser.read(24))
        crc, msgType, flags, length, msgId = struct.unpack('<HHHHL', header)
        if length > 512: raise Exception('Corrupt header')

        # Read the message body
        data = binascii.unhexlify(self.ser.read(length * 2))

        # Check the crc
        newCrc = calcCrc16(header[2:])
        newCrc = calcCrc16(data, newCrc)
        if newCrc != crc: raise Exception('CRC error')

        # TODO: Handle the CONFIRMATION_NEEDED_FLAG

        return msgType, data
