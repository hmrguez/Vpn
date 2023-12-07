from scapy.all import *
from scapy.layers.inet import IP, TCP


def server(port):
    # Create raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    while True:
        # Receive data
        data, addr = sock.recvfrom(65535)

        # Parse received packet
        ip = IP(data)
        tcp = TCP(data[IP().len:])

        # Check if SYN flag is set
        if tcp.flags & 0x02:
            # Send SYN-ACK
            synack = TCP(sport=port, dport=tcp.sport,
                         flags="SA", seq=100, ack=tcp.seq + 1, window=8192)
            send(IP(dst=ip.src, src=ip.dst) / synack)

            # Receive ACK
            data, addr = sock.recvfrom(65535)
            ip = IP(data)
            tcp = TCP(data[IP().len:])

            # Check if ACK flag is set
            if tcp.flags & 0x10:
                print(f"Connection established with {addr[0]}")
                # ... Implement communication logic here ...
        else:
            print(f"Received unknown packet from {addr[0]}")


# Run server on port 12345
server(12345)
