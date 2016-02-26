from ciscotator.con import serialswitch as serial


switch = serial.SerialSwitch()
print(switch.mode)
print(switch.send_command('show version'))
with switch.enable_context:
    print(switch.send_command('show version'))
