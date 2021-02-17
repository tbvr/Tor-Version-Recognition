from os.path import join
import tempfile

#############
# tor setup #
#############
driverpath = "/root/nslab/torbrowser_902"	# TBB browser path
TorProxypath = "/root/nslab/torbrowser_902"	# Tor proxy path
DEFAULT_TOR_BINARY_PATH = join(driverpath,"Browser/TorBrowser/Tor/tor")

##########################
# dataset and output dir #
##########################
BaseDir = "/root/nslab"
Datapath = join(BaseDir,"Data/Tranco_WebList.csv")	# closed-world dataset
OpenWorldDataPath = join(BaseDir,"Data/OpenWorld_WebList.csv")	# open-world dataset

pcapDir = join(BaseDir,"traces/")
ResultDir = join(BaseDir,"result")
netInterface = "eth0"
LogDir = join(BaseDir,"logs")
LogFile = join(LogDir,"log.txt")
ErrorFilePath = join(LogDir,'ErrorList.txt')
StreamFile = join(LogDir,"streamInfo.txt")
rawtrafficdir = join(BaseDir,'rawTraffic')

###################
# Feature Extract #
###################
StreamInfo = "logs/streamInfo.txt"

#########
# torrc #
#########
TorSocksPort = 9250

TorConfig = {
	'SocksPort': str(TorSocksPort),
	'ControlPort': str(9251),
	'MaxCircuitDirtiness': '600000',
	'UseEntryGuards': '0', # change entry node for every new connection
	'NumEntryGuards':'1',
	'DataDirectory':tempfile.mkdtemp()
}

TBprofile = {
	"javascript.enable": True
}

USE_STEM = 2  # use tor started with Stem
USE_RUNNING_TOR = 1  # use system tor or tor started with stem
MAX_SITES_PER_TOR_PROCESS = 200

VISITPAGE_TIMEOUT = 100
DURATION_VISIT_PAGE = 10
PAUSE_BETWEEN_SITES = 5
WAIT_IN_SITE = 10             # time to wait after the page loads

CLOST_STREAM_DURATION = 20 # close all stream in 20 sec
INSTANCE = 4
PAUSE_BETWEEN_INSTANCES = 4  # pause before visiting the same site (instances)

################
# Error handle #
################
TRYCNT = 3

#####################
# pcapParser config #
#####################
# version ip.v
# ihl: ip.hl
# protocol : ip.p
# ip.df, mf fregment
# tos: type of service
packetinfo = [
	"cnt","timestamp","srcip","dstip","id","ihl","protocol","tos","offset","packetlen",\
	"flags","srcport","dstport","seq","ack"
]

