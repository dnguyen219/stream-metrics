#!/usr/bin/env python
import dpkt
from stream import ProfessionalMediaStream
import argparse
import sys
import numpy

def main():
    parser = argparse.ArgumentParser(description='Stream Metrics')
    parser.add_argument('pcap', help='PCAP file to dump')
    parser.add_argument('--activeWidth', default=1920)
    parser.add_argument('--activeHeight', default=1080)
    parser.add_argument('--rate', default=59.94, help='field-rate for interlaced, frame-rate for progressive')
    parser.add_argument('--interlaced', default=True)
    parser.add_argument('--colorSubsampling', default='4:2:2')
    parser.add_argument('--sampleWidth', default=10)
    parser.add_argument('--senderType', default='2110TPW', help='2110TPN, 2110TPNL, 2110TPW')
    parser.add_argument('--rtpPayload', default=1428)
    arguments = parser.parse_args(sys.argv[1:])
    pcapFile = arguments.pcap

    strm = ProfessionalMediaStream(arguments.activeWidth, arguments.activeHeight, arguments.rate, arguments.interlaced, arguments.colorSubsampling, arguments.sampleWidth, arguments.senderType)
    strm.rtpPayload = arguments.rtpPayload

    #use dpkt
    with open(pcapFile, 'rb') as f:
        print '= StreamMetrics =\n'
        print 'Reading: {}'.format(pcapFile)
        packets = dpkt.pcap.Reader(f)
        for ts, buf in packets:
            # print str.format('{0:.9f}', ts)
            strm.packetEvent(ts)

    strm.deltas = strm.getDeltas()
    print 'Read {} packets\n'.format(len(strm.deltas) + 1)
    print '= Summary Statistics ='
    a = numpy.array(strm.deltas)
    print 'Min interval over file (in us)={0:.2f}'.format(numpy.amin(a))
    print '1st percentile (find outliers, in us)={0:.2f}'.format(numpy.percentile(a, 1))
    print '5th percentile (find outliers, in us)={0:.2f}'.format(numpy.percentile(a, 5))
    print 'Median (50th percentile, in us)={0:.2f}'.format(numpy.median(a))
    print 'Average packet interval (in us)={0:.2f}'.format(numpy.mean(a))
    print 'Packet interval standard dev. (in us)={0:.2f}'.format(numpy.std(a))

    return 0

if __name__ == '__main__':
    sys.exit(main())
