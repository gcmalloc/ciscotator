import serial
from ..switch import Switch


class SerialSwitch(Switch):
    def __init__(self, serial_device='/dev/ttyUSB0', **kwargs):
        self.serial = serial.Serial(serial_device)
        super(SerialSwitch, self).__init__(**kwargs)

    def send(self, s=''):
        return self.serial.write(s)

    def recv(self, nbytes=None):
        return self.serial.read(nbytes or self.buffer_size)
