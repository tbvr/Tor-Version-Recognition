import csv, argparse, os
import matplotlib.pyplot as plt

headerlist = "Num_Packet,Num_outgoinging_packet,Num_incoming_packet,outgoing_ratio,incoming_ratio,std_outgoing_packetOrder,avg_outgoing_packetOrder,std_incoming_packetOrder,avg_incoming_packetOrder,Concentrate_outgoing_avg,Concentrate_incoming_avg,Concentrate_outgoing_std,Concentrate_incoming_std,Concentrate_outgoing_max,Concentrate_incoming_max,Num_Flow,Num_Packet_flow_avg,Num_Packet_flow_std,Num_Packet_flow_max,Num_Packet_flow_median,First30_incoming,First30_outgoing,Last30_incoming,Last30_outgoing,Packet_Second_avg,Packet_Second_std,Packet_Second_median,Packet_Second_min,Packet_Second_max,Flow_duration_avg,Flow_duration_std,Flow_duration_median,Flow_duration_min,Flow_duration_max,Flow_duration_1stQuartile,Flow_duration_3rdQuartile,Packet_Interval_avg,Packet_Interval_std,Packet_Interval_max,Packet_Interval_min,Packet_Interval_median,Packet_outgoing_Interval_avg,Packet_outgoing_Interval_std,Packet_outgoing_Interval_max,Packet_outgoing_Interval_median,Packet_outgoing_Interval_min,Packet_incoming_Interval_avg,Packet_incoming_Interval_std,Packet_incoming_Interval_max,Packet_incoming_Interval_median,Packet_incoming_Interval_min".split(',')
def WriteFile(out,outputdir):
	filepath = os.path.join(outputdir,"hist.csv")
	with open(filepath,'w') as fw:
		for k,v in out.items():
			t = [str(x) for x in v]
			data = str(k) + ',' + ','.join(t)
			fw.write(data+"\n")


def getFeatures(filepath,feature):
	l = []
	try:
		with open(filepath,'r') as f:
			reader = csv.DictReader(f)
			for line in reader:
				l.append(float(line[feature]))
	except Exception as e:
		print("error message : ",filepath,feature)
	return -1 if len(l) == 0 else sum(l) / len(l)

###########################
# handle border, interval #
###########################
# def DrawGraph(out,outputdir):
# 	for k,v in out.items():
# 		plt.title(k)
# 		plt.xlabel('Value')
# 		plt.ylabel('Number of website')
# 		if max(v) - min(v) > 1000:
# 			interval = (max(v) - min(v)) // 100
# 		elif max(v) - min(v) > 100:
# 			interval = (max(v) - min(v)) // 10
# 		else:
# 			interval = 1
# 		plt.xlim([int(min(v)),int(max(v))])
# 		binlist = [x for x in range(int(min(v)),int(max(v)),interval)]
# 		plt.hist(v,bins=binlist)
# 		plt.savefig(os.path.join(outputdir,k+".jpg"))
# 		plt.clf()


def ReadAllFeatures(inputdir):
	out = dict()
	for domain in os.listdir(inputdir):
		if domain.endswith(".csv"):
			filepath = os.path.join(inputdir,domain)
			for h in headerlist:
				if h not in out:
					out[h] = []
				out[h].append(getFeatures(filepath,h))
	return out


def parseCommand():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputdir','-i',type=str,default=None, help='input traces dir, EX: traces')
	parser.add_argument("--outputdir",'-o',type=str,required=True, help='outputdir')
	args = parser.parse_args()
	if args.test == False and args.inputdir == None:
		print("At least testfile or inputdir argument should be specified")
		return 0
	if args.test != False and args.inputdir != None:
		print("only one of the argument: testfile, inputdir could have value")	
		return 0
	return args

def main():
	args = parseCommand()
	if args == 0:
		return 0
	out = ReadAllFeatures(args.inputdir)
	WriteFile(out,args.outputdir)

if __name__ == "__main__":
	main()