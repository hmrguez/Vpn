# VPN Project Documentation

## Overview

This project is a simple implementation of a VPN (Virtual Private Network) using Python. It consists of a client, a server, and a VPN that acts as a middleman. The client sends packets in the form of UDP datagrams to the VPN, which then forwards them to the server. The VPN can also restrict certain users and VLANs from accessing the server.

## Files

The project consists of the following files:

- `client.py`: This file contains the code for the client that sends packets to the VPN.
- `server.py`: This file contains the code for the server that receives packets from the VPN.
- `vpn.py`: This file contains the code for the VPN that forwards packets from the client to the server.
- `vpn_cli.py`: This file provides a command-line interface (CLI) for controlling the VPN.
- `checksum_utils.py`: This file contains utility functions for calculating UDP checksums.
- `utils.py`: This file contains utility functions for assigning IP addresses and ports to users.

## Modules

### `client.py`

The client creates a raw socket and sends a UDP packet to the VPN. The packet contains a message and the real destination port. The client calculates the UDP checksum and includes it in the UDP header.

### `server.py`

The server creates a raw socket and listens for incoming packets. When it receives a packet, it unpacks the UDP header and checks the checksum. If the checksum is valid, it processes the packet. Otherwise, it discards the packet.

### `vpn.py`

The VPN creates a raw socket and listens for incoming packets. When it receives a packet, it validates the user and checks the checksum. If the user is valid and the checksum is correct, it forwards the packet to the server. Otherwise, it discards the packet.

The VPN can also restrict certain users and VLANs. Restricted users are identified by their port, and restricted VLANs are identified by their VLAN ID.

### `vpn_cli.py`

The VPN CLI provides a command-line interface for controlling the VPN. It supports the following commands:

- `start`: Starts the VPN.
- `stop`: Stops the VPN.
- `create_user <username> <password> <vlan_id>`: Creates a user with the given username, password, and VLAN ID. The user is assigned a random IP address and port.
- `restrict_user <port>`: Restricts the user with the given port.
- `restrict_vlan <vlan_id>`: Restricts the VLAN with the given VLAN ID.

### `checksum_utils.py`

This module contains two functions:

- `udp_checksum(source_ip, dest_ip, udp_packet)`: Calculates the UDP checksum for a packet.
- `calc_checksum(packet)`: Calculates the checksum for a packet.

### `utils.py`

This module contains the `assign_ip_address` function, which assigns a random IP address and port to a user.

## Usage

To use this project, follow these steps:

1. Start the VPN by running `vpn_cli.py` and entering the `start` command.
2. Create a user by entering the `create_user <username> <password> <vlan_id>` command.
3. Run `client.py` to send a packet to the VPN.
4. Run `server.py` to receive the packet from the VPN.

You can restrict users and VLANs by entering the `restrict_user <port>` and `restrict_vlan <vlan_id>` commands in the VPN CLI.

To stop the VPN, enter the `stop` command in the VPN CLI.

## Dependencies

This project requires Python 3 and the following Python libraries:

- `socket`
- `struct`
- `random`

## Understanding UDP

User Datagram Protocol (UDP) is one of the core protocols of the Internet protocol suite. It is a simple, connectionless protocol that does not guarantee delivery, ordering, or error checking of data. This means that UDP does not establish a connection before sending data, does not ensure that the data is received, and does not ensure that the data is received in the same order it was sent.

Despite these limitations, UDP is used in this project for its simplicity and speed. Because UDP does not have the overhead of establishing a connection, ensuring delivery, and ensuring ordering, it is faster and simpler than connection-oriented protocols like TCP (Transmission Control Protocol). This makes UDP suitable for applications where speed is more important than reliability, such as streaming audio and video.

## UDP Datagram

A UDP datagram is composed of a header and data. The UDP header is 8 bytes long and consists of the following fields:

- Source Port (2 bytes): This is the port number of the application on the host sending the datagram.
- Destination Port (2 bytes): This is the port number of the application on the host receiving the datagram.
- Length (2 bytes): This is the length in bytes of the entire datagram (header and data).
- Checksum (2 bytes): This is used for error-checking of the header and data, simple error checking, meaning that packets that are detected as flawed ones just get discarded, "Fire and Forget", let layer 5 worry about it.

The data follows the header and contains the payload of the datagram.

## Important Details

- Because UDP is a connectionless protocol, it does not establish a connection before sending data. This means that UDP does not have a three-way handshake like TCP.
- UDP does not ensure that the data is received. This means that UDP does not have acknowledgements (ACKs) or negative acknowledgements (NACKs) like TCP.
- UDP does not ensure that the data is received in the same order it was sent. This means that UDP does not have sequence numbers like TCP.
- The simplicity and speed of UDP come at the cost of reliability. Applications that use UDP must be able to handle lost, duplicate, and out-of-order packets.
- Despite its limitations, UDP is used in many important Internet protocols, including DNS (Domain Name System), DHCP (Dynamic Host Configuration Protocol), and RTP (Real-time Transport Protocol).

## References

- [Practical Networking Youtube](https://www.youtube.com/@PracticalNetworking): the main source for information about the transport layer protocols.