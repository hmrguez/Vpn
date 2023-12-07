from scapy.all import *
from scapy.layers.inet import TCP, IP


def client(server_ip, port):
    # Create raw socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    # Generate random source port
    sport = random.randint(1024, 65535)

    # Send SYN packet
    syn = TCP(sport=sport, dport=port, flags="S", seq=1000)
    send(IP(dst=server_ip, src="0.0.0.0") / syn)

    # Receive SYN-ACK
    data, addr = sock.recvfrom(65535)
    ip = IP(data)
    tcp = TCP(data[IP().len:])

    # Check if SYN-ACK flag is set
    if tcp.flags & 0x18:
        # Send ACK
        ack = TCP(sport=sport, dport=port, flags="A", seq=1001, ack=tcp.seq + 1, window=8192)
        send(IP(dst=server_ip, src="0.0.0.0") / ack)
        print(f"Connection established with server {addr[0]}")
        # ... Implement communication logic here ...
    else:
        print(f"Unexpected response from server")


# Connect to server at 192.168.1.100:12345
client("192.168.1.100", 12345)
