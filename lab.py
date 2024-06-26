from netmiko import ConnectHandler

if __name__ == "__main__":

    switch = {
        'device_type': 'cisco_ios_telnet',
        'host':   '10.100.0.1',
        'username': 'Q',
        'password': 'BA',
        'secret': 'Q-BA'
    }

    commands = []
    for i in range(1,6):
        commands.extend([
            f"vlan {i * 10}",
            "exit",
            f"int fa 0/{i}",
            f"switchport access vlan {i * 10}",
            "switchport mode access",
            "exit"
        ])
    try:
       handler = ConnectHandler(**switch)
       if not handler.check_enable_mode(): handler.enable()
       handler.send_config_set(commands)
    finally:
       if handler:
           handler.disconnect()
