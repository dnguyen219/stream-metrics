#!/usr/bin/env python
from scapy.all import *
import dpkt
import argparse
import sys

def printTS(pcapFile, lib):
    if lib == 'scapy':
        packets = rdpcap(pcapFile)
        counter = 0
        for packet in packets:
            # print packet.time
            print str.format('{0:.9f}', packet.time)
            counter += 1
            if counter >= 10:
                break
    elif lib == 'dpkt':
        counter = 0
        with open(pcapFile, 'rb') as f:
            packets = dpkt.pcap.Reader(f)
            for ts, buf in packets:
                print str.format('{0:.9f}', ts)
                counter += 1
                if counter >= 10:
                    break
    else:
        print 'The requested lib is not supported.'

def main():
    parser = argparse.ArgumentParser(description='PCAP Timestamp Diagnostic')
    parser.add_argument('pcap', help='PCAP file to dump')
    parser.add_argument('-l', '--lib', default='dpkt', help='lib to use: scapy or dpkt (if not supplied, default to dpkt)')
    arguments = parser.parse_args(sys.argv[1:])

    printTS(arguments.pcap, arguments.lib)

    return 0

if __name__ == '__main__':
    sys.exit(main())
