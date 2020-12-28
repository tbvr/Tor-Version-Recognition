import matplotlib.pyplot as plt

import csv,os
inputdir = '/mnt/c/Users/LICON/nslab/WF-Result/settings/20201221/removeFailed'
outputdir = '/mnt/c/Users/LICON/nslab/WF-Result/setting-visualize/'

targetFeature = ["Num_outgoinging_packet"]
urllist = ["icloud.com", "slideshare.net", "medium.com", "oracle.com"]

visualize = dict()

VersionList = ["nocontentblock","contentblock"]
versiondir = os.path.join(inputdir,'normal')
for domain in os.listdir(versiondir):
    domaindata = dict({domain:dict()})
    for feature in targetFeature:
        domaindata[domain][feature] = [[],[]]
    if domain.endswith('.csv'):
        cnt = 0
        for version in VersionList:
            filepath = os.path.join(inputdir,version,domain)
            try:
                with open(filepath,'r') as f:
                    reader = csv.DictReader(f)
                    for line in reader:
                        for feature in targetFeature:
                            domaindata[domain][feature][cnt].append(int(line[feature]))
            except Exception as e:
                print("Error domain:",domain)
                pass
            finally:
                cnt += 1
    if domain[:-4] in urllist:
        visualize[domain[:-4]] = [domaindata[domain][feature][0],domaindata[domain][feature][1]]


# function for setting the colors of the box plots pairs
def setBoxColors(bp,domain=""):
    try:
        plt.setp(bp['boxes'][0], color='blue')
        plt.setp(bp['caps'][0], color='blue')
        plt.setp(bp['caps'][1], color='blue')
        plt.setp(bp['whiskers'][0], color='blue')
        plt.setp(bp['whiskers'][1], color='blue')
        plt.setp(bp['fliers'][0], color='blue')
        plt.setp(bp['fliers'][1], color='blue')
        plt.setp(bp['medians'][0], color='blue')
        plt.setp(bp['boxes'][1], color='red')
        plt.setp(bp['caps'][2], color='red')
        plt.setp(bp['caps'][3], color='red')
        plt.setp(bp['whiskers'][2], color='red')
        plt.setp(bp['whiskers'][3], color='red')
        plt.setp(bp['fliers'][2], color='red')
        plt.setp(bp['fliers'][3], color='red')
        plt.setp(bp['medians'][1], color='red')
    except Exception as e:
        print("error: ",e)

# Some fake data to plot
# A= [[1, 2, 5,],  [7, 2]]
# B = [[5, 7, 2, 2, 5], [7, 2, 5]]
# C = [[3,2,5,7], [6, 7, 3]]
position = [1.3,3.3,5.3,7.3]

fig,ax = plt.subplots()
plt.suptitle("Amount of outgoinging Packet", fontsize=12)
plt.ylabel("Amount of Packets",fontsize=12)
# first boxplot pair
bp = plt.boxplot(visualize['icloud.com'], positions = [position[0]-0.4, position[0]+0.4], widths = 0.6)
setBoxColors(bp)

# second boxplot pair
bp = plt.boxplot(visualize['slideshare.net'], positions = [position[1]-0.4, position[1]+0.4], widths = 0.6)
setBoxColors(bp)

# thrid boxplot pair
bp = plt.boxplot(visualize['medium.com'], positions = [position[2]-0.4, position[2]+0.4], widths = 0.6)
setBoxColors(bp,domain="indeed.com")

bp = plt.boxplot(visualize['oracle.com'], positions = [position[3]-0.4, position[3]+0.4], widths = 0.6)
setBoxColors(bp)

# set axes limits and labels
# xlim(0,9)
# ylim(0,9)
ax.set_xticklabels(["icloud.com", "slideshare.net", "medium.com", "oracle.com"],fontsize=10, ha='center',rotation=10)
ax.set_xticks(position)

# draw temporary red and blue lines and use them to create a legend
hB, = plt.plot([1,1],'b-')
hR, = plt.plot([1,1],'r-')
plt.legend((hB, hR),('content blocking disabled', 'Content blocking enabled'))
hB.set_visible(False)
hR.set_visible(False)

plt.savefig('/mnt/c/Users/LICON/nslab/WF-Result/setting-visualize/figure7.png')
# plt.show()

