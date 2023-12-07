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
SERVER_PORT = 7000
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
raw_socket.bind(('localhost', SERVER_PORT))

connection_states = {}

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
    if flags & 2 and dest_port == SERVER_PORT:  # SYN flag set
        handle_syn(data, addr[0], tcp_data[0])
        continue

    # Check if the packet matches the filter criteria
    if dest_port == SERVER_PORT:

        # Print basic information
        print("Basic Information: ")
        print(f"Paquete TCP recibido de {addr}")
        print(f"Puerto de origen: {source_port}, Puerto de destino: {dest_port}")
        print(f"Número de secuencia: {sequence_number}, Número de ACK: {ack_number}")
        print(f"Flags: {flags}, Ventana: {window}, Checksum: {checksum}")
        print("---------------------------------------------------------")

        # Process the packet
        print("Received valid packet:", data[38:])
        process_data(data[38:])
    else:
        # Discard the packet
        print("Ignoring packet coming from: ", source_port)
        print("---------------------------------------------------------")

# Close socket
raw_socket.close()
