import os,csv
from statistics import median
import MLConfig as cm

header = ','.join(cm.headerlist + ['srcDir'])

inputdir = "/Users/jimmy/Desktop/WF_Result/WFfeature/9"
outputdir = "/Users/jimmy/Desktop/WF_Result/WFfeature/removeFailed/9"

for domain in os.listdir(inputdir):
	if domain.endswith(".csv"):
		filepath = os.path.join(inputdir,domain)
		l,data = [],[]
		cnt = 0
		with open(filepath,'r') as f:
			for line in f:
				if cnt == 1:
					l.append(int(line.split(',')[0]))
					data.append(line)
				cnt = 1
		med = median(l)
		if med > 100 and len(l) > cm.n_threshold:
			outputpath = os.path.join(outputdir,domain)
			if not os.path.isfile(outputpath):
				with open(outputpath,'a+') as fw:
					fw.write(header+"\n")
			fw = open(outputpath,'a+')
			for i in range(len(l)):
				if l[i] > med * 0.8:
					fw.write(data[i])
