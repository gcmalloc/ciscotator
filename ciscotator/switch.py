from contextlib import contextmanager
import enum
import time
import logging
import re


logging.basicConfig(level=logging.DEBUG)
DEFAULT_BUFFER_SIZE = 1000

class SwitchMode(enum.Enum):
    disable = 0
    enable = 1
    configure = 2

class Switch(object):
    """docstring for Switch"""
    def __init__(self, line_ending='\r\n',
                 enable_password=None, username=None,
                 password=None, quiet=False, buffer_size=DEFAULT_BUFFER_SIZE):
        self.line_ending = line_ending
        self.quiet = quiet
        self.username = username
        self.password = password
        self.line_ending = line_ending
        self.enable_password = enable_password
        self.mode = SwitchMode.disable
        self.buffer_size = buffer_size
        self.update_status()
        #self.disable_paging()

    def expect_prompt(self):
        if self.mode == SwitchMode.configure:
            logging.debug('expecting )#')
            # config
            return self.expect(')#')
        elif self.mode == SwitchMode.enable:
            logging.debug('expecting #')
            # enable
            return self.expect('#')
        elif self.mode == SwitchMode.disable:
            logging.debug('expecting >')
            # normal mode ?
            return self.expect('>')

    def expect(self, char):
        matching_ref = re.compile(char)
        incoming_buffer = ''
        logging.debug('search for {!s}'.format(char))
        while not bool(matching_ref.search(incoming_buffer)):
            #logging.debug('current buffer: {!s}'.format(incoming_buffer))
            current_char = self.recv(1)
            incoming_buffer += current_char

        return incoming_buffer

    def send(self, s):
        """send a buffer of byte to the switch"""
        raise NotImplemented()

    def recv(self, nbytes):
        """receive the incoming nbyte from the switch,
        will return None if nothing is available
        """
        raise NotImplemented()

    def disable_paging(self):
        self.send_command("terminal length 0")

    def update_status(self):
        self.send(self.line_ending)
        output = self.expect(">|#|[yes/no]:|'yes' or 'no'.")
        logging.debug("status detection output is {!s}".format(output))
        if '>' == output[-1]:
            self.mode = SwitchMode.disable
        elif ')#' == output[-2:]:
            self.mode = SwitchMode.configure
        elif '#' == output[-1]:
            self.mode = SwitchMode.enable
        elif ':' == output[-1] or '.' == output[-1]:
            self.send('no' + self.line_ending)
        logging.debug("current mode is" +
                      str(self.mode))
        return self.mode

    def send_command(self, command='', wait_time=0.1):
        self.send(command)
        self.send(self.line_ending)
        time.sleep(wait_time)
        output = self.expect_prompt()
        logging.debug("command output is:" + output)
        return output

    def disable(self):
        self.update_status()
        if self.mode == SwitchMode.configure:
            enable()
        if self.mode == SwitchMode.enable:
            self.send_command('disable')
        self.update_status()

    def enable(self):
        self.update_status()
        if self.mode == SwitchMode.configure:
            self.send_command('exit')
            self.update_status()
        elif not (self.mode == SwitchMode.enable):
            self.send_command('enable')
            if self.enable_password:
                self.send(self.enable_password)
            self.update_status()

    def configure(self):
        self.enable()
        if not self.mode == SwitchMode.configure:
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
