import scipy, os, sys, csv, argparse
import pandas as pd
from scipy.stats import f_oneway
sys.path.append("../ml")
import FeatureVisualize
import pingouin as pg

##########
# config #
##########
IQRrange = 1.5

# input: simple list: domaindata[domain][feature][cnt]
# output: in-range sample, [num of samples in data, outlier prob]
def filterOutlier(data):
    df = pd.DataFrame(data)
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1    #IQR is interquartile range. 
    output = ((df >= Q1 - IQRrange * IQR)  & (df <= Q3 + IQRrange *IQR)).any(axis=1)
    inrange,outrange = [],[]
    for i in range(len(output)):
        if output[i] == True:
            inrange.append(data[i])
        else:
            outrange.append(data[i])
    return inrange,[len(data), len(outrange) / len(data)]


def getDataDistribution(inputdir,targetFeature,websiteList):
    VersionList = ["7","8","9"]
    inrangestatistic = dict()
    outlierstatistic = dict()
    for web in websiteList:
        domain = web+".csv" if ".csv" not in web else web
        domaindata = dict({domain:dict()})
        inrangestatistic[domain] = dict()
        outlierstatistic[domain] = dict()
        for feature in targetFeature:
            domaindata[domain][feature] = [[],[],[]]
            inrangestatistic[domain][feature], outlierstatistic[domain][feature] = [],[]
        if domain.endswith('.csv'):
            cnt = 0
            for version in VersionList:
                filepath = os.path.join(inputdir,version,domain)
                try:
                    with open(filepath,'r') as f:
                        reader = csv.DictReader(f)
                        for line in reader:
                            for feature in targetFeature:
                                domaindata[domain][feature][cnt].append(float(line[feature]))
                except Exception as e:
                    print("Error domain:",domain)
                    pass
                finally:
                    cnt += 1
        for feature in targetFeature:
            x,tmp = filterOutlier(domaindata[domain][feature][0])
            inrangestatistic[domain][feature].append(x)
            outlierstatistic[domain][feature].append(tmp)
            x,tmp = filterOutlier(domaindata[domain][feature][1])
            inrangestatistic[domain][feature].append(x)
            outlierstatistic[domain][feature].append(tmp)
            x,tmp = filterOutlier(domaindata[domain][feature][2])
            inrangestatistic[domain][feature].append(x)
            outlierstatistic[domain][feature].append(tmp)
    return inrangestatistic, outlierstatistic


def checkOutlierPercentage(outlier):
    for domain in outlier.keys():
        for feature in outlier[domain].keys():
            print("domain: %s, feature: %s, version: %d, data: %d, outlier: %f"%(domain,feature,7,outlier[domain][feature][0][0],outlier[domain][feature][0][1]))
            print("domain: %s, feature: %s, version: %d, data: %d, outlier: %f"%(domain,feature,7,outlier[domain][feature][1][0],outlier[domain][feature][1][1]))
            print("domain: %s, feature: %s, version: %d, data: %d, outlier: %f"%(domain,feature,7,outlier[domain][feature][2][0],outlier[domain][feature][2][1]))


def statisticAnalysis(inlier):
    d = dict()
    for domain in inlier.keys():
        d[domain] = dict()
        for feature in inlier[domain].keys():
            d[domain][feature] = f_oneway(inlier[domain][feature][0],inlier[domain][feature][1],inlier[domain][feature][2]).pvalue
    return d

################
# modification #
################
def checkPvalue(p):
    d = []
    for domain in p.keys():
        for feature in p[domain].keys():
            if p[domain][feature] < 0.05:
                d.append(1)
                break
    if 0 in d:
        print("same traffic features for a domain....")


#############
# tukey-HSD #
#############
def tukeyHSD(inrangestatistic):
    similaritydict = dict()
    for domain in inrangestatistic.keys():
        similaritydict[domain] = []
        for feature in inrangestatistic[domain].keys():
            minsize = min(len(inrangestatistic[domain][feature][0]),len(inrangestatistic[domain][feature][1]),len(inrangestatistic[domain][feature][2]))
            data = []
            for i in range(minsize):
                data.append(["7",inrangestatistic[domain][feature][0][i]])
                data.append(["8",inrangestatistic[domain][feature][1][i]])
                data.append(["9",inrangestatistic[domain][feature][2][i]])
            df = pd.DataFrame(data,columns=["version","feature"])
            output = df.pairwise_tukey(dv='feature',between='version')
            for e in output['p-tukey']:
                if e > 0.05:
                    similaritydict[domain].append(feature)
                    print("domain=%s, feature=%s have similarity"%(domain,feature))
                    print(output)
                    break
    print("similaritydict result")
    for domain in similaritydict:
        print("%s -> %d\n"%(domain,len(similaritydict[domain])))
    return similaritydict


############
# test all #
############
def retrieveALLWebsiteList(inputdir):
    weblist = []
    versionList = ["7","8","9"]
    for version in versionList:
        weblist.append(set())
        versionDir = os.path.join(inputdir,version)
        for domain in os.listdir(versionDir):
            weblist[-1].add(domain)
    websiteList = weblist[0].intersection(weblist[1]).intersection(weblist[2])
    return websiteList

def parseCommand():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir','-i',type=str,default=None, help='inputdir to rf features')
    parser.add_argument("--featuredir",'-f',type=str,default=None, help='important feature dir')
    parser.add_argument('--all','-a',action='store_true',help='test with all domains')
    args = parser.parse_args()
    return args

def main(args):
    targetFeature = FeatureVisualize.RetrieveTop9Features(args.featuredir)
    if args.all != True:
        websiteList = ["amazon.co.uk","aol.com","bbc.com","cnn.com","dailymail.co.uk","harvard.edu","imdb.com","indeed.com","instagram.com","instructure.com","wired.com"]
    else:
        websiteList = retrieveALLWebsiteList(args.inputdir)
    print("filtering outlier...")
    inrangestatistic, outlierstatistic = getDataDistribution(args.inputdir,targetFeature,websiteList)
    # checkOutlierPercentage(outlierstatistic)
    print("running anova....")
    p = statisticAnalysis(inrangestatistic)
    print("running pairwise-tukey")
    similaritydict = tukeyHSD(inrangestatistic)

if __name__ == '__main__':
    args = parseCommand()
    main(args)
