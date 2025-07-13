from netmiko import ConnectHandler
from getpass import getpass

# Securely fetch SSH and enable passwords
ssh_password = getpass("Enter SSH password: ")
enable_password = getpass("Enter ENABLE password: ")

# Router IPs and interface info
routers = [
    {
        'host': '192.168.44.129',  # Router1
        'interfaces': [
            ('fa0/1', '10.1.1.1', '255.255.255.252'),
            ('fa1/0', '20.1.1.1', '255.255.255.252'),
        ]
    },
    {
        'host': '192.168.44.130',  # Router2
        'interfaces': [
            ('fa0/1', '30.1.1.1', '255.255.255.252'),
            ('fa1/0', '20.1.1.2', '255.255.255.252'),
        ]
    },
    {
        'host': '192.168.44.131',  # Router3
        'interfaces': [
            ('fa0/1', '40.1.1.1', '255.255.255.252'),
            ('fa1/0', '30.1.1.2', '255.255.255.252'),
        ]
    },
    {
        'host': '192.168.44.132',  # Router4
        'interfaces': [
            ('fa0/1', '10.1.1.2', '255.255.255.252'),
            ('fa1/0', '40.1.1.2', '255.255.255.252'),
        ]
    }
]

for router in routers:
    print(f"\nConnecting to {router['host']}...")
    device = {
        'device_type': 'cisco_ios',
        'host': router['host'],
        'username': 'admin',
        'password': ssh_password,
        'secret': enable_password,
    }

    try:
        connection = ConnectHandler(**device)
        connection.enable()

        config_cmds = []

        # Assign IPs to interfaces
        for intf, ip, mask in router['interfaces']:
            config_cmds += [
                f'interface {intf}',
                f'ip address {ip} {mask}',
                'no shutdown',
                'exit'
            ]

        # Configure OSPF in area 0
        config_cmds += ['router ospf 1']
        for _, ip, mask in router['interfaces']:
            wildcard = '.'.join(str(255 - int(octet)) for octet in mask.split('.'))
            network = ip[:ip.rfind('.')] + '.0'
            config_cmds.append(f'network {network} {wildcard} area 0')

        # Send config
        output = connection.send_config_set(config_cmds)
        print(output)

        # Save configuration (write memory)
        print("[✔] Saving configuration...")
        save_output = connection.send_command("write memory")
        print(save_output)

        # Show OSPF neighbor
        print("[✔] Showing OSPF neighbors...")
        neighbors = connection.send_command("show ip ospf neighbor")
        print(neighbors)

        # Show OSPF database
        print("[✔] Showing OSPF database...")
        database = connection.send_command("show ip ospf database")
        print(database)

        connection.disconnect()

    except Exception as e:
        print(f"[✖] Error with {router['host']}: {e}")
