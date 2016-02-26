import paramiko
import sys
import logging
from ..switch import Switch, DEFAULT_BUFFER_SIZE
from contextlib import contextmanager

logging.basicConfig(level=logging.DEBUG)


class SSHSwitch(Switch):
    """docstring for Switch"""

    def __init__(self, ip, **kwargs):
        self.connect()
        super(Switch, self).__init__(**kwargs)

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(self.ip,
                            username=self.username,
                            password=self.password,
                            look_for_keys=False,
                            allow_agent=False)
        self.shell = self.client.invoke_shell()

    def send(self, s=''):
        return self.shell.send(s)

    def recv(self, nbytes=None):
        return self.shell.recv(nbytes or self.buffer_size)

    def flush_input(self):
        pass
