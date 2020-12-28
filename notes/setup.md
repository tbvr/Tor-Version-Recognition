# Tor traffic Crawler setup

## VM Setup

- aws ec2 
- subnet us-east-1b

```
$ git clone https://github.com/jimmychang851129/NSLAB_WebFingerprint.git
$ sudo apt update
$ sudo apt install -y python3-pip xvfb x11-utils firefox
$ sudo apt install -y chromium-chromedriver chromium-browser
$ pip3 install -r requirements.txt
``` 

## TCPdump setup

1. turn off optimization of tcpdump(LRO,gro)

```
$ sudo ethtool -K <interface> tx off rx off tso off gso off gro off lro off
$ sudo ifconfig eth0 mtu 1500
$ sudo ethtool -k eth0
```

2. [set permssion of tcpdump for non-root user](https://www.linuxtutorial.co.uk/tcpdump-eth0-you-dont-have-permission-to-capture-on-that-device/)

## Download driver / browser / tor browser


- [tor version](https://archive.archlinux.org/packages/t/tor/)

- [tor browser archive](https://archive.torproject.org/tor-package-archive/torbrowser/)

- download geckodriver, set permission to 700, and place it in /usr/local/bin/

- move profile.default to directory <working dir>/torbrowser/Browser/TorBrowser/Data/Browser/

- [Tor Browser config](https://drive.google.com/open?id=1GV3ioVL78vw4-2GekGTAF8VfVDgoWal6)

## Code setup

After cloning the repository:

```
$ cd NSLAB_WebFingerprint
$ vim Config.py    # setup configuration
$ mkdir result/ logs/  # store traffic result & logfile, not necessary to have these directories, setup your own directory in Config.py
$ download tor browser config above and put it in the directory <working dir>/torbrowser/Browser/TorBrowser/Data/Browser/
```
