import random

from checksum_utils import udp_checksum
import socket
import struct

# Define server address and port
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8000

# Create a raw socket
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)

# Define source and destination ports
SOURCE_ADDRESS = "127.0.0.1"
SOURCE_PORT = 63402

# Define real destination port and message
REAL_DEST_PORT = 7000

# Build a string array of 10 strings that build up a coherent message
messages = ["Hello", "from", "the", "client", "!", "How", "is", "it", "going", "?!"]

for i in range(len(messages)):

    message = messages[i].encode()
    # Pack the real destination port before actual data
    data = struct.pack(">H", REAL_DEST_PORT) + message

    # Build the UDP header
    udp_header = struct.pack("!HHHH", SOURCE_PORT, SERVER_PORT, 8 + len(data), 0)

    # Calculate checksum
    checksum = udp_checksum(SOURCE_ADDRESS, SERVER_ADDRESS, udp_header + data)

    rand_num = random.randint(1, 5)
    message = messages[i]
    if rand_num == 1:
        checksum_to_send = 1
    else:
        checksum_to_send = checksum

    udp_header = struct.pack("!HHHH", SOURCE_PORT, SERVER_PORT, 8 + len(data), checksum_to_send)
    packet = udp_header + data
    sock.sendto(packet, (SERVER_ADDRESS, SERVER_PORT))
    print(f"Sent UDP packet #{i} to {SERVER_ADDRESS}:{SERVER_PORT} with real destination port {REAL_DEST_PORT}")

# Build the entire packet

# Send the packet to the server

# Close the socket
sock.close()
