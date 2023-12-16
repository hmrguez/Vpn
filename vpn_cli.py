from utils import assign_ip_address
from vpn import VPN  # Import the VPN class from vpn.py

# Create a VPN instance
vpn = VPN()


def main():
    while True:
        command = input("\033[92mVPN > \033[0m").split()

        if command[0] == 'start':
            print("\033[93mStarting VPN...\033[0m")
            vpn.start()
        elif command[0] == 'stop':
            print("\033[93mStopping VPN...\033[0m")
            vpn.stop()
        elif command[0] == 'create_user':
            vpn.create_user(command[1], command[2], command[3])
        elif command[0] == 'restrict_vlan':
            vpn.restrict_vlan(command[1])
        elif command[0] == 'restrict_user':
            vpn.restrict_user(command[1])
        elif command[0] == 'show_logs':
            print("\033[93mShowing logs...\033[0m")
            while not vpn.log_queue.empty():
                print("\033[96m" + vpn.log_queue.get() + "\033[0m")
                print("---------------------------------------------------------")
        else:
            print("\033[91mInvalid command\033[0m")


if __name__ == "__main__":
    main()
