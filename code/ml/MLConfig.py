##################
# Random forrest #
#################
n_threshold = 80	# only retrieve websites that have amount of traffic instaces > n_threshold
k_fold = 5 			# k-fold cross validation
njobs = 3			# parllel workers for random forrest
testingsize = 0.1 	# size of testing size(0 to 1) -> train_test_split
Trees = 100			# number of trees for random forrest

versionList = ['7','8','9']

######################
# Grandient Boosting #
######################
GBparams = {
    'n_estimators': 120,
    'max_depth': 3,
    'learning_rate': 0.05,
    'criterion': 'mse',
    'verbose':1
}

CellFeature = {
	"Num_Packet":-1,
	"Num_outgoinging_packet":-1,
	"Num_incoming_packet":-1,
	"outgoing_ratio":-1,
	"incoming_ratio":-1,
	"std_outgoing_packetOrder":-1,
	"avg_outgoing_packetOrder":-1,
	"std_incoming_packetOrder":-1,
	"avg_incoming_packetOrder":-1,
	"Concentrate_outgoing_avg":-1,	# concentrate the outgoing packet(find peak)
	"Concentrate_incoming_avg":-1,
	"Concentrate_outgoing_std":-1,	# concentrate the outgoing packet(find peak)
	"Concentrate_incoming_std":-1,
	"Concentrate_outgoing_max":-1,	# concentrate the outgoing packet(find peak)
	"Concentrate_incoming_max":-1,
	"Num_Flow":-1,
	"Num_Packet_flow_avg":-1,	# average number of packet between direction changes
	"Num_Packet_flow_std":-1,
	"Num_Packet_flow_max":-1,
	"Num_Packet_flow_median":-1,
	"First30_incoming":-1,	# first 30 packets: num of incoming
	"First30_outgoing":-1,	# first 30 packets: num of outgoing
	"Last30_incoming":-1,	# last 30 packets: num of incoming
	"Last30_outgoing":-1,		# last 30 packets: num of outgoing
	"burst_avg":-1,
	"burst_std":-1,
	"burst_max":-1,
	"burst_min":-1,
	"burst_median":-1
}

TimeFeature = {
	"TotalTime":-1,
	"Packet_Second_avg":-1,		# packet per second
	"Packet_Second_std":-1,
	"Packet_Second_median":-1,
	"Packet_Second_min":-1,
	"Packet_Second_max":-1,
	"Flow_duration_avg":-1,
	"Flow_duration_std":-1,
	"Flow_duration_median":-1,
	"Flow_duration_min":-1,
	"Flow_duration_max":-1,
	"Flow_duration_1stQuartile":-1,
	"Flow_duration_3rdQuartile":-1,
	"Packet_Interval_avg":-1,
	"Packet_Interval_std":-1,
	"Packet_Interval_max":-1,
	"Packet_Interval_min":-1,
	"Packet_Interval_median":-1,
	"Packet_Interval_3rdQuartile":-1,
	"Packet_outgoing_Interval_avg":-1,
	"Packet_outgoing_Interval_std":-1,
	"Packet_outgoing_Interval_max":-1,
	"Packet_outgoing_Interval_median":-1,
	"Packet_outgoing_Interval_min":-1,
	"Packet_outgoing_Interval_3rdQuartile":-1,
	"Packet_incoming_Interval_avg":-1,
	"Packet_incoming_Interval_std":-1,
	"Packet_incoming_Interval_max":-1,
	"Packet_incoming_Interval_median":-1,
	"Packet_incoming_Interval_min":-1,
	"Packet_incoming_Interval_3rdQuartile":-1,
	'wavelet_All_Interval_avg_ca':-1,
	'wavelet_All_Interval_std_ca':-1,
	'wavelet_All_Interval_max_ca':-1,
	'wavelet_All_Interval_min_ca':-1,
	'wavelet_All_Interval_median_ca':-1,
	'wavelet_incoming_Interval_avg_ca':-1,
	'wavelet_incoming_Interval_std_ca':-1,
	'wavelet_incoming_Interval_max_ca':-1,
	'wavelet_incoming_Interval_min_ca':-1,
	'wavelet_incoming_Interval_median_ca':-1,
	'wavelet_outgoing_Interval_avg_ca':-1,
	'wavelet_outgoing_Interval_std_ca':-1,
	'wavelet_outgoing_Interval_max_ca':-1,
	'wavelet_outgoing_Interval_min_ca':-1,
	'wavelet_outgoing_Interval_median_ca':-1,
	'wavelet_All_Interval_avg_cd':-1,
	'wavelet_All_Interval_std_cd':-1,
	'wavelet_All_Interval_max_cd':-1,
	'wavelet_All_Interval_min_cd':-1,
	'wavelet_All_Interval_median_cd':-1,
	'wavelet_incoming_Interval_avg_cd':-1,
	'wavelet_incoming_Interval_std_cd':-1,
	'wavelet_incoming_Interval_max_cd':-1,
	'wavelet_incoming_Interval_min_cd':-1,
	'wavelet_incoming_Interval_median_cd':-1,
	'wavelet_outgoing_Interval_avg_cd':-1,
	'wavelet_outgoing_Interval_std_cd':-1,
	'wavelet_outgoing_Interval_max_cd':-1,
	'wavelet_outgoing_Interval_min_cd':-1,
	'wavelet_outgoing_Interval_median_cd':-1,
	"Timestamp_All_1Quartile":0,
	"Timestamp_All_2Quartile":0,
	"Timestamp_All_3Quartile":0,
	"Timestamp_Incoming_1Quartile":0,
	"Timestamp_Incoming_2Quartile":0,
	"Timestamp_Incoming_3Quartile":0,
	"Timestamp_Outgoing_1Quartile":0,
	"Timestamp_Outgoing_2Quartile":0,
	"Timestamp_Outgoing_3Quartile":0
}

####################
# list of features #
####################
headerlist = []
for k in CellFeature.keys():
	headerlist.append(k)
for k in TimeFeature.keys():
	headerlist.append(k)