#!/usr/bin/python

import socket
from scapy.all import Ether, IP, UDP, Raw
 
'''class RawUdpTarget(UdpTarget):
 
    def _prepare_socket(self):
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
        self.socket.bind((self._interface, 0))
 
    def _send_to_target(self, data):
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')
        ip = IP(src=self.host, dst='255.255.255.255')
        udp = UDP(sport=68, dport=self.port)
        payload = Raw(load=data)
        packet = str(ether / ip / udp / payload)
        self.logger.debug('Sending header+data to host: %s:%d' % (self.host, self.port))
        self.socket.send(packet)
        self.logger.debug('Header+data sent to host')
'''

def _send_to_(data):
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    ip = IP(src='1.1.1.1', dst='255.255.255.255')
    udp = UDP(sport=68, dport=69)
    payload = Raw(load=data)
    packet = str(ether / ip / udp / payload)
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sock.bind(('eth0', 0))
    sock.send(packet)

_send_to_("kalyan")
