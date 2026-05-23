"""
Packet sniffer on local network interface - prints decoded data.
"""

from scapy.all import sniff

def packet_callback(packet):
    if packet.haslayer("Raw"):
        print(packet["Raw"].load.decode(errors="ignore"))

sniff(filter="tcp port 80", prn=packet_callback, store= 0)