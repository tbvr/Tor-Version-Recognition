import csv, pickle, os, argparse
import sklearn
import MLConfig as cm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

domain_acc_file = "/Users/jimmy/Desktop/WF_Result/WFfeature/browsercmp/single_domain_acc.csv"

# fetch domain with acc_rate lower than 80%
def getLowAccDomain():
	d = dict()
	CheckDomainList = []
	with open(domain_acc_file) as f:
		for line in f:
			line = line.strip().split(',')
			try:
				d[line[0]] = float(line[1])
			except Exception as e:
				pass
	l = sorted(d, key=d.get, reverse=True)
	for ele in l:
		if d[ele] < 0.8:
			CheckDomainList.append(ele)
		print("%s acc -> %f"%(ele,d[ele]))
	return CheckDomainList

def ReadImportantFeature(importancepath,threshold = 0.01):
	with open(importancepath,'rb') as f:
		data = pickle.load(f)
	ret = dict()
	for k,v in data.items():
		if float(v) > threshold:
			ret[k] = v
	return ret

def ReadCSV(inputdir,targetFeature = []):
	x = []
	for i in range(len(cm.versionList)):
		dirpath = os.path.join(inputdir,cm.versionList[i])
		for domain in os.listdir(dirpath):
			if domain.endswith(".csv"):
				filepath = os.path.join(dirpath,domain)
				t = []
				with open(filepath,'r') as f:
					reader = csv.DictReader(f)
					for line in reader:
						t.append([float(line[h]) for h in targetFeature.keys()])
					if len(t) > cm.n_threshold:
						for d in t:
							x.append(d)
	return x

#################
# write HeatMap #
#################
def writeImg(data,outputpath):
	sns.set(font_scale=0.8)
	plt.subplots_adjust(bottom=0.20)
	plt.subplots_adjust(left=0.20)
	sns.heatmap(data,cmap="coolwarm", xticklabels=data.columns.values, yticklabels=data.columns.values)
	plt.savefig(outputpath)
	plt.clf()

# calculate feature covariance and visualize
def FeatureCovCorrVisualize(data,targetFeature,outputdir):
	df = pd.DataFrame(data,columns=targetFeature.keys())
	cov = df.cov()
	outputpath = os.path.join(outputdir,"FeatureCov.png")
	writeImg(cov,outputpath)
	df = pd.DataFrame(data,columns=targetFeature.keys())
	corr = df.corr()
	outputpath = os.path.join(outputdir,"FeatureCorr.png")
	writeImg(corr,outputpath)

def parseCommand():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputdir','-i',type=str,default=None, help='Direcotry of Features, EX: directory path of TrafficResult-3')
	parser.add_argument('--featurefile','-f',type=str,default=None,help='feature importance from browser cmp')
	parser.add_argument('--outputdir','-o',type=str,default="./", help='path of output Directory')
	args = parser.parse_args()
	if args.inputdir == None:
		print("inputdir argument should be specified")
		return 0
	return args

def main(args):
	# args = parseCommand()
	# ret = ReadImportantFeature(args.featurefile)
	# data = ReadCSV(args.inputdir,ret)
	# FeatureCovCorrVisualize(data,ret,args.outputdir)
	domainList = getLowAccDomain()

if __name__ == '__main__':
	args = parseCommand()
	main(args)

#############
# Reference #
#############
# legend align(cutoff issue): https://stackoverflow.com/questions/48526788/python-seaborn-legends-cut-off
# seaborn map: https://stackoverflow.com/questions/29432629/plot-correlation-matrix-using-pandas