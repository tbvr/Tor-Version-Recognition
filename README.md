# Tor Browser Version Reconnaissance via Network Traffic Analysis

## Objective

- Verify that TBB version will affect a website's network traffic
- TBVR attack implementation
- Two-Phase Classifier(An enhancement of WF attack)
- Identify why different TBB versions have distinguishable traffic features


## Dataset

- [Closed-world Dataset](https://drive.google.com/drive/folders/1qz2o_uiTIlb7WDMwo6NLn98oN7jh78Yb?usp=sharing)
- [Open-world Dataset](https://drive.google.com/drive/folders/1G_hM03ymfxYwEMliwwfJVa1wHWRjGIvr?usp=sharing)
- [Configuration Dataset](https://drive.google.com/drive/folders/1ZZEbHMgunu1lXhMTlvVVN-vxnauZxhv6?usp=sharing)

## Crawler Setup

### Docker

```
$ change Config.py(torbrowser directory to either torbrowser_902 | torbrowser_806 | torbrowser_752)
$ change Dockerfile, change argument of setup.sh to the specific torbrowser version
$ docker build -t <imageName> .
$ ./run.sh <image_name> <container_name> <outputdir>(volume)
```

## Feature Exctraction

```
$ python3 FeatureExtract.py -t 	# for testing(need to change the default config setting in the code)

$ python3 FeatureExtract.py -i <TrafficDir> -o <outputdir>

<TrafficDir>: in csv form(the output of pcapParser)
```

### FeatureList

refer to ml/FeatureExtract.py

## Visualization & training

### Top 9 Important Features in version classifier

```
Num_Packet 173
avg_outgoing_packetOrder 172
Num_incoming_packet 172
std_incoming_packetOrder 169
avg_incoming_packetOrder 167
incoming_ratio 164
outgoing_ratio 163
std_outgoing_packetOrder 155
Num_outgoinging_packet 146
```

### Version Classifier(Random Forest based)

```
$ cd ml
$ python3 browserClassifier.py -i <filepath to extracted feature(in csv format) -o <output filepath>
```
