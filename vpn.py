from checksum_utils import udp_checksum
import socket
import struct

# Create and bind raw socket
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8000
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

    # Check if the packet matches the filter criteria
    if dest_port == SERVER_PORT:

        # Check checksum
        received_checksum = udp_data[3]
        sender_addr, sender_port = addr

        # Set checksum field to zero before calculating checksum
        zero_checksum_header = udp_header[:6] + b'\x00\x00' + udp_header[8:]
        calculated_checksum = udp_checksum(sender_addr, SERVER_ADDRESS, zero_checksum_header + data[28:])

        if received_checksum != calculated_checksum:
            print("Checksum does not match, packet might be corrupted")
            continue  # Skip the rest of the loop and wait for the next packet

        # Extract destination port from data
        forward_port = struct.unpack('!H', data[28:30])[0]

        # Generate new UDP header with server port as source and dynamic port from data
        new_source_port = SERVER_PORT
        new_udp_header = struct.pack("!HHHH", new_source_port, forward_port, length, 0)

        # Calculate new checksum
        # TODO change destination address to actual client address
        new_udp_checksum = udp_checksum(SERVER_ADDRESS, SERVER_ADDRESS, new_udp_header + data[28:])
        new_udp_header = struct.pack("!HHHH", new_source_port, forward_port, length, new_udp_checksum)

        # Combine new header and original data for forwarding
        forwarded_packet = new_udp_header + data[28:]

        # Send the forwarded packet
        raw_socket.sendto(forwarded_packet, (SERVER_ADDRESS, forward_port))

        # Print confirmation
        print(f"Forwarded packet to {SERVER_ADDRESS}:{forward_port}")
    else:
        # Discard the packet
        print("Ignoring packet coming from: ", source_port)
        print("---------------------------------------------------------")

# Close socket
raw_socket.close()
