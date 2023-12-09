import socket
import struct


# Helper methods
def udp_checksum(source_ip, dest_ip, udp_packet):
    pseudo_header = struct.pack('!4s4sBBH',
                                socket.inet_aton(source_ip),
                                socket.inet_aton(dest_ip),
                                0,
                                socket.IPPROTO_UDP,
                                len(udp_packet))
    return calc_checksum(pseudo_header + udp_packet)


def calc_checksum(packet):
    if len(packet) % 2 != 0:
        packet += b'\0'
    res = sum((int.from_bytes(packet[i:i + 2], 'big') for i in range(0, len(packet), 2)))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return ~res & 0xffff


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

        # Set checksum field to zero before calculating checksum
        zero_checksum_header = udp_header[:6] + b'\x00\x00' + udp_header[8:]
        calculated_checksum = udp_checksum(SERVER_ADDRESS, SERVER_ADDRESS, zero_checksum_header + data[28:])

        if received_checksum != calculated_checksum:
            print("Checksum does not match, packet might be corrupted")

        # Print basic information
        print("Basic Information: ")
        print(f"UDP packet received from {addr}")
        print(f"Source port: {source_port}, Destination port: {dest_port}")
        print(f"Length: {length}, Checksum: {checksum}")
        print("---------------------------------------------------------")

        # Process the packet
        print("Received valid packet:", data[28:])
        process_data(data[28:])
    else:
        # Discard the packet
        print("Ignoring packet coming from: ", source_port)
        print("---------------------------------------------------------")

# Close socket
raw_socket.close()
