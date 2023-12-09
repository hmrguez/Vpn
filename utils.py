import random


def assign_ip_address():
    # Generate a random IP address within the range 192.168.1.0 - 192.168.255.255
    ip_address = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
    return ip_address
