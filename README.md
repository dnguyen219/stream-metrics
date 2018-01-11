# stream-metrics
CLI program to derive SMPTE ST 2110 metrics from input .pcap files. This is the python version of the original [StreamMetrics](https://github.com/andrewburnheimer/StreamMetrics). The enhancement is the ability to process nanosecond .pcap files.

## License

The user of this software is free to use it for any purpose, to distribute it,
to modify it, and to distribute modified versions of the software, under the
terms of the *Apache License 2.0* contained in LICENSE.txt, without concern for
royalties.


## Pre-Requisites

* Python 2.7


## Installation

1. Clone this repository to your local machine.

2. Run `pip install -r requirements.txt` to install dependencies.


## Usage

```
usage: streammetrics [-h] [--activeWidth ACTIVEWIDTH]
                     [--activeHeight ACTIVEHEIGHT] [--rate RATE]
                     [--interlaced INTERLACED]
                     [--colorSubsampling COLORSUBSAMPLING]
                     [--sampleWidth SAMPLEWIDTH] [--senderType SENDERTYPE]
                     [--rtpPayload RTPPAYLOAD] [-l LIB] [-v]
                     pcap

Stream Metrics

positional arguments:
  pcap                  PCAP file to dump

optional arguments:
  -h, --help            show this help message and exit
  --activeWidth ACTIVEWIDTH
                        active width of a frame (default: 1920)
  --activeHeight ACTIVEHEIGHT
                        active height of a frame (default: 1080)
  --rate RATE           field-rate for interlaced, frame-rate for progressive
                        (default: 59.94)
  --interlaced INTERLACED
                        whether frames are interlaced (default: True)
  --colorSubsampling COLORSUBSAMPLING
                        color subsampling (default: 4:2:2)
  --sampleWidth SAMPLEWIDTH
                        sample width (default: 10)
  --senderType SENDERTYPE
                        2110TPN, 2110TPNL, 2110TPW (default: 2110TPW)
  --rtpPayload RTPPAYLOAD
                        RTP payload (default: 1428)
  -l LIB, --lib LIB     lib to use: scapy or dpkt (if not supplied, default to
                        dpkt) (default: dpkt)
  -v, --version         show program's version number and exit
  ```


## Example Results

```
= StreamMetrics 1.0.0 =

Reading: Vendor1.pcap

Read 1442065 packets

= Summary Statistics =
Min interval over file (in us)=0.00
1st percentile (find outliers, in us)=7.00
5th percentile (set standard, in us)=7.00
Median (50th percentile, in us)=9.00
Average packet interval (in us)=9.19
Packet interval standard dev. (in us)=0.55
95th percentile (set standard, in us)=10.00
99th percentile (find outliers, in us)=10.00
Max interval over file (in us)=12.00

= Packet Interval Numerical Histogram =
(0;1.2] = 101
(1.2;2.4] = 81
(2.4;3.6] = 328
(3.6;4.8] = 2800
(4.8;6] = 417
(6;7.2] = 18
(7.2;8.4] = 60301
(8.4;9.6] = 832317
(9.6;10.8] = 232
(10.8;12] = 2752

= Packet Interval Pictogram =
Width: 1.2
(0;1.2]           :
(1.2;2.4]         :
(2.4;3.6]         :
(3.6;4.8]         :
(4.8;6]           :
(6;7.2]           :
(7.2;8.4]         :#########
(8.4;9.6]         :##########################################################
(9.6;10.8]        :
(10.8;12]         :

= ST 2110-21 =
Octets to capture the active picture area=5184000
Number of packets per frame of video, N_pkts=3631
Period between consecutive frames of video, T_FRAME (in s)=3.34E-02
Sender Type=2110TPW

= Network Compatibility Model Compliance =
Scaled period between packets draining, T_DRAIN (in s)=8.35E-06
Scaling factor, Beta=1.10
Spec. C_MAX (left part)=16
Spec. C_MAX (right part)=5.04
Spec. C_MAX=16
Obs. C_MAX=3
Stream does comply with the Network Compatibility Model of ST 2110-21

= Virtual Receiver Buffer Model Compliance =
Unscaled period between packets draining, T_DRAIN (in s)=9.19E-06
Spec. VRX_FULL (left part)=720
Spec. VRX_FULL (right part)=362.74
Spec. VRX_FULL=720
Obs. Min VRX_FULL=-1
Obs. Max VRX_FULL=280
Obs. Range VRX_FULL=281
Stream does comply with the Virtual Receive Buffer Model of ST 2110-21

Receiver to start rendering after receiving 281 packets.
```

## Contribute

Please fork the GitHub project (https://github.com/quarker/stream-metrics),
make any changes, commit and push to GitHub, and submit a pull request.


## Contact

This project was initiated by Dao Nguyen.

* Email:
  * dao_nguyen@comcast.com
* Twitter:
  * @quarker93
* Github:
  * https://github.com/quarker
