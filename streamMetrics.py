#!/usr/bin/env python
import dpkt
from stream import ProfessionalMediaStream
import argparse
import sys
import numpy

def writeHistogramToConsole(hist, bin_edges):
    bucketIdx = 0
    while bucketIdx < len(hist):
        axis = "[{0:.2f},{1:.2f})".format(bin_edges[bucketIdx], bin_edges[bucketIdx+1])
        print axis + "={0}".format(hist[bucketIdx])
        bucketIdx += 1

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
    print '95th percentile (find outliers, in us)={0:.2f}'.format(numpy.percentile(a, 95))
    print '95th percentile (find outliers, in us)={0:.2f}'.format(numpy.percentile(a, 99))
    print 'Max interval over file (in us)={0:.2f}'.format(numpy.amax(a))

    print "\n= Packet Interval Numerical Histogram (in us) ="
    hist, bin_edges = numpy.histogram(a, 10)
    writeHistogramToConsole(hist, bin_edges)

    print "\n= Packet Interval Pictogram (in us) ="
    print "Width: {0:.2f}".format(bin_edges[1] - bin_edges[0])
    # writePictogramToConsole(hist, bin_edges)

    print "\n= ST 2110-21 ="
    print "Octets to capture the active picture area={:.2f}".format(strm.activeOctets())
    print "Number of packets per frame of video, N_pkts={:.2f}".format(strm.NPackets())
    print "Period between consecutive frames of video, T_FRAME (in s)={:.2e}".format(strm.TFrame())
    print "Sender Type={}".format(strm.senderType)

    print "\n= Network Compatibility Model Compliance ="
    print "Scaled period between packets draining, T_DRAIN (in s)={:.2e}".format(strm.TDrain(strm.getBeta()))
    print "Scaling factor, Beta={:.2f}".format(strm.getBeta())
    print "Spec. C_MAX (left part)={:.2f}".format(strm.CMaxSpecLeft())
    print "Spec. C_MAX (right part)={:.2f}".format(strm.CMaxSpecRight())
    print "Spec. C_MAX={:.2f}".format(strm.CMaxSpec())
    print "Obs. C_MAX={:.2f}".format(strm.getNetCompatBucketMaxDepth())

    isNCCompliant = ""
    if strm.getNetCompatBucketMaxDepth() > strm.CMaxSpecLeft() and strm.getNetCompatBucketMaxDepth() > strm.CMaxSpecRight():
        isNCComplied = "NOT "
    print "Stream does {}comply with the Network Compatibility Model of ST 2110-21\n".format(isNCCompliant)

    print "= Virtual Receiver Buffer Model Compliance ="
    print "Unscaled period between packets draining, T_DRAIN (in s)={:.2e}".format(strm.TDrain(1.0))
    print "Spec. VRX_FULL (left part)={:.2f}".format(strm.VrxFullSpecLeft())
    print "Spec. VRX_FULL (right part)={:.2f}".format(strm.VrxFullSpecRight())
    print "Spec. VRX_FULL={:.2f}".format(strm.VrxFullSpec())
    print "Obs. Min VRX_FULL={:.2f}".format(strm.getVirtRecvBuffBucketMinDepth())
    print "Obs. Max VRX_FULL={:.2f}".format(strm.getVirtRecvBuffBucketMaxDepth())
    virtRecvBufferBucketRange = strm.getVirtRecvBuffBucketMaxDepth() - strm.getVirtRecvBuffBucketMinDepth()
    print "Obs. Range VRX_FULL={:.2f}".format(virtRecvBufferBucketRange)

    isVCBCompliant = ""
    if virtRecvBufferBucketRange > strm.VrxFullSpecLeft() and virtRecvBufferBucketRange > strm.VrxFullSpecRight():
        isVCBComplied = "NOT "
    print "Stream does {}comply with the Virtual Receive Buffer Model of ST 2110-21\n".format(isVCBCompliant)

    print "Receiver to start rendering after receiving {:.0f} packets.\n".format(strm.getVirtRecvBuffBucketMaxDepth() - strm.getVirtRecvBuffBucketMinDepth())

    return 0

if __name__ == '__main__':
    sys.exit(main())
