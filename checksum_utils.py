import socket
import struct


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