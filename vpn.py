import os
import queue
import json
import socket
import threading


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