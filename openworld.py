import os,joblib
import os, pickle, csv, sys
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from FeatureUtils import parseFileName,ReadCSV,writeFeature, MergeDict
from FeatureUtils import getTarFile, RemoveUncompressDir, WriteLog
from utils import StreamProcessing
import CellFeature, TimeFeature
import Config as cm
from statistics import median
import numpy as np
import joblib
sys.path.append("./ml")
import MLConfig as mlconfig
from randomForrest import writeLog
import browserClassifier

failedlist = set()
with open("ErrorList.txt",'r') as f:
	for line in f:
		if line.strip() != "":
			failedlist.append(line.split(',')[0])


inputdir = "/home/jimmy/openworld/7/part2trace/trace"
logfile = "/home/jimmy/openworld/7/part2trace/logs/streamInfo.txt"
outputdir = "/home/jimmy/openworld/"
ver = 7
def ProcessRawData(inputdir,outputdir,ver):
    rfoutputdir = os.path.join(outputdir,"rf/%s"%(ver))
    StreamList = StreamProcessing(logfile)
    for domain in os.listdir(inputdir):
        domainpath = os.path.join(inputdir,domain)
        for instance in os.listdir(domainpath):
            try:
                instancepath = os.path.join(domainpath,instance)
                cnt,domain,timestamp = parseFileName(instancepath)
                if (domain,cnt) in StreamList:
                    rf_datalist = ReadCSV(instancepath,StreamList[(domain,cnt)])
                    cellsDict = CellFeature.FeatureRetrieve(rf_datalist,StreamList[(domain,cnt)],domain)
                    TimeDict = TimeFeature.FeatureRetrieve(rf_datalist,StreamList[(domain,cnt)],domain)
                    AllDict = MergeDict(cellsDict,TimeDict)
                    AllDict['srcDir'] = instancepath.split("Traffic/")[-1]
                    writeFeature(rfoutputdir,domain,AllDict)
                else:
                    WriteLog("Not found: %s in streamInfo"%(instancepath))
            except Exception as e:
                print("Error string: ",str(e))
                WriteLog(str(e))
                pass		

inputdir = "/home/jimmy/openworld"
outputdir = "/home/jimmy/openworld"
def RemoveFailSample(inputdir,outputdir):
    versionList = ['7','8','9']
    header = ','.join(mlconfig.headerlist + ['srcDir'])
    for version in versionList:
        rfdir = os.path.join(inputdir,'rf',version)
        rf_outputdir = os.path.join(outputdir,'rf/removeFailed',version)
        for domain in os.listdir(rfdir):
            if domain.endswith(".csv"):
                filepath = os.path.join(rfdir,domain)
                l,data = [],[]
                cnt = 0
                with open(filepath,'r') as f:
                    for line in f:
                        if cnt == 1:
                            l.append(int(line.split(',')[0]))
                            data.append(line)
                        cnt = 1
                med = median(l)
                if med > 100:
                    rfoutputpath = os.path.join(rf_outputdir,domain)
                    if not os.path.isfile(rfoutputpath):
                        with open(rfoutputpath,'w') as fw:
                            fw.write(header+"\n")
                    fw = open(rfoutputpath,'a+')
                    cnt_check = 0
                    for i in range(len(l)):
                        if l[i] > med * 0.8:
                            cnt_check += 1
                            fw.write(data[i])

def ReadRFData(filepath):
    data = []
    try:
        with open(filepath,'r') as f:
            reader = csv.DictReader(f)
            for line in reader:
                data.append([float(line[h]) for h in mlconfig.headerlist])
    except Exception as e:
        data = []
        print("[ReadRFData error] filepath not found: ",filepath)
        print(str(e))
    return data

#######################
# process csv to features #
#######################
inputdir = "/home/jimmy/openworld/7/part2trace/trace"
logfile = "/home/jimmy/openworld/7/part2trace/logs/streamInfo.txt"
outputdir = "/home/jimmy/openworld/"
ver = 7
ProcessRawData(inputdir,outputdir,ver)

inputdir = "/home/jimmy/openworld/7/2020-11-16-08/trace"
logfile = "/home/jimmy/openworld/7/2020-11-16-08/streamInfo.txt"
outputdir = "/home/jimmy/openworld/"
ProcessRawData(inputdir,outputdir,ver)

inputdir = "/home/jimmy/openworld/8/2020-11-13-11/trace"
logfile = "/home/jimmy/openworld/8/2020-11-13-11/streamInfo.txt"
outputdir = "/home/jimmy/openworld/"
ver = 8
ProcessRawData(inputdir,outputdir,ver)

inputdir = "/home/jimmy/openworld/9/2020-11-13-11/trace"
logfile = "/home/jimmy/openworld/9/2020-11-13-11/streamInfo.txt"
outputdir = "/home/jimmy/openworld/"
ver = 9
ProcessRawData(inputdir,outputdir,ver)

#################
# removedFailed #
#################
inputdir = "/home/jimmy/openworld"
outputdir = "/home/jimmy/openworld"
RemoveFailSample(inputdir,outputdir)

#############
# read data #
#############
header = mlconfig.headerlist + ['srcDir']
inputdir = "/home/jimmy/openworld/rf/removeFailed"
outputdir = "/home/jimmy/openworld/rf/dataset"
versionList = ["7","8","9"]
for version in versionList:
    verdir = os.path.join(inputdir,version)
    domainmap = os.path.join(outputdir,"domainmapping-%s.txt"%(version))
    fw = open(domainmap,'w')
    l = []
    l.append(header)
    for domain in os.listdir(verdir):
        domainpath = os.path.join(verdir,domain)
        with open(domainpath,'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for line in csv_reader:
                l.append([float(x) for x in line[:-1]])
        fw.write("%s-%s\n"%(version,domain))
    fw.close()
    outputpath = os.path.join(outputdir,'openworld-%s.pkl'%(version))
    with open(outputpath, 'wb') as fw:
        pickle.dump(l,open(outputpath,'wb'))

##############
# load model #
##############
import joblib,pickle,os
import numpy as np
from sklearn.utils import shuffle
sys.path.append("./ml")
import browserClassifier

inputdir = "/home/jimmy/twophase/versionclassifier"
versionmodel = os.path.join(inputdir,"versionClassifier-90-split.pkl")
clf = joblib.load(versionmodel)

versionlist = ['7','8','9']
data = []
label = []
inputdir = "/home/jimmy/openworld/rf/dataset"
cnt = 0
for ver in versionlist:
    openworldir = os.path.join(inputdir,"openworld-%s.pkl"%(ver))
    tmp = pickle.load(open(openworldir,'rb'))
    tmp = [x for x in tmp]
    data += tmp[1:]
    label += [cnt] * len(tmp[1:])
    cnt += 1

data = np.array(data)
label = np.array(label)
data = browserClassifier.Preprocessing(data)
shuffle(data,label)
ans = clf.predict(data)

correct,wrong = 0,0
for i in range(len(ans)):
    if ans[i] == label[i]:
        correct += 1
    else:
        wrong += 1

print("accuracy = %f"%(correct/(correct+wrong)))