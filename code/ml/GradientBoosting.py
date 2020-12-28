import csv, os
import argparse
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import MLConfig as cm

#############
# Reference # 
#############
# [Gradient Boosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier)

def writeLog(output,outputpath):
	with open(outputpath,'a+') as fw:
		fw.write(output+"\n")

# only read data with more than n_threshold features
def ReadAllFeatures(inputdir,outputdir):
	x,y = [],[]
	cnt = 0
	labelpath = os.path.join(outputdir,"labelmapping.txt")
	for domain in os.listdir(inputdir):
		if domain.endswith(".csv"):
			filepath = os.path.join(inputdir,domain)
			t = []
			with open(filepath,'r') as f:
				reader = csv.DictReader(f)
				for line in reader:
					t.append([float(line[h]) for h in cm.headerlist])
			if len(t) > cm.n_threshold:
				writeLog("mapping: %s -> %d"%(domain.strip(".csv"),cnt),labelpath)
				for d in t:
					x.append(d)
					y.append(cnt)
				cnt += 1
	return shuffle(np.array(x),np.array(y))

###################
# Normalized data #
###################
def NormalizeData(x):
	scalar = StandardScaler()
	scalar.fit(x)
	return scalar.transform(x)

######################################
# preprocessing data befor training #
######################################
def Preprocessing(x):
	x = NormalizeData(x)
	return x

############################################
# Gradient Boosting capable of multi-class #
############################################
def Training(x_train,y_train,GBparams):
	clf = GradientBoostingClassifier(**GBparams)
	clf.fit(x_train,y_train)
	return clf

###########################
# k-fold cross validation #
###########################
def Validation(x_train,y_train):
	clf = GradientBoostingClassifier(**cm.GBparams)
	scores = cross_val_score(clf,x_train,y_train,cv=cm.k_fold,scoring='accuracy')
	print("cross-validation score: %s"%(str(scores)))
	print("cross-validation Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

################################
# test model with testing data #
################################
def Testing(clf,x_test,y_test,outputdir,GBparams):
	ans = clf.predict(x_test)
	failcnt = []
	failpath = os.path.join(outputdir,"%d_failedCase.txt"%(GBparams['n_estimators']))
	logpath = os.path.join(outputdir,'%d_logfile.txt'%(GBparams['n_estimators']))
	for a,b in zip(ans,y_test):
		if a != b:
			failcnt.append([a,b])
	print("Testing Accuracy: %f"%(1-(len(failcnt)/len(y_test))))
	writeLog("Testing Accuracy: %f"%(1-(len(failcnt)/len(y_test))),logpath)
	s = ""
	for d in failcnt:
		s += "failed: %d,%d\n"%(d[0],d[1])	# the latter one is the correct class
	writeLog(s,failpath)

###################################
# show the importance of features #
###################################
def VisualizeFeatures(clf,outputdir,n_estimators):
	pklpath = os.path.join(outputdir,"%d_featureImportance.pkl"%(n_estimators))
	imgpath = os.path.join(outputdir,"GBVisualize.png")
	feature_imp = pd.Series(clf.feature_importances_,index=cm.headerlist).sort_values(ascending=False)
	feature_imp.to_pickle(pklpath)
	# sns.barplot(x=feature_imp, y=feature_imp.index)
	# plt.xlabel('Feature Importance Score')
	# plt.ylabel('Features')
	# plt.title("Visualizing Important Features")
	# plt.legend()
	# plt.savefig(imgpath)

def parseCommand():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputdir','-i',type=str,default=None, help='Direcotry of Features, EX: directory path of TrafficResult-3')
	parser.add_argument('--outputdir','-o',type=str,default="./", help='path of output Directory')
	args = parser.parse_args()
	if args.inputdir == None:
		print("inputdir argument should be specified")
		return 0
	return args

def main(args=0):
	if args == 0:
		return 0
	x,y = ReadAllFeatures(args.inputdir,args.outputdir)
	x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=cm.testingsize, stratify=y) # split data(ensure every classes appears in training set and testing set)
	x_train = Preprocessing(x_train)
	x_test = Preprocessing(x_test)
	# Validation(x_train,y_train)
	for i in range(130,170,20):
		print("testing i = ",i)
		tmpGBparams = dict(cm.GBparams)
		tmpGBparams['n_estimators'] = i
		clf = Training(x_train,y_train,tmpGBparams)
		Testing(clf,x_test,y_test,args.outputdir,tmpGBparams)
		VisualizeFeatures(clf,args.outputdir,i)

if __name__ == '__main__':
	args = parseCommand()
	main(args)
