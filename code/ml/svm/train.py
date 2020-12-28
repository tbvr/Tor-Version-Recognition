import os, csv, pickle
import numpy as np
from sklearn import svm
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import argparse
import time

def writeLog(filepath,outputstr):
    with open(filepath,'a+') as f:
        f.write(outputstr+"\n")
        f.flush()

def ReadDomainSet():
    domainList = []
    with open("dataset.txt") as f:
        for line in f:
            domainList.append(line.strip())
    return domainList

# clf = svm.SVC(decision_function_shape='ovo')
#########################
# removed failed sample #
#########################
# remove failure traffic
# remove packetlen < 0.8 * median
# remove traffic with median less than 80 cells
def RemoveFailedSample(data):
    datalenList = []
    for ele in data:
    	datalenList.append(sum([abs(x) for x in ele]) // 600)
    datalenList = np.array(datalenList)
    med = np.percentile(datalenList,50)
    t = [ele for ele in data if sum([abs(x) for x in ele]) // 600 > med * 0.8]
    if len(t) > 40: # only leave 40 traffic instances, leave kernel size smaller
        t = t[:40]
    if med < 80:
    	return []
    return t

def ReadData(dirpath,outputdir):
    data = []
    label = []
    cnt = 0
    instancelist = dict()
    labelpath = os.path.join(outputdir,"labelmapping.txt")
    domainList = ReadDomainSet()
    for domain in domainList:
        if "DS_Store" not in domain:
            try:
                filepath = os.path.join(dirpath,domain)
                tmp = []
                with open(filepath,'r') as f:
                    for line in f:
                        if line.strip() != '':
                            tmp.append([float(x) for x in line.strip().split(',')])
                tmp = RemoveFailedSample(tmp)
                if tmp == []:
                    print("Warning: domain %s has few packets"%(domain))
                else:
                    label += [cnt] * len(tmp)
                    data += tmp
                    writeLog(labelpath,"mapping: %s -> %d"%(domain,cnt))
                    cnt += 1
                    instancelist[domain] = len(tmp)
            except Exception as e:
                print("[train.py error]ReadData, failed to read file or remove failed sample",domain)
                print(str(e))
    data = np.array(data)
    print("instance size of each domain...")
    print({k: v for k, v in sorted(instancelist.items(), key=lambda item: item[1])})
    # return shuffle(data,label)
    return shuffle(data,label)

# output: [1,-1,-1,-1,1.....]
def RecordToCell(x):
    output = []
    for ele in x:
        ele = int(ele)
        output += [1] * (ele // 600) if ele > 0 else [-1] * (abs(ele) // 600)
    return output

def preBuildDictionary(x):
    data = RecordToCell(x)
    loc = [set(),set()]
    for i in range(len(data)):
        if data[i] == 1:    # positive int
            loc[0].add(i)
        else:               # negative int
            loc[1].add(i)
    return loc

def EditDistance(loc,x1len,x2):
    transport_cost = 0.01
    outputgoing_deletion = 4
    incoming_deletion = 1
    cost = 0
    x2 = RecordToCell(x2)
    for i in range(len(x2)):
        idx = 0 if x2[i] == 1 else 1
        if len(loc[idx]) != 0:
            pos = min(loc[idx], key=lambda x:abs(x-i))
            cost = abs(pos - i) * transport_cost
            loc[idx].remove(pos)
        else:
            cost += outputgoing_deletion if x2[i] == 1 else incoming_deletion
            cost += len(loc[0])*outputgoing_deletion
    cost += len(loc[1]) * incoming_deletion 
    return cost / min(x1len,len(x2))

# cnt = 0
# for i in range(len(x1)):
#     while cnt < len(x2) and 

# clf = svm.SVC(kernel=testKernel,decision_function_shape='ovo')
# clf.fit(data, label)
def KernelMethod(x,x2=0,stpoint=0,edpoint=0,outputdir="./"):
    if x2 == 0:
        output = np.zeros((len(x),len(x)))
        if stpoint == 0 and edpoint == 0:
            edpoint = len(x)
        for i in range(stpoint,edpoint):
            print("%s\t %d/%d"%(time.strftime('%Y-%m-%d %H:%M', time.localtime()),i,len(x)))
            loc = preBuildDictionary(x[i])
            for j in range(i+1):
                output[i][j] = EditDistance(loc,len(x[i]),x[j])
            pickle.dump(output[i],open(os.path.join(args.outputdir,"svmpkl","%d.pkl"%(i)),'wb'))
    else:
        output = np.zeros((len(x2),len(x)))
        for i in range(len(x)):
            loc = preBuildDictionary(x[i])
            for j in range(len(x)):
                output[i][j] = EditDistance(loc,len(x[i]),x2[j])

def Readpkl(filepath,kernel=0):
    if kernel == 1:
        return np.power(np.e,pickle.load(open(filepath,'rb')))
    return pickle.load(open(filepath,'rb'))

def Training(kernel,datay):
    x1_train, x1_test, y1_train, y1_test = train_test_split(kernel,datay,test_size=0.1, stratify=datay)
    clf = svm.SVC(decision_function_shape='ovo')
    clf.fit(kernel,datay)
    ans = clf.predict(kernel)

def parseCommand():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir','-i',type=str,default=None, help='Direcotry of Features, EX: directory path of TrafficResult-3')
    parser.add_argument('--outputdir','-o',type=str,default="./", help='path of output Directory')
    parser.add_argument('--loaddata','-l',action='store_true',help='load pickle and not read raw data')
    parser.add_argument('--pklpath','-p',type=str,default=None)
    parser.add_argument('--st',type=str,default=0,help='svm vector start point[0-4000]')
    parser.add_argument('--ed',type=str,default=4000,help='svm vector end point[0-4000]')
    args = parser.parse_args()
    return args

def main(args):
    args = parseCommand()
    if args.loaddata == False:
        assert args.inputdir != None
        x,y = ReadData(args.inputdir,args.outputdir)
        pickle.dump(x,open(os.path.join(args.outputdir,"datax.pkl"),'wb'))
        pickle.dump(y,open(os.path.join(args.outputdir,"datay.pkl"),'wb'))
    else:
        assert args.loaddata == True and args.pklpath != None
        x = pickle.load(open(os.path.join(args.pklpath,'datax.pkl'),'rb'))
        y = pickle.load(open(os.path.join(args.pklpath,'datay.pkl'),'rb'))
        print("x,y",len(x),len(y))
        svmdata = os.path.join(args.outputdir,"svmpkl")
        if not os.path.exists(svmdata):
            os.makedirs(svmdata, exist_ok=True)
        KernelMethod(x,x2=0,stpoint=args.st,edpoint=args.ed,outputdir=args.outputdir)
    # x1_train, x1_test, y1_train, y1_test = train_test_split(x,y,test_size=0.1, stratify=y)
    # pickle.dump(x1_train,open(os.path.join(args.outputdir,"x1_train.pkl"),'wb'))
    # pickle.dump(x1_test,open(os.path.join(args.outputdir,"x1_test.pkl"),'wb'))
    # pickle.dump(y1_train,open(os.path.join(args.outputdir,"y1_train.pkl"),'wb'))
    # pickle.dump(y1_test,open(os.path.join(args.outputdir,"y1_test.pkl"),'wb'))

if __name__ == '__main__':
    args = parseCommand()
    main(args)

# inputdir = "/Users/jimmy/Desktop/WF_Result/WFfeature/svmfeature/9"
# outoputdir = "/Users/jimmy/Desktop/WF_Result/WFfeature/svmfeature/output"