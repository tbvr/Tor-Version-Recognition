# ML analysis

## Dataset

###  Closed World Dataset of Tor Browser Bundle(TBB) 9

[TrafficResult-3(Links to Google Drive)](https://drive.google.com/open?id=1R7ZqTzOGg9bWMqB2kXvWoJQHLJJEZCjq), This is the dataset we used.

- Top 200 sites from TrancoWebList
- Crawl with tor browser bundle 9.0.2
- After noise removal, Each website has 80-150 traffic instances, 175 websites left

### FYI

- [raw network traffic](https://drive.google.com/open?id=1CfmR0964r3pcZvKqelhCwvrYAkgfRNfx)(output of pcapParser, record every packet headers of the traffic)
- [Noise removal details as mentioned in the third point in Closed World Dataset](https://github.com/jimmychang851129/NSLAB_WebFingerprint/blob/master/meetings/20200521.md)

## Result

| Dataset | Method | Accuracy |
| -------- | -------- | -------- |
| Closed World, tbb 9     | Random Forrest     | 87% - 90%     |

- Feature importance: cell feature(especially order feature) > time-based feature
	- Meaning multi-tab, background noise do have large impact on accuracy
	- Crawler location / user location may not be a important factors in accuracy(time-based feature is not important)

### Visualization of feature distribution

[hist.csv](https://drive.google.com/open?id=1hBkLJ5STDHTR52tE5Px5rd12dI17DB1U6heuhLMWb1A)

We try to plot the distribution of websites according to the features

for every chart:
- x axis: the value of the feature
- y axis: number of websites

We can have further observation on the distribution.
Also, if you want to see the distribution of the importance features mentioned in random forrest, please refer to this file

## Execution

### Environment

python3.6

### Setup

[Dataset: TrafficResult-3 ( Closed world Dataset, Same as the link above)](https://drive.google.com/open?id=1R7ZqTzOGg9bWMqB2kXvWoJQHLJJEZCjq)

```
$ download the dataset from the above link
$ git clone https://github.com/jimmychang851129/NSLAB_WebFingerprint.git
$ fetch branch: Analysis/ML-training
$ cd NSLAB_WebFingerprint/code
$ pip3 install -r requirements.txt    # will install packages utilized by crawler,pcapParser and mlAnalysis
$ cd ml/
$ setup MLConfig.py
$ python3 randomForrest.py -i <path_to_TrafficResult-3> -o <output_Directory>
$ python3 randomForrest.py -h for more information
```

### RandomForrest

```
$ cd NSLAB_WebFingerprint/code/ml/
$ setup MLConfig.py
$ python3 randomForrest.py -i <path_to_TrafficResult-3> -o <output_Directory>
$ python3 randomForrest.py -h for more information
```

for comparsion of different torbrowser version

```
$ python3 randomForrest.py -i <First Datapath>,<Second Datapath> -v <version1,version2> -o <outputdir>

EX:
$ python3 randomForrest.py -i ~/Desktop/WFfeature/removeFailed/9/,/Users/jimmy/Desktop/WFfeature/removeFailed/8/  -v 9,8 -o ~/Desktop/WFfeature/mlresult/9-8
```

#### output

- labelmapping.txt: mapping of domain to the classes
- failedCase.txt: cases failed to classify
- featureimportance.pkl: DataFrame of feature importance in Random Forrest
- rfVisualize.png: img of feature importance

#### [Sample Output](https://drive.google.com/open?id=1694YbaXOeyFitDfsgBIsEGxqzwH3MTDE)

### GradientBoosting

```
$ cd NSLAB_WebFingerprint/code/ml/
$ setup MLConfig.py
$ python3 GradientBoosting.py -i <path_to_TrafficResult-3> -o <output_Directory>
$ python3 GradientBoosting.py -h for more information
```

#### output

- labelmapping.txt: mapping of domain to the classes
- failedCase.txt: cases failed to classify
- featureimportance.pkl: DataFrame of feature importance in GradientBoosting
- rfVisualize.png: img of feature importance

## BrowserVersionClassifier

### Browserclassifier and analysis

```
Train a browserClassifier based on the whole dataset(multiple domains)

$ python3 browserClassifier.py -i WFfeature/removeFailed -o WFfeature/browsercmp

Train a browserClassifier for each domain

$ python3 browserClassifier.py -i WFfeature/removeFailed -o WFfeature/browsercmp -sv
```

analyze the domain with low accuracy in browserclassifier

```
$ python3 browserClassifier.py -i WFfeature/removeFailed -o WFfeature/browsercmp -sv
$ python3 analysis.py
```

### FeatureVisualize.py

#### Draw boxplot of a specific domain

It will draw boxplot of top 9 features extracted from version classifier.

```
$ python3 browserClassifier.py -i WFfeature/removeFailed -o WFfeature/browsercmp -sv
$ python3 FeatureVisualize.py -i WFfeature/removeFailed -o WFfeature/browsercmp -u <url>
```

#### Observation

## DeepFingerprint Reproduce

### Feature Extract

```
$ cd deepfingerprint
$ python3 DFFeatureExtract.py -i <path_to_raw_traffic> -o <path_to_output_features>
```

### Training

```
$ cd deepfingerprint
$ python3 train.py -i <path to features> -o <path for output file>
```

### Compare

```
$ cd deepfingerprint
$ python3 train.py -t -d1 <model directory(load model)> -d2 <load features dataset of another version> -o <output results> 
```

| train\test | 7        | 8        | 9        |
| ---------- | -------- | -------- | -------- |
| 7          | 0.976479 | 0.019088 | 0.587606 |
| 8          | 0.044932 | 0.915098 | 0.125688 |
| 9          | 0.421791 | 0.025403 | 0.977744 |