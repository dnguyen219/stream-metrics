#!/usr/bin/env python
import math, re
import sys

class ProfessionalMediaStream:
    global RTP_PAYLOAD, __lastTicks, deltas, __netCompatBucketDepth, netCompatBucketMaxDepth, __virtRecvBuffBucketDepth, virtRecvBuffBucketMaxDepth, virtRecvBuffBucketMinDepth, beta

    RTP_PAYLOAD = 1428 #per ST 2110
    __MAX_IP = 1500
    __lastTicks = 0.0
    deltas = []
    __netCompatBucketDepth = 0.0 #Must be a float to handle continuous time
    netCompatBucketMaxDepth = 0
    __virtRecvBuffBucketDepth = 0.0 #Must be a float to handle continuous time
    virtRecvBuffBucketMaxDepth = 0
    virtRecvBuffBucketMinDepth = 0

    # Ratio of active time to total time within the frame period
    rActive = 1.0
    senderType = "2110TPW"
    beta = 1.1

    def __init__(self, activeWidth, activeHeight, rate, interlaced, colorSubsampling, sampleWidth, senderType):
        self.activeWidth = activeWidth
        self.activeHeight = activeHeight
        self.rate = rate
        self.interlaced = interlaced
        self.colorSubsampling = colorSubsampling
        self.sampleWidth = sampleWidth
        self.senderType = senderType

    # Only handles 8, 10, 12, 16 sampleWidths for 4:2:2 and 4:4:4
    def pGroupOctets(self):
        octets = self.sampleWidth / 2
        if self.colorSubsampling == "4:4:4":
            if self.sampleWidth == 12:
                octets = 9
            else: #self.sampleWidth = 16
                octets = 6
        return octets

    # Only handles 8, 10, 12, 16 sampleWidths for 4:2:2 and 4:4:4
    def pGroupPixels(self):
        pixels = 2
        if self.colorSubsampling == "4:4:4":
            if self.sampleWidth == 12:
                pixels = 1
        return pixels

    # Number of octets to capture the active picture area
    def activeOctets(self):
        return self.activeWidth * self.activeHeight * self.pGroupOctets() / self.pGroupPixels()

    # Number of packets per frame of video (depends on mapping details)
    def NPackets(self):
        return math.ceil(self.activeOctets() * 1.0 / RTP_PAYLOAD)

    # Period between consecutive frames of video at the prevailing frame rate
    def TFrame(self):
        effRate = self.rate
        if self.interlaced:
            effRate = self.rate / 2
        return 1 / effRate

    def TDrain(self, scaler):
        return (self.TFrame() / self.NPackets() / scaler)

    def CMaxSpecLeft(self):
        if self.senderType == "2110TPW":
            return 16
        else:
            return 4

    def CMaxSpecRight(self):
        ret = 0
        if self.senderType == "2110TPN":
            ret = self.NPackets() / (43200 * rActive * self.TFrame())
        elif self.senderType == "2110TPNL":
            ret = self.NPackets() / (43200 * self.TFrame())
        else:
            ret = self.NPackets() / (21600 * self.TFrame())
        return ret

    def CMaxSpec(self):
        return max(self.CMaxSpecLeft(), self.CMaxSpecRight())

    def VrxFullSpecLeft(self):
        ret = 0
        if re.match("^2110TPN", self.senderType):
            ret = (1500 * 8) / __MAX_IP
        else: #2110TPW
            ret = (1500 * 720) / __MAX_IP
        return ret

    def VrxFullSpecRight(self):
        ret = 0
        if re.match("^2110TPN", self.senderType):
            ret = self.NPackets() / (27000 * self.TFrame())
        else: #2110TPW
            ret = self.NPackets() / (300 * self.TFrame())
        return ret

    def VrxFullSpec(self):
        return max(math.floor(self.VrxFullSpecLeft()), math.floor(self.VrxFullSpecRight()))

    def packetEvent(self, ticks):
        global __lastTicks, deltas, __netCompatBucketDepth, netCompatBucketMaxDepth, __virtRecvBuffBucketDepth, virtRecvBuffBucketMaxDepth, virtRecvBuffBucketMinDepth
        if __lastTicks > 0:
            # deltas converted from ticks (0.1 us) to micro-seconds
            # deltas.append((ticks - __lastTicks) / 10)
            deltas.append((ticks - __lastTicks) * 1000000.0)
        if self.rate and self.activeHeight and self.activeWidth and self.colorSubsampling and self.interlaced and self.sampleWidth:
            if __lastTicks > 0:
                netCompatPacketsDrained = ((ticks - __lastTicks) / 10000000.0) / self.TDrain(beta)
                __netCompatBucketDepth -= netCompatPacketsDrained
            if __netCompatBucketDepth < 0:
                __netCompatBucketDepth = 0

            __netCompatBucketDepth += 1

            if __netCompatBucketDepth > netCompatBucketMaxDepth:
                netCompatBucketMaxDepth = math.ceil(__netCompatBucketDepth)

            virtRecvBuffPacketsDrained = ((ticks - __lastTicks) / 10000000.0) / self.TDrain(1.0)
            __virtRecvBuffBucketDepth -= virtRecvBuffPacketsDrained

            __virtRecvBuffBucketDepth += 1
            if __virtRecvBuffBucketDepth < virtRecvBuffBucketMinDepth:
                virtRecvBuffBucketMinDepth = math.floor(__virtRecvBuffBucketDepth)
            if __virtRecvBuffBucketDepth > virtRecvBuffBucketMaxDepth:
                virtRecvBuffBucketMaxDepth = math.ceil(__virtRecvBuffBucketDepth)

        __lastTicks = ticks

    def getDeltas(self):
        return deltas
