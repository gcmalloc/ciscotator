# Cisco ssh api

Wrapper around the ssh interface for cisco switches.
Simple usage:

    sw = Switch(hostname, username, password)
    sw.send_command('bluh')

## Support for context management

Enable context:

    sw = Switch(hostname, username, password)
    with sw.enable_context:
        sw.send_command('reload')

Configuration context:

    sw = Switch(hostname, username, password)
    with sw.configuration_context:
        sw.send_command('errdisable detect cause gbic-invalid')
