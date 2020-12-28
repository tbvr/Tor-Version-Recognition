# Data collection

Based on : 
- [Improved Website Fingerprinting on Tor(WPES 2013)](https://drive.google.com/open?id=1NdSn-r8jD3IBJuMOa-gZtWm0ftHVDLXl)
- [A Critical Evaluation of Website Fingerprinting Attacks(CCS 2014)](https://drive.google.com/open?id=1yz4pwJ_eD4OkfK4d459VgN1wwYjS5pqX)

## Crawler implementation

### tbselenium

[Source code](https://github.com/webfp/tor-browser-selenium)

we can set up tor, tbb with these package

For the details of the package:

- Utilize stem to launch / control tor

- Inherit selenium to control tor browser driver

#### Config

```lang=c
TorConfig = {
	'SocksPort': str(9250),
	'ControlPort': str(9251),
	'MaxCircuitDirtiness': '600000',
	'UseEntryGuards': '0', # Do not use specific set of tor guard node
	'NumEntryGuards':'1',
	'DataDirectory':tempfile.mkdtemp()
}

```

#### problem

tor proxy will maintain a set of circuit / tor guard node connection
We cannot know which one tor browser select thorugh selenium driver API
It seems to be no API for noticing the selection of tor guard node


### tcpdump

![](https://i.imgur.com/VHK8kC1.png)

We have to disabled offload mechanism in localhost(since the attackers will intercept fully segment packet)

#### Setup

disable optimization

```
$ ethtool -K <interface> tx off rx off tso off gso off gro off lro off
```

set MTU size = 1500

```
$ ifconfig <interface> mtu 1500
```

run subprocess tcpdump locally

```
$ tcpdump -i <interface> tcp -w output.pcap
```

## feature extractrion

### pcap to raw traces(csv file)

packet sent through tor network are well encrypted. An attacker could not retrieve even the packet information sent to the end point.

In our scenario, attacker intercept / eavesdrop packet between the user to the guard node. The header we retrieved are actually the guard node, not the end host. The whole packet are encrypted into a format called cell. Each cell are 500 bytes at most.

Retrieve all the header information in each packet in the pcap file, and save it to csv file.

We would eventually get things like this.

![](https://i.imgur.com/hZbD81n.png)

command:

```
$ python3 pcapParser.py
```

### Feature extraction

Refer to feature.md

1. Remove ACK,FIN,SYN packet
