import os
import queue
import json
import socket
import threading

from utils import assign_ip_address



class VPN:
    def __init__(self):
        self.run_thread = None
        self.stop_thread = False
        self.SERVER_ADDRESS = "127.0.0.1"
        self.SERVER_PORT = 8000
        self.raw_socket = None
        self.log_queue = queue.Queue()

        if not os.path.exists('logs.txt'):
            with open('logs.txt', 'w') as f:
                pass

        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            self.users = {}
            with open('users.json', 'w') as f:
                json.dump(self.users, f)

        try:
            with open('restricted_users.json', 'r') as f:
                self.restricted_users = set(json.load(f))
        except FileNotFoundError:
            self.restricted_users = set()
            with open('restricted_users.json', 'w') as f:
                json.dump(list(self.restricted_users), f)

        try:
            with open('restricted_vlans.json', 'r') as f:
                self.restricted_vlans = set(json.load(f))
        except FileNotFoundError:
            self.restricted_vlans = set()
            with open('restricted_vlans.json', 'w') as f:
                json.dump(list(self.restricted_vlans), f)
    
    def start(self):
        self.raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        self.raw_socket.bind(('localhost', self.SERVER_PORT))

        # Create a new thread that will run the 'run' method, so we can still type in the console
        self.stop_thread = False
        self.run_thread = threading.Thread(target=self.run)
        self.run_thread.start()

        print(f"VPN started on {self.SERVER_ADDRESS}:{self.SERVER_PORT}")

    def stop(self):
        if self.run_thread is not None:
            self.raw_socket.close()
            self.raw_socket = None
            self.run_thread = None
    
    def create_user(self, username, password, vlan_id):
        # Assign an IP address and a port to the user
        ip_address, port = assign_ip_address()
        self.users[username] = {'password': password, 'vlan_id': vlan_id, 'ip_address': ip_address, 'port': port}
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

        self.log_message(f"User {username} created with IP address {ip_address}, port {port} and vlan {vlan_id}")

    def restrict_user(self, port):
        self.restricted_users.add(port)
        with open('restricted_users.json', 'w') as f:
            json.dump(list(self.restricted_users), f)

    def restrict_vlan(self, vlan_id):
        self.restricted_vlans.add(vlan_id)
        with open('restricted_vlans.json', 'w') as f:
            json.dump(list(self.restricted_vlans), f)

    def validate_user(self, sender_addr, sender_port):
        # Check if the sender's IP address and port are registered
        user_data = next((user for user in self.users.values() if user['port'] == sender_port), None)
        if user_data is None:
            self.log_message(f"Ignored packet coming from unregistered user: {sender_addr}:{sender_port}")
            return False

        # Check if the sender's port is restricted
        if str(sender_port) in self.restricted_users:
            self.log_message(f"Ignored packet coming from restricted port: {sender_port}")
            return False

        # Check if the user's VLAN is restricted
        if str(user_data['vlan_id']) in self.restricted_vlans:
            self.log_message(f"Ignored packet from restricted VLAN: {user_data['vlan_id']}")
            return False

        # If all validations pass, return True
        return True

    def log_message(self, message):
        # Add the message to the queue
        self.log_queue.put(message)

        # Write the message to the file
        with open('logs.txt', 'a') as f:
            f.write(message + '\n')