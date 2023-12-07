import socket
import struct


# Define functions for processing different flags, interpreting data, etc.
def handle_syn(data, source_address, source_port):
    # ... send SYN-ACK response ...
    print("Handle SYN not implemented")


def process_data(data):
    # ... interpret and handle data based on content ...
    print("Process data not implemented")


def handle_other_flags(flags):
    # ... identify and handle other TCP flags ...
    print("Handle other flags not implemented")


# Create and bind raw socket
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 8000
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
raw_socket.bind(('localhost', SERVER_PORT))

while True:
    # Receive data
    data, addr = raw_socket.recvfrom(65535)

    # Unpack TCP header
    tcp_header = data[20:40]
    tcp_data = struct.unpack('!HHLLBBHHH', tcp_header)

    # Extract information
    source_port = tcp_data[0]
    dest_port = tcp_data[1]
    sequence_number = tcp_data[2]
    ack_number = tcp_data[3]
    data_offset_reserved = tcp_data[4]
    flags = tcp_data[5]
    window = tcp_data[6]
    checksum = tcp_data[7]
    urgent_pointer = tcp_data[8]

    # Identify and handle SYN packets
    # flags = tcp_data[5]
    # if flags & 2:  # SYN flag set
    #     handle_syn(data, addr[0], tcp_data[0])
    #     continue

    # Check if the packet matches the filter criteria
    if dest_port == SERVER_PORT:

        # Extract destination port from data
        forward_port = struct.unpack('!H', data[36:38])[0]

        # Generate new TCP header with server port as source and dynamic port from data
        new_source_port = SERVER_PORT
        new_tcp_header = struct.pack("!HHLLBBH", new_source_port, forward_port, 100, 0, 5 << 4, 2, 0)

        # Combine new header and original data for forwarding
        forwarded_packet = new_tcp_header + data[36:]

        # Send the forwarded packet
        raw_socket.sendto(forwarded_packet, (SERVER_ADDRESS, forward_port))

        # Print confirmation
        print(f"Forwarded packet to {SERVER_ADDRESS}:{forward_port}")

        # Print basic information
        # print("Basic Information: ")
        # print(f"Paquete TCP recibido de {addr}")
        # print(f"Puerto de origen: {source_port}, Puerto de destino: {dest_port}")
        # print(f"Número de secuencia: {sequence_number}, Número de ACK: {ack_number}")
        # print(f"Flags: {flags}, Ventana: {window}, Checksum: {checksum}")
        # print("---------------------------------------------------------")

        # Process the packet
        # print("Received valid packet:", data[36:])
        # process_data(data[36:])
    else:
        # Discard the packet
        print("Ignoring packet coming from: ", source_port)
        print("---------------------------------------------------------")

# Close socket
raw_socket.close()
