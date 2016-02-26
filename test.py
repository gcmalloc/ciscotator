import unittest
from ciscotator.con import serialswitch as serial
from ciscotator.switch import SwitchMode


class SwitchTest(unittest.TestCase):

    def setUp(self):
        self.switch = serial.SerialSwitch()

    def test_send(self):
        #output = self.switch.send_command('show version')
        self.switch.send('show version' + self.switch.line_ending)
        output = self.switch.expect_prompt()
        self.assertIn("This product contains cryptographic features and is subject to United", output)
        self.switch.send('show version' + self.switch.line_ending)
        output = self.switch.expect_prompt()
        self.assertIn("This product contains cryptographic features and is subject to United", output)

    def test_send_command(self):
        output = self.switch.send_command('show version')
        self.assertIn("This product contains cryptographic features and is subject to United", output)
        output = self.switch.send_command('show version')
        self.assertIn("This product contains cryptographic features and is subject to United", output)


    def test_update_status(self):
        self.switch.update_status()

    def test_two_disable(self):
        self.switch.disable()
        self.switch.mode == SwitchMode.disable
        self.switch.disable()
        self.switch.mode == SwitchMode.disable

    def test_switch_disable_enable(self):
        self.switch.disable()
        self.switch.mode == SwitchMode.disable
        self.switch.enable()
        self.switch.mode == SwitchMode.enable
        self.switch.disable()
        self.switch.mode == SwitchMode.disable
        self.switch.enable()
        self.switch.mode == SwitchMode.enable
        self.switch.disable()
        self.switch.mode == SwitchMode.disable

    def test_two_enable(self):
        self.switch.enable()
        self.switch.mode == SwitchMode.enable
        self.switch.enable()
        self.switch.mode == SwitchMode.enable

    def test_two_config(self):
        self.switch.configure()
        self.switch.mode == SwitchMode.configure
        self.switch.configure()
        self.switch.mode == SwitchMode.configure

    def test_switch_enable_config(self):
        self.switch.configure()
        self.switch.mode == SwitchMode.configure
        self.switch.enable()
        self.switch.mode == SwitchMode.enable
        self.switch.configure()
        self.switch.mode == SwitchMode.configure
        self.switch.enable()
        self.switch.mode == SwitchMode.enable

    def test_switch_disable_config(self):
        self.switch.configure()
        self.switch.mode == SwitchMode.configure
        self.switch.disable()
        self.switch.mode == SwitchMode.disable
        self.switch.configure()
        self.switch.mode == SwitchMode.configure
        self.switch.disable()
        self.switch.mode == SwitchMode.disable

    def test_switch_three_mode(self):
        self.switch.disable()
        self.switch.mode == SwitchMode.disable
        self.switch.enable()
        self.switch.mode == SwitchMode.enable
        self.switch.configure()
        self.switch.mode == SwitchMode.configure
        self.switch.enable()
        self.switch.mode == SwitchMode.enable
        self.switch.disable()
        self.switch.mode == SwitchMode.disable
        output = self.switch.send_command('show version')
        self.assertIn("This product contains cryptographic features and is subject to United", output)

    def test_disable_command(self):
        self.switch.disable()
        self.switch.mode == SwitchMode.disable
        output = self.switch.send_command('show version')
        self.assertIn("This product contains cryptographic features and is subject to United", output)

    def test_conf_command(self):
        pass

if __name__ == '__main__':
    unittest.main()



