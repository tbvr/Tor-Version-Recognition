# NSLab Website fingerprinting

## Documentation & Powerpoint

- [hackmd documentation_Chinese](https://hackmd.io/57c2BCj0TSqA424JlY9zyw)
- [ppt](https://docs.google.com/presentation/d/1JYm6kk1WkFmGZexQORxVfmwa4IdQnHttFaI9hay8A6w/edit?usp=sharing)
- [waseda seminar ppt](https://docs.google.com/presentation/d/1DAyRV6h8sglhRhNuaWm1_xVeYTmfW_Dmq_DuHtfQAAw/edit?usp=sharing)
- [information theory ppt](https://docs.google.com/presentation/d/1LK_YZ2rV8j4J_sTv3hgr2Cjklszna6TY5T6m_5KUeQQ/edit?usp=sharing)

## Objective 

1. Summarize attack / defense techniques in Website Fingerprinting
2. Evaluate recent attacks on the assumption mentioned [in this paper](https://drive.google.com/file/d/1yz4pwJ_eD4OkfK4d459VgN1wwYjS5pqX/view?usp=sharing)
3. Analyze the effectiveness of WF attack for cross-browser dataset and explain the result
	- Browser version 7,8,9
4. Come up with a measurement / evaluation regarding info leaks for tor browser version, thus providing a new metrics other than classification accuracy for security level of tor browser version regarding WF attack or all other possible attack.
5. Browser version Classifier as a recon
	- Train a browser version classifier to notice the version of the tor browser, together with CVE report on the tor browser version, there may be some potential threat.

For more details, please refer to this [slides](https://docs.google.com/presentation/d/10pt0KTaYPd-poWew-QcRuBt8WwrbE0jgYhjkEpeT8Xk/edit?usp=sharing)

### Data Collection / Parsing Methodology

[Improved Website Fingerprinting on Tor](https://drive.google.com/open?id=1NdSn-r8jD3IBJuMOa-gZtWm0ftHVDLXl)

### Preprocessing

- remove Chinese websites(cannot be visited through tor)
- remove all google.com except one(too many google.com on the list, which is basically same sites but in different language)
- remove some websites that are not accessible through tor(apple-dns.com, google-usercontent.com,microsoftoneline.com and etc)
- remove websites that have less than 100 of packets transmitted for all traces in hte dataset

Traffic instance:
- For every domain, remove traffic instance if the amount of packets transmitted(Num_Packet) are less than (median of Num_Packet among all instances) * 0.8 of the webpages


### Dataset 202004

[traffic & extracted features for tbb 9.0.2](https://drive.google.com/drive/folders/1CfmR0964r3pcZvKqelhCwvrYAkgfRNfx?usp=sharing)

[dan.me.uk](https://www.dan.me.uk/torlist/) - A page containing a full TOR nodelist.

Data/ directory:
- TrancoWebList.csv: top 200 websites(closed-world evaluation)
- OpenWorld_WebList.csv: top 6950 websites, discarding duplicate sites from closed-world dataset

For the WebList: Top 250 -> Top 187 sites(after preprocessing)

### Dataset 202006

Dataset of torbrowser 9.0.2, 8.0.6, 7.5.2<br />
This three torbrowser versions are released around the same month each year(so each tor browser version I selected is released a year after the former one)

[link to Dataset](https://drive.google.com/drive/folders/1Y-mGf0IOP0FpwSOGwfAJcBcAaBUuvs7o?usp=sharing)

## Environment
- geckodriver: 0.23.0
- tor-browser: 9.0.4(latest version on torporject webpage)
- tbselenium
- xvfb
- ChromeDriver 80.0.3987.163
- Chromium 80.0.3987.163

| tbb version | geckodriver version | 
| -------- | -------- |
| 7.5.2     | 0.17.0     | 
| 8.0.6     | 0.23.0     | 
| 9.0.2     | 0.23.0     | 

[firefox & geckodriver & selenium version support](https://firefox-source-docs.mozilla.org/testing/geckodriver/Support.html)


## Integration

Integration of crawler and pcapParser.
Simply run crawler and we will store the extracted pcap file in tar.gz form in rawTraffic directory
the extracted pcap file contains only header of the ip address(no encrypted payload).
Each traffic instance for a single site will be in csv form. Therefore, when finishing executing the crawler and uncompress the tar.gz file in rawTrafficdir, there will be 200 directories in rawTraffic directory, each stands for one website, for each website directory, there will be 4 csv file, each is he extracted traffic instances of the websites.

- rawTraffic
	- 1: stands for the round of crawler execution(sequentially increase)
		- 1_traces.tar.gz
			- 200directory: each stands for a website
				- 4-8csv file: each stands for an extracted traffic instance
		- log.txt: output log of the crawler
		- ErrorList.txt: websites failed to crawled
		- StreamInfo.txt: record opended stream for every visit


## Setup

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

refer to CellFeature.py and TimeFeature.py

## Visualization & training

### [TrafficResult-3](https://drive.google.com/open?id=1R7ZqTzOGg9bWMqB2kXvWoJQHLJJEZCjq)
1. Remove Websites which has a median of packetNum less than 100
2. Remove traffic instance that has 20% less packetNum comparing with the median of packetNum in the websites
3. Remove websites that has less than n_threshold traffic instances left
4. Around 175 sites left

### TorBrowser Version Accuracy result

#### Random Forrest

| Training Ver.  \ Testing Ver. | 7.5.2       | 8.0.6       | 9.0.2       |
| ----------------------------- | ----------- | ----------- | ----------- |
| 7.5.2                         | 0.84 / 0.73 | 0.053189    | 0.305637    |
| 8.0.6                         | 0.039714    | 0.75 / 0.69 | 0.045313    |
| 9.0.2                         | 0.294561    | 0.055094    | 0.85 / 0.85(val acc/test acc) |

Not found Domain:

| train ver \ test ver | 7.5.2 | 8.0.6 | 9.0.2 |
| -------------------- | ----- | ----- | ----- |
| 7.5.2                |   | 19    | 5     |
| 8.0.6                | 1     |   | 0     |
| 9.0.2                | 4     | 17    |       |

### Top 9 Important Features in version classifier

Train Version classifier for each webpage, extract top 10 important features for all these 200 version classifier. Finally, record how many times each feature appears in the important features in each version classifier. The 10th feature only appear 45 times among all the version classifier.

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

## Version Classifier

To have deeper understanding on the results above(WF attack failure in cross-version training and testing). We train a browser version classifier, given a traffic instance, classify which browser version it belongs to.

accuracy: 88%

Browser version classifier, train a traffic collected from each single domain with different browser version and test it on the same domain.

accuracy: [google sheet link](https://docs.google.com/spreadsheets/d/1FPNCdpcd_JAUvXhr22fgHUG4c3Anohl3Q5HaLZLbZdc/edit?usp=sharing)

## Two-phase Classifier

### Target

We try to take difference in browser version into account, dataset will be traffic coming from different browser version.

Train a 2-phase classifier, such that given a traffic
- random forrest for browser version recognition
- Deep Fingerprint for Website recognition

Given dataset of traffic from different browser verseion, try to compare our 2-phase classifier with Deep fingerprint.

### Dataset

version 7, 8, 9

Total Accuracy

### Methodology

#### Extract traffic features from raw traffic

raw traffic contains all the packet header of traffic, in csv file format

```
$ python3 two-phase-classifier.py -e -i <rawdata/7> -o <twophase/>
$ python3 two-phase-classifier.py -e -i <rawdata/8> -o <twophase/>
$ python3 two-phase-classifier.py -e -i <rawdata/9> -o <twophase/>
```

### Remove Failed Samples

```
$ python3 two-phase-classifier.py -r -i <twophase/> -o <twophase/>
```

### Train_Test_Split

```
python3 two-phase-classifier.py -i <twophase/> -o <twophase/> -s
```

### train version classifer(random forest)

```
$ python3 two-phase-classifier.py -b -i <twophase/rf/train_test/> -o <twophase/versionclassifier/>
```

### Train 2-phase DF model

```
$ python3 two-phase-classifier.py -i </twophase/df/train_test/> -o </twophase/df/train_test/7> -v 7  -d
$ python3 two-phase-classifier.py -i </twophase/df/train_test/> -o </twophase/df/train_test/8> -v 8  -d
$ python3 two-phase-classifier.py -i </twophase/df/train_test/> -o </twophase/df/train_test/9> -v 9  -d
```

### Train DF model with whole dataset(for comparison)

```
$ python3 two-phase-classifier.py -i <twophase/df/train_test> -o <twophase/df/train_test/cmpdfmodel/> -d -a
```

### Result

- 2-phase classifier
    - random forest for version classifier: 0.88
    - DF for further website recognition:  0.83
- DF model with whole dataset(for cmp)

## Tor documents
https://2019.www.torproject.org/projects/torbrowser/design/#idm29

This documents elaborate the design of Tor. It will clarify why we use geckodriver for tor browser.
Also, if there is more details about tor on this webpage.

## Statistical Analysis

anova + Tukey-HSD

```
Test all domains
$ python3 anova.py -i <dir to removeFailed_with_burst> -f <dir to dir to important feature(browsercmp)> -a

Test selected domains
$ python3 anova.py -i <dir to removeFailed_with_burst> -f <dir to dir to important feature(browsercmp)>
```