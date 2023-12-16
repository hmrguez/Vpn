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
SOURCE_PORT = 56017

# Define real destination port and message
REAL_DEST_PORT = 7000
MESSAGE = b"Hello from the client!"

# Pack the real destination port before actual data
data = struct.pack(">H", REAL_DEST_PORT) + MESSAGE

# Build the UDP header
udp_header = struct.pack("!HHHH", SOURCE_PORT, SERVER_PORT, 8 + len(data), 0)

# Calculate checksum
udp_checksum = udp_checksum(SOURCE_ADDRESS, SERVER_ADDRESS, udp_header + data)
udp_header = struct.pack("!HHHH", SOURCE_PORT, SERVER_PORT, 8 + len(data), udp_checksum)

# Build the entire packet
packet = udp_header + data

# Send the packet to the server
sock.sendto(packet, (SERVER_ADDRESS, SERVER_PORT))
print(f"Sent UDP packet to {SERVER_ADDRESS}:{SERVER_PORT} with real destination port {REAL_DEST_PORT}")

# Close the socket
sock.close()
