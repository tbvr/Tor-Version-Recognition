import os,csv,pickle
import sys, argparse
sys.path.append('../../')
from FeatureUtils import getTarFile, RemoveUncompressDir
from FeatureUtils import parseFileName, MergeDict,parseFileName
from utils import StreamProcessing
import Config as cm

##########
# config #
##########
FilterFlag = [1,2] # SYN, FIN
HalfCell = 256	   # round packetlen to the closest multiple 512, less than 256 = 0
featurelen = 5000  # based on deepfingerprint
# handle ack,encryption, macoverhead, refer to data collection paper

def ReadCSV(filepath,StreamList):
	nt = []
	with open(filepath,'r') as f:
		reader = csv.DictReader(f)
		for line in reader:
			if int(line['flags']) not in FilterFlag and int(line['packetlen']) > HalfCell:
				if line['dstip'] in StreamList:
					nt += [1] * round((int(line['packetlen'])/500))
				elif line['srcip'] in StreamList:
					nt += [-1] * round((int(line['packetlen'])/500))
	if len(nt) < featurelen:
		nt += [0] * (featurelen - len(nt))
	return nt

def writeFeature(outputdir,domain,data):
	outputpath = os.path.join(outputdir,domain)
	if os.path.exists(outputpath):
		tmp = pickle.load(open(outputpath,'rb'))
	else:
		tmp = []
	tmp.append(data)
	pickle.dump(tmp,open(outputpath,"wb"))

def ParsePcap(inputdir,outputdir,ver):
	for CrawlDate in os.listdir(inputdir):				# inputdir: Traffic/
		if "DS_Store" not in CrawlDate and CrawlDate != '':
			try:
				CrawlDir = os.path.join(inputdir,CrawlDate)	# CrawlDir: 20200422/
				print("processing Dir: %s..."%(CrawlDir))
				domainDir = getTarFile(CrawlDir,ver)			# domainDir: 20200422/traces/ 
				logfile = os.path.join(CrawlDir,cm.StreamInfo)	# logfile: XXX/logs/streamInfo.txt
				if not os.path.exists(logfile):
					logfile = os.path.join(CrawlDir,'streamInfo.txt')
				StreamList = StreamProcessing(logfile)
				for domain in os.listdir(domainDir):
					if ".DS_Store" not in domain and domain != '':
						domainpath = os.path.join(domainDir,domain)
						print("parsing domain: ",domainpath)
						for instance in os.listdir(domainpath):
							try:
								instancepath = os.path.join(domainpath,instance)
								inputfilepath = instancepath.split("Traffic/")[-1]
								cnt,domain,timestamp = parseFileName(instancepath)
								if (domain,cnt) in StreamList:
									datalist = ReadCSV(instancepath,StreamList[(domain,cnt)])
									writeFeature(outputdir,domain,datalist)
								else:
									print("Not found: %s in streamInfo"%(instancepath))
							except Exception as e:
								print("Error string: ",str(e))
								print(str(e))
								pass
			except Exception as e:
				print(str(e))
			finally:
				RemoveUncompressDir(domainDir)				# domainDir: 20200422/<untardir>

def ParseArg():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputdir','-i',type=str,required=True, help='input traces dir, EX: traces')
	parser.add_argument("--outputdir",'-o',type=str,required=True, help='outputdir')
	parser.add_argument("--version",'-v',type=str,default="new",help="new Version Crawler or old one")
	args = parser.parse_args()
	return args

def main():
	args = ParseArg()
	if args.inputdir == None or args.outputdir == None:
		print("inputdir and outputdir should be specified")
		return 0
	ParsePcap(args.inputdir,args.outputdir,args.version)


if __name__ == '__main__': 
	main()