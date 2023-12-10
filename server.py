from checksum_utils import udp_checksum
import socket
import struct


def process_data(data):
    # ... interpret and handle data based on content ...
    print("Process data not implemented")


# Create and bind raw socket
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 7000
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
raw_socket.bind(('localhost', SERVER_PORT))

while True:
    # Receive data
    data, addr = raw_socket.recvfrom(65535)

    # Unpack UDP header
    udp_header = data[20:28]
    udp_data = struct.unpack('!HHHH', udp_header)

    # Extract information
    source_port = udp_data[0]
    dest_port = udp_data[1]
    length = udp_data[2]
    checksum = udp_data[3]

    # Check if the packet matches the filter criteria
    if dest_port == SERVER_PORT:

        # Check checksum
        received_checksum = udp_data[3]

        sender_address, sender_port = addr

        # Set checksum field to zero before calculating checksum
        zero_checksum_header = udp_header[:6] + b'\x00\x00' + udp_header[8:]
        calculated_checksum = udp_checksum(sender_address, SERVER_ADDRESS, zero_checksum_header + data[28:])

        if received_checksum != calculated_checksum:
            print("Checksum does not match, packet might be corrupted")

        # Print basic information
        print("Basic Information: ")
        print(f"UDP packet received from {addr}")
        print(f"Source port: {source_port}, Destination port: {dest_port}")
        print(f"Length: {length}, Checksum: {checksum}")

        # Process the packet
        print("Received valid packet:", data[28:])
        process_data(data[28:])
    else:
        # Discard the packet
        print("Ignoring packet coming from: ", source_port)

    print("---------------------------------------------------------")

# Close socket
raw_socket.close()
