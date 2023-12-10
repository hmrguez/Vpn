import random


def assign_ip_address():
    ip_address = f"127.0.0.1"
    port = random.randint(1024, 65535)
    return ip_address, port
