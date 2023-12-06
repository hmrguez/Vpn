import socket
import struct

# Crear un socket raw
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# Direcciones IP
source_ip = '127.0.0.1'  # Cambia estas direcciones por las correctas
dest_ip = '127.0.0.1'

# Construir el encabezado IP
ip_version = 4
ip_ihl = 5
ip_ttl = 255
ip_protocol = socket.IPPROTO_TCP
ip_tot_len = 20 + 20  # Tamaño del encabezado IP + Tamaño del encabezado TCP

ip_header = struct.pack('!BBHHHBBH4s4s', (ip_version << 4) + ip_ihl, 0, ip_tot_len, 0, 0, ip_ttl, ip_protocol, 0, socket.inet_aton(source_ip), socket.inet_aton(dest_ip))

# Construir el encabezado TCP
tcp_source = 1234  # Puerto origen
tcp_dest = 80  # Puerto destino
tcp_seq = 1000
tcp_ack_seq = 0
tcp_offset_res = (5 << 4)
tcp_flags = 2  # Flags SYN
tcp_window = socket.htons(5840)
tcp_check = 0
tcp_urg_ptr = 0

tcp_header = struct.pack('!HHLLBBHHH', tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)

# Pseudo encabezado para el checksum
source_address = socket.inet_aton(source_ip)
dest_address = socket.inet_aton(dest_ip)
placeholder = 0
protocol = socket.IPPROTO_TCP
tcp_length = len(tcp_header)

pseudo_header = struct.pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length)
pseudo_header_checksum = 0

# Calcular el checksum
packet_for_checksum = pseudo_header + tcp_header
for i in range(0, len(packet_for_checksum), 2):
    if i + 1 < len(packet_for_checksum):
        packet_piece = packet_for_checksum[i:i + 2]
        pseudo_header_checksum += int.from_bytes(packet_piece, "big")

pseudo_header_checksum = (pseudo_header_checksum >> 16) + (pseudo_header_checksum & 0xffff)
tcp_checksum = socket.htons(~pseudo_header_checksum & 0xffff)

# Finalmente, enviar el paquete TCP
packet = ip_header + tcp_header
raw_socket.sendto(packet, (dest_ip, 8000))