from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, BatchNormalization
from keras.layers.core import Activation, Flatten, Dense, Dropout
from keras.layers.advanced_activations import ELU
from keras.initializers import glorot_uniform
import pickle, os, sys, argparse
import numpy as np
sys.path.append('../')
import DFConfig as cm
from randomForrest import writeLog
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from keras import backend as K
from keras.optimizers import Adamax
from keras import callbacks

# remove packetlen < 0.8 * median
# remove traffic with median less than 80 cells
def RemovedFailedSample(tmp):
    datalenList,t = [],[]
    for ele in tmp:
        datalenList.append(sum([abs(x) for x in ele]))
        datalenList = np.array(datalenList)
        med = np.percentile(datalenList,50)
        if med < 80:
            return []
        for i in range(len(tmp)):
            if sum([abs(x) for x in tmp[i]]) > med * 0.8:
                if len(tmp[i]) > 5000:
                    t.append(tmp[i][:5000])
                else:
                    t.append(tmp[i])
        return t

def ReadData(dirpath,outputdir="",labeldict=[]):
    data = []
    label = []
    cnt = 0
    instancelist = dict()
    if labeldict == []:
        labelpath = os.path.join(outputdir,"labelmapping.txt")
        for domain in os.listdir(dirpath):
            if "DS_Store" not in domain:
                try:
                    filepath = os.path.join(dirpath,domain)
                    tmp = pickle.load(open(filepath,'rb'))
                    tmp = RemovedFailedSample(tmp)
                    if tmp == []:
                        print("Warning: domain %s has few packets"%(domain))
                    else:
                        label += [cnt] * len(tmp)
                        data += (tmp)
                        writeLog("mapping: %s -> %d"%(domain,cnt),labelpath)
                        cnt += 1
                        instancelist[domain] = len(tmp)
                except Exception as e:
                    print("[train.py error]ReadData, failed to read pickle",domain)
    else:
        for k in labeldict.keys():
            try:
                filepath = os.path.join(dirpath,k)
                tmp = pickle.load(open(filepath,'rb'))
            except Exception as e:
                print("[ReadData error] filepath not found: ",filepath)
                print(str(e))
            try:
                tmp = RemovedFailedSample(tmp)
                if tmp == []:
                    print("Warning: domain %s has few packets"%(k))
                else:
                    label += [labeldict[k]] * len(tmp)
                    data += (tmp)
                    instancelist[k] = len(tmp)
            except Exception as e:
                print("[train.py error]ReadData, failed to read pickle",domain)
    print({k: v for k, v in sorted(instancelist.items(), key=lambda item: item[1])})
    return shuffle(data,label)

def findBestModel(dirpath):
    BestModel = 0
    value = -1
    for file in os.listdir(dirpath):
        if file.endswith("hdf5"):
            if int(file.split('.')[1]) > value:
                BestModel = file
                value = int(file.split('.')[1])
    return os.path.join(dirpath,BestModel)

def FindNumOfClass(dirpath):
    cnt = 0
    try:
        with open(os.path.join(dirpath,"labelmapping.txt"),'r') as f:
            for line in f:
                cnt = int(line.strip().split(' ')[-1])
    except Exception as e:
        print("[train.py] error in FindNumOfClass,",str(e))
    return cnt

def ReadLabel(labeldir):
    d = dict()
    labelpath = os.path.join(labeldir,"labelmapping.txt")
    try:
        with open(labelpath,'r') as f:
            for line in f:
                line = line.strip().split(' ')
                domain = line[1]
                cnt = int(line[-1])
                d[domain] = cnt
    except Exception as e:
        print("[train.py error] ReadLabel failed...",str(e))
    return d

class DFNet:
    def __init__(self,classes):
        input_shape = (cm.LENGTH,1)
        print("num of classes: ",classes)
        model = Sequential()
        #Block1
        filter_num = ['None',32,64,128,256]
        kernel_size = ['None',8,8,8,8]
        conv_stride_size = ['None',1,1,1,1]
        pool_stride_size = ['None',4,4,4,4]
        pool_size = ['None',8,8,8,8]

        model.add(Conv1D(filters=filter_num[1], kernel_size=kernel_size[1], input_shape=input_shape,
                         strides=conv_stride_size[1], padding='same',
                         name='block1_conv1'))
        model.add(BatchNormalization(axis=-1))
        model.add(ELU(alpha=1.0, name='block1_adv_act1'))
        model.add(Conv1D(filters=filter_num[1], kernel_size=kernel_size[1],
                         strides=conv_stride_size[1], padding='same',
                         name='block1_conv2'))
        model.add(BatchNormalization(axis=-1))
        model.add(ELU(alpha=1.0, name='block1_adv_act2'))
        model.add(MaxPooling1D(pool_size=pool_size[1], strides=pool_stride_size[1],
                               padding='same', name='block1_pool'))
        model.add(Dropout(0.1, name='block1_dropout'))

        model.add(Conv1D(filters=filter_num[2], kernel_size=kernel_size[2],
                         strides=conv_stride_size[2], padding='same',
                         name='block2_conv1'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='block2_act1'))

        model.add(Conv1D(filters=filter_num[2], kernel_size=kernel_size[2],
                         strides=conv_stride_size[2], padding='same',
                         name='block2_conv2'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='block2_act2'))
        model.add(MaxPooling1D(pool_size=pool_size[2], strides=pool_stride_size[3],
                               padding='same', name='block2_pool'))
        model.add(Dropout(0.1, name='block2_dropout'))

        model.add(Conv1D(filters=filter_num[3], kernel_size=kernel_size[3],
                         strides=conv_stride_size[3], padding='same',
                         name='block3_conv1'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='block3_act1'))
        model.add(Conv1D(filters=filter_num[3], kernel_size=kernel_size[3],
                         strides=conv_stride_size[3], padding='same',
                         name='block3_conv2'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='block3_act2'))
        model.add(MaxPooling1D(pool_size=pool_size[3], strides=pool_stride_size[3],
                               padding='same', name='block3_pool'))
        model.add(Dropout(0.1, name='block3_dropout'))

        model.add(Conv1D(filters=filter_num[4], kernel_size=kernel_size[4],
                         strides=conv_stride_size[4], padding='same',
                         name='block4_conv1'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='block4_act1'))
        model.add(Conv1D(filters=filter_num[4], kernel_size=kernel_size[4],
                         strides=conv_stride_size[4], padding='same',
                         name='block4_conv2'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='block4_act2'))
        model.add(MaxPooling1D(pool_size=pool_size[4], strides=pool_stride_size[4],
                               padding='same', name='block4_pool'))
        model.add(Dropout(0.1, name='block4_dropout'))

        model.add(Flatten(name='flatten'))
        model.add(Dense(512, kernel_initializer=glorot_uniform(seed=0), name='fc1'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='fc1_act'))

        model.add(Dropout(0.7, name='fc1_dropout'))

        model.add(Dense(512, kernel_initializer=glorot_uniform(seed=0), name='fc2'))
        model.add(BatchNormalization())
        model.add(Activation('relu', name='fc2_act'))

        model.add(Dropout(0.5, name='fc2_dropout'))

        model.add(Dense(classes, kernel_initializer=glorot_uniform(seed=0), name='fc3'))
        model.add(Activation('softmax', name="softmax"))
        self.model = model
    def Training(self,trainx,trainy,outputdir):
        OPTIMIZER = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0) # Optimizer
        self.model.compile(loss='categorical_crossentropy',optimizer=OPTIMIZER,metrics=["accuracy"])
        self.model.fit(trainx,trainy,batch_size=cm.batch_size,epochs=cm.epochs,validation_split=0.1,shuffle=True,verbose=cm.verbose,callbacks=self.callbacklist)
    def CallbackList(self,outputdir):
        filepath=os.path.join(outputdir,"model{epoch:03d}-{val_accuracy:.3f}.hdf5")
        Checkpoint = callbacks.ModelCheckpoint(filepath, monitor='val_accuracy', save_best_only=True, mode='max', period=1,save_weights_only=True)
        batch_print_callback = callbacks.LambdaCallback(
        on_epoch_end=lambda batch, logs: print(
            'Epoch[%d] Train-accuracy=%f  Epoch[%d] Validation-accuracy=%f' %(batch, logs['accuracy'], batch, logs['val_accuracy'])))
        self.callbacklist = [Checkpoint,batch_print_callback]
    def Testing(self,x1_test,y1_test):
        score_test = self.model.evaluate(x1_test, y1_test, verbose=cm.verbose)
        print("Testing accuracy:", score_test)
    def loadmodel(self,dirpath):
        modelpath = findBestModel(dirpath)
        print("Best model = ",modelpath)
        ycnt = FindNumOfClass(dirpath)
        self.model.build(ycnt)    #tmp, to create same number of classes
        self.model.load_weights(modelpath)
    def testResult(self,labelpath,datapath,outputdir="./"):
        labeldict = ReadLabel(labelpath)
        x1,y1 = ReadData(datapath,"",labeldict)
        x1 = np.array(x1)
        x1 = x1[:, :,np.newaxis]
        y1 = np_utils.to_categorical(y1,max(y1)+1)
        x1_train, x1_test, y1_train, y1_test = train_test_split(x1,y1,test_size=0.4, stratify=y1)
        ans = self.model.predict(x1_test)
        ans = ans.argmax(axis=-1)
        correct,wrong = 0,0
        for i in range(len(ans)):
            if ans[i] == np.where(y1_test[0]==1)[0][0]:
                correct += 1
            else:
                wrong += 1
        print("Accuracy = %f"%(correct/(correct+wrong)))
        outputpath = os.path.join(outputdir,"%s-%s.txt"%(labelpath.strip().split('/')[-2],datapath.strip().split('/')[-2]))
        with open(outputpath,'w') as fw:
            fw.write("Accuracy = %f"%(correct/(correct+wrong)))

def parseCommand():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputdir','-i',type=str,default=None, help='Direcotry of Features, EX: directory path of TrafficResult-3')
    parser.add_argument('--outputdir','-o',type=str,default="./", help='path of output Directory')
    parser.add_argument("--test",'-t',action='store_true')
    parser.add_argument("--data1",'-d1',type=str,help="only used when test specified, modelpath of tested version")
    parser.add_argument("--data2",'-d2',type=str,help="only used when test specified, tested datapath of dataset")
    # parser.add_argument('--all','-a',type=str,action='store_true')
    args = parser.parse_args()
    if args.inputdir == None and args.test==False:
        print("inputdir argument should be specified")
        return 0
    return args

def main(args):
    if args.test == True:
        ycnt = FindNumOfClass(args.data1)
        df = DFNet(ycnt+1)
        df = df.loadmodel(args.data1)
        df.testResult(args.data1,args.data2,args.outputdir)
    else:
        x1,y1 = ReadData(args.inputdir,args.outputdir)
        x1 = np.array(x1)
        x1 = x1[:, :,np.newaxis]
        y1 = np_utils.to_categorical(y1,max(y1)+1)
        x1_train, x1_test, y1_train, y1_test = train_test_split(x1,y1,test_size=0.1, stratify=y1)
        dfnet = DFNet(len(y1_train[0]))
        dfnet.CallbackList(args.outputdir)
        dfnet.Training(x1_train,y1_train,args.outputdir)
        dfnet.Testing(x1_test,y1_test)
        testdatapath = os.path.join(args.outputdir,"testdata.pkl")
        labeldatapath = os.path.join(args.outputdir,"labeldata.pkl")
        pickle.dump(x1_test,open(testdatapath,"wb"))
        pickle.dump(y1_test,open(labeldatapath,"wb"))

if __name__ == '__main__':
    args = parseCommand()
    main(args)