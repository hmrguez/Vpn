from utils import assign_ip_address
from vpn import VPN  # Import the VPN class from vpn.py

# Create a VPN instance
vpn = VPN()


def main():
    while True:
        command = input("Enter command: ").split()

        if command[0] == 'start':
            vpn.start()
        elif command[0] == 'stop':
            vpn.stop()
        elif command[0] == 'create_user':
            vpn.create_user(command[1], command[2], command[3])
        elif command[0] == 'restrict_vlan':
            vpn.restrict_vlan(command[1])
        elif command[0] == 'restrict_user':
            vpn.restrict_user(command[1])
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
