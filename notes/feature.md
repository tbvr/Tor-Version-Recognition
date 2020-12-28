# Feature List

List of feature we can try.


## Time-based Feature


### Based on Characterization of Encrypted and VPN Traffic using Time-related
Features

flow definition: consecutive packet with same features
	- srcIP, srcPort
	- dstIP, dstPot

- duration of the active flow
- forward inter Arrival time: time between two packets sent forward direction(mean,min,max,std)
- backword inter Arrival time: ... backward direction(mean,min,max,std)

- Interval Time between each packet 
- bytes per second
- packets per second
- flow bytes per second

### Misc

- traffic burst
- n gram feature

## Packet amount

- first n packet (n could be any number)
- size & direction of each packet
	- size of cell are always 512 bytes
	- + : outgoin, - : incoming
- Number Marker: number of packets sent before the direction changes
- Size Marker: bytes sent before direction changegs (not necessary, fixed size tor cell)
- Total Transmitted packet / bytes
- percentage of incoming packet / outgoing packet

## Misc

- n gram feature