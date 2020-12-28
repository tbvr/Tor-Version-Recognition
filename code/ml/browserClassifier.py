import os,csv
import MLConfig as cm
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from randomForrest import writeLog
import argparse
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import pandas as pd

######################################
# preprocessing data befor trainging #
######################################
def Preprocessing(x):
	x = NormalizeData(x)
	return x

def NormalizeData(x):
	scalar = StandardScaler()
	scalar.fit(x)
	return scalar.transform(x)

#########################################
# random forrest capable of multi-class #
#########################################
def Training(x_train,y_train):
	clf = RandomForestClassifier(n_estimators=cm.Trees, n_jobs=cm.njobs, criterion='gini', verbose=0)
	clf.fit(x_train,y_train)
	return clf

def ReadCSV(inputdir,outputdir):
	x,y = [],[]
	for i in range(len(cm.versionList)):
		dirpath = os.path.join(inputdir,cm.versionList[i])
		for domain in os.listdir(dirpath):
			if domain.endswith(".csv"):
				filepath = os.path.join(dirpath,domain)
				t = []
				with open(filepath,'r') as f:
					reader = csv.DictReader(f)
					for line in reader:
						t.append([float(line[h]) for h in cm.headerlist])
					if len(t) > cm.n_threshold:
						for d in t:
							x.append(d)
							y.append(i)
	return shuffle(np.array(x),np.array(y))

##################
# ret all domain #
##################
def retDomain(inputdir):
	l = []
	dirpath = os.path.join(inputdir,"7")
	for domain in os.listdir(dirpath):
		if domain.endswith(".csv"):
			l.append(domain[:-4])
	return l

###########################
# test only single domain #
###########################
def ReadSingleDomain(inputdir,testdomain):
	x,y = [],[]
	for i in range(len(cm.versionList)):
		dirpath = os.path.join(inputdir,cm.versionList[i])
		filepath = os.path.join(dirpath,testdomain+".csv")
		t = []
		if os.path.isfile(filepath):
			with open(filepath,'r') as f:
				reader = csv.DictReader(f)
				for line in reader:
					t.append([float(line[h]) for h in cm.headerlist])
				if len(t) > cm.n_threshold:
					for d in t:
						x.append(d)
						y.append(i)
	return shuffle(np.array(x),np.array(y))

def parseCommand():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputdir','-i',type=str,default=None, help='Direcotry of Features, EX: directory path of TrafficResult-3')
	parser.add_argument('--outputdir','-o',type=str,default="./", help='path of output Directory')
	parser.add_argument('--testsingle', '-s', help='train rf for every domain',action='store_true')
	parser.add_argument('--verbose', '-v',default=False, help='train rf for every domain',action='store_true')
	args = parser.parse_args()
	if args.inputdir == None:
		print("inputdir argument should be specified")
		return 0
	return args

def VisualizeFeatures(clf,outputdir):
	pklpath = os.path.join(outputdir,"featureImportance.pkl")
	feature_imp = pd.Series(clf.feature_importances_,index=cm.headerlist).sort_values(ascending=False)
	feature_imp.to_pickle(pklpath)

def Testing(clf,x_test,y_test,outputdir,testdomain = False):
	ans = clf.predict(x_test)
	failcnt = []
	failpath = os.path.join(outputdir,"failedCase.txt")
	for a,b in zip(ans,y_test):
		if a != b:
			failcnt.append([a,b])
	print("Testing Accuracy: %f"%(1-(len(failcnt)/len(y_test))))
	if testdomain != False:
		l = []
		logfile = os.path.join(outputdir,"log.txt")
		writeLog("%s -> Testing Accuracy: %f"%(testdomain,1-(len(failcnt)/len(y_test))),logfile)

def txtTocsv(outputdir):
	filepath = os.path.join(outputdir,"log.txt")
	outputpath = os.path.join(outputdir,"domain_acc.csv")
	l = []
	with open(filepath,'r') as f:
		for line in f:
			line = line.strip().split(' ')
			domain = line[0]
			acc = line[-1]
			l.append([domain,acc])
	with open(outputpath,'w') as fw:
		fw.write("domain,acc\n")
		for ele in l:
			fw.write("%s,%s\n"%(ele[0],ele[1]))

def SaveFeatureImportance(outputdir,domain,data):
	filepath = os.path.join(outputdir,"domainFeatureIMP",domain+".pkl")
	print("filepath = ",filepath)
	data = data.nlargest(n=10)
	data.to_pickle(filepath)

def main(args):
	if args == 0:
		return 0
	if args.testsingle == True:
		domainList = retDomain(args.inputdir)
		for domain in domainList:
			print("reading domain %s..."%(domain))
			x,y = ReadSingleDomain(args.inputdir,domain)
			x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=cm.testingsize, stratify=y) # split data(ensure every classes appears in training set and testing set)
			x_train = Preprocessing(x_train)
			x_test = Preprocessing(x_test)
			print("training domain %s..."%(domain))
			clf = Training(x_train,y_train)
			print("testing domain %s... "%(domain))
			Testing(clf,x_test,y_test,args.outputdir,testdomain = domain)
			if args.verbose == True:
				feature_imp = pd.Series(clf.feature_importances_,index=cm.headerlist).sort_values(ascending=False)
				print(feature_imp)
				SaveFeatureImportance(args.outputdir,domain,feature_imp)
		txtTocsv(args.outputdir)
	else:
		x,y = ReadCSV(args.inputdir,args.outputdir)
		x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=cm.testingsize, stratify=y) # split data(ensure every classes appears in training set and testing set)
		x_train = Preprocessing(x_train)
		x_test = Preprocessing(x_test)
		# Validation(x_train,y_train)
		clf = Training(x_train,y_train)
		Testing(clf,x_test,y_test,args.outputdir)
		VisualizeFeatures(clf,args.outputdir)

if __name__ == '__main__':
	args = parseCommand()
	main(args)