import socket
import struct

# Crear un socket raw
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
raw_socket.bind(('localhost', 8000))  # Enlazar el socket a una dirección y puerto

while True:
    # Recibir datos
    data, addr = raw_socket.recvfrom(65535)  # Tamaño máximo del paquete
    ip_header = data[:20]  # Tamaño del encabezado IP
    tcp_header = data[20:40]  # Tamaño del encabezado TCP

    # Desempaquetar la cabecera TCP para obtener información básica
    tcp_data = struct.unpack('!HHLLBBHHH', tcp_header)
    source_port = tcp_data[0]
    dest_port = tcp_data[1]
    sequence_number = tcp_data[2]
    ack_number = tcp_data[3]
    data_offset_reserved = tcp_data[4]
    flags = tcp_data[5]
    window = tcp_data[6]
    checksum = tcp_data[7]
    urgent_pointer = tcp_data[8]

    print(f"Paquete TCP recibido de {addr}")
    print(f"Puerto de origen: {source_port}, Puerto de destino: {dest_port}")
    print(f"Número de secuencia: {sequence_number}, Número de ACK: {ack_number}")
    print(f"Flags: {flags}, Ventana: {window}, Checksum: {checksum}")
    print("Datos del paquete TCP:", data[40:])  # Datos TCP
