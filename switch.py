import paramiko
import time
import sys
import logging
from contextlib import contextmanager

logging.basicConfig(level=logging.DEBUG)
DEFAULT_BUFFER_SIZE = 1000


class Switch(object):
    """docstring for Switch"""

    def __init__(self, ip, username, password,
                 line_ending='\n', enable_password=None,
                 buffer_size=DEFAULT_BUFFER_SIZE):
        super(Switch, self).__init__()
        self.ip = ip
        self.username = username
        self.password = password
        self.line_ending = line_ending
        self.enable_password = enable_password
        self.enable_mode = False
        self.configure_mode = False
        self.connect()

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(self.ip,
                            username=self.username,
                            password=self.password,
                            look_for_keys=False,
                            allow_agent=False)
        self.shell = self.client.invoke_shell()
        self.disable_paging()

    def disable_paging(self):
        self.send_command("terminal length 0")

    def get_buffer(self):
        """Clear the buffer on the screen
        """
        output = self.recv(self.buffer_size)
        return output

    def update_status(self):
        """
        """
        output = self.send_command()
        logging.debug("status detection output is " + output)
        if '>' == output[-1]:
            self.enable_mode = False
            self.configure_mode = False
        elif ')#' == output[-2:]:
            self.enable_mode = False
            self.configure_mode = True
        elif '#' == output[-1]:
            self.enable_mode = True
            self.configure_mode = False
        logging.debug("current status for enable is :" +
                      str(self.enable_mode))
        logging.debug("current status for disable is :" +
                      str(self.configure_mode))
        return self.enable

    def send(self, s):
        return self.shell.send(s)

    def recv(self, nbytes):
        return self.shell.recv()

    def send_command(self, command, wait_time=1):
        self.send(command)
        self.send(self.line_ending)
        time.sleep(wait_time)
        output = self.recv(self.buffer_size)
        logging.debug("command output is:" + output)
        return output

    def disable(self):
        self.update_status()
        if self.enable:
            self.send_command('disable')
        self.update_status()

    def enable(self):
        self.update_status()
        if self.configure_mode:
            self.send_command('exit')
            self.update_status()
        elif not self.enable_mode:
            self.send('enable' + self.line_ending)
            if self.enable_password:
                self.send(self.enable_password)
            self.update_status()

    def configure(self):
        self.enable()
        if not self.configure_mode:
            self.send_command('config t')
        self.update_status()

    @property
    @contextmanager
    def enable_context(self):
        self.enable()
        yield
        self.disable()

    @property
    @contextmanager
    def config_context(self):
        self.configure()
        yield
        self.enable()


if __name__ == '__main__':
    sw = Switch(sys.argv[1], sys.argv[2],
                sys.argv[3], enable_password=sys.argv[3])

    with sw.enable_context:
        print(sw.send_command("show interface status"))
