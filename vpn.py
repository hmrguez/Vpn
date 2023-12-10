import socket
import struct
from checksum_utils import udp_checksum
from utils import assign_ip_address


class VPN:
    def __init__(self):
        self.SERVER_ADDRESS = "127.0.0.1"
        self.SERVER_PORT = 8000
        self.raw_socket = None
        self.users = {}
        self.restricted_users = set()
        self.restricted_vlans = set()

    def start(self):
        self.raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.raw_socket.bind(('localhost', self.SERVER_PORT))
        self.run()

    def stop(self):
        if self.raw_socket is not None:
            self.raw_socket.close()
            self.raw_socket = None

    def create_user(self, username, password, vlan_id):
        # Assign an IP address and a port to the user
        ip_address, port = assign_ip_address()
        self.users[username] = {'password': password, 'vlan_id': vlan_id, 'ip_address': ip_address, 'port': port}
        print(f"User {username} created with IP address {ip_address}, port {port} and vlan {vlan_id}")

    def restrict_user(self, port):
        self.restricted_users.add(port)

    def restrict_vlan(self, vlan_id):
        self.restricted_vlans.add(vlan_id)

    def validate_user(self, sender_addr, sender_port):
        # Check if the sender's IP address and port are registered
        user_data = next((user for user in self.users.values() if user['port'] == sender_port), None)
        if user_data is None:
            print("Ignoring packet coming from unregistered user: ", sender_addr, ":", sender_port)
            return False

        print("Restricted users: ", self.restricted_users)
        print("Sender port: ", sender_port)

        # Check if the sender's port is restricted
        if str(sender_port) in self.restricted_users:
            print("Ignoring packet coming from restricted port: ", sender_port)
            return False

        # Check if the user's VLAN is restricted
        if str(user_data['vlan_id']) in self.restricted_vlans:
            print("Ignoring packet from restricted VLAN: ", user_data['vlan_id'])
            return False

        # If all validations pass, return True
        return True

    def run(self):
        while True:
            # Receive data
            data, addr = self.raw_socket.recvfrom(65535)

            # Unpack UDP header
            udp_header = data[20:28]
            udp_data = struct.unpack('!HHHH', udp_header)

            # Extract information
            source_port = udp_data[0]
            dest_port = udp_data[1]
            length = udp_data[2]

            # Check if the packet matches the filter criteria
            if dest_port == self.SERVER_PORT:

                # Sender port is always 0 because it sends directly through the interface
                sender_addr, sender_port = addr

                # Check if the user is created and not restricted
                if not self.validate_user(sender_addr, source_port):
                    continue

                # Check checksum
                received_checksum = udp_data[3]

                # Set checksum field to zero before calculating checksum
                zero_checksum_header = udp_header[:6] + b'\x00\x00' + udp_header[8:]
                calculated_checksum = udp_checksum(sender_addr, self.SERVER_ADDRESS, zero_checksum_header + data[28:])

                if received_checksum != calculated_checksum:
                    print("Checksum does not match, packet might be corrupted")
                    continue  # Skip the rest of the loop and wait for the next packet

                # Extract destination port from data
                forward_port = struct.unpack('!H', data[28:30])[0]

                # Generate new UDP header with server port as source and dynamic port from data
                new_source_port = self.SERVER_PORT
                new_udp_header = struct.pack("!HHHH", new_source_port, forward_port, length, 0)

                # Calculate new checksum
                new_udp_checksum = udp_checksum(self.SERVER_ADDRESS, self.SERVER_ADDRESS, new_udp_header + data[28:])
                new_udp_header = struct.pack("!HHHH", new_source_port, forward_port, length, new_udp_checksum)

                # Combine new header and original data for forwarding
                forwarded_packet = new_udp_header + data[28:]

                # Send the forwarded packet
                self.raw_socket.sendto(forwarded_packet, (self.SERVER_ADDRESS, forward_port))

                # Print confirmation
                print(f"Forwarded packet to {self.SERVER_ADDRESS}:{forward_port}")
            else:
                # Discard the packet
                print("Ignoring packet coming from: ", source_port)

            print("---------------------------------------------------------")

