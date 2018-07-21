import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
from my_dataset import My_DataSet
import  my_inference
import os
import xlrd
import numpy as np

input_number=577
output_number = 5


BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.2
LEARNING_RATE_DECAY = 0.999
REGULARIZATION_RATE = 0.000001
#REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 50000
MOVING_AVERAGE_DECAY = 0.9999
MODEL_SAVE_PATH="model0716/"
MODEL_NAME="mnist_model"

my_keep_prob=0.6

def vectorized_result(j):
    """将标签转化成网络的输出格式"""
    e = np.zeros(output_number)
    e[int(j)] = 1.0
    e=np.array(e)
    #print(e.shape)
    return e

def load_data():
    """从xls文件读取数据，并进行数据格式的转换"""

    traindata = []
    trainlabel=[]
    valdata = []
    vallabel=[]
    testdata = []
    testlabel=[]
    ExcelFile = xlrd.open_workbook(r'write.xlsx')
    print(ExcelFile.sheet_names())
    sheet = ExcelFile.sheet_by_index(0)
    print(sheet.nrows)
    for i in range(0, sheet.nrows):
        rows = sheet.row_values(i)
        # linedata=[float(x) for x in line]
        # linedata=[x- min(linedata) for x in linedata]
        # linedata=[x/(max(linedata)-min(linedata))for x in linedata]
        if (str(rows[2]) == 'artifact'):
            catedata = 2
        elif (str(rows[2]) == 'extrahls'):
            catedata = 1
        elif ((str(rows[2]) == 'normal')):
            catedata = 0
        elif ((str(rows[2]) == 'extrastole')):
            catedata = 3
        elif ((str(rows[2]) == 'murmur')):
            catedata = 4
        else:
            print("catedata is wrong\n")
            return

        # catedata=float(rows[3])-1
        linedata = rows[3:]
        # print(len(linedata))
        # linedata[0:40] = [x - min(linedata[0:40]) for x in linedata[0:40]]
        # linedata[0:40] = [x / (max(linedata[0:40]) - min(linedata[0:40])) for x in linedata[0:40]]
        # linedata[40:52] = [x - min(linedata[40:52]) for x in linedata[40:52]]
        # linedata[40:52] = [x / (max(linedata[40:52]) - min(linedata[40:52])) for x in linedata[40:52]]
        # linedata[52:180] = [x - min(linedata[52:180]) for x in linedata[52:180]]
        # linedata[52:180] = [x / (max(linedata[52:180]) - min(linedata[52:180])) for x in linedata[52:180]]
        # linedata[180:187] = [x - min(linedata[180:187]) for x in linedata[180:187]]
        # linedata[180:187] = [x / (max(linedata[180:187]) - min(linedata[180:187])) for x in linedata[180:187]]
        # linedata[187:193] = [x - min(linedata[187:193]) for x in linedata[187:193]]
        # linedata[187:193] = [x / (max(linedata[187:193]) - min(linedata[187:193])) for x in linedata[187:193]]
        # linedata[193:] = [x - min(linedata[193:]) for x in linedata[193:]]
        # linedata[193:] = [x / (max(linedata[193:]) - min(linedata[193:])) for x in linedata[193:]]
        if (np.random.rand(1) < 0.9):
            traindata.append((np.reshape(np.array(linedata), (input_number))))
            trainlabel.append(vectorized_result(catedata))
            if (np.random.rand(1) < 0.15):
                valdata.append(np.reshape(np.array(linedata), (input_number)))
                vallabel.append(vectorized_result(catedata))
        else:
            testdata.append(np.reshape(np.array(linedata), (input_number)))
            testlabel.append(vectorized_result(catedata))
    traindata=np.array(traindata)
    trainlabel=np.array(trainlabel)
    valdata=np.array(valdata)
    vallabel=np.array(vallabel)
    testdata=np.array(testdata)
    testlabel=np.array(testlabel)
    print('traindata_number='+str(traindata.shape)+'\n')
    print('trainlabel_number='+str(trainlabel.shape)+'\n')
    print('valdata=' + str(len(valdata)) + '\n')
    print('testdata=' + str(len(testdata))+ '\n')
    return traindata,trainlabel, valdata,vallabel, testdata,testlabel


def train(mnist, valdata, vallabel, testdata, testlabel):

    x = tf.placeholder(tf.float32, [None, my_inference.INPUT_NODE], name='x-input')
    y_ = tf.placeholder(tf.float32, [None, my_inference.OUTPUT_NODE], name='y-input')
    keep_prob = tf.placeholder(tf.float32,name='keep_prob')

    regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
    y = my_inference.inference(x, regularizer,keep_prob)
    predictions = tf.nn.softmax(y)
    tf.add_to_collection("predicts",predictions)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))  #用于精确度
    global_step = tf.Variable(0, trainable=False)


    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variables_averages_op = variable_averages.apply(tf.trainable_variables())
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    loss = cross_entropy_mean + tf.add_n(tf.get_collection('losses'))



    learning_rate = tf.train.exponential_decay(
        LEARNING_RATE_BASE,
        global_step,
        1000, LEARNING_RATE_DECAY,
        staircase=True)
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)

    with tf.control_dependencies([train_step, variables_averages_op]):
        train_op = tf.no_op(name='train')


    saver = tf.train.Saver(max_to_keep=10)
    with tf.Session() as sess:
       # print(os.getcwd())
        #saver = tf.train.import_meta_graph('MNIST_model/mnist_model-240001.meta')
        #saver.restore(sess, tf.train.latest_checkpoint('MNIST_model/'))
        tf.global_variables_initializer().run()

        max_test_accuracy = 0.0

        max_acc_index = 0

        for i in range(TRAINING_STEPS):
            xs, ys = mnist.next_batch(BATCH_SIZE)
            _, loss_value, step= sess.run([train_op, loss, global_step], feed_dict={x: xs, y_: ys,keep_prob:my_keep_prob})
            if i % 500 == 0:
                acc_1 = sess.run([accuracy], feed_dict={x: valdata, y_: vallabel,keep_prob:1.0})  #二者不参与反向传播
                acc_2 = sess.run([accuracy], feed_dict={x: testdata, y_: testlabel,keep_prob:1.0})
                if(float(acc_2[0])>max_test_accuracy):
                    max_test_accuracy=float(acc_2[0])
                    max_acc_index=i
                    saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)
                print("After %d step, train_loss  %g, val_acc is %g, test_acc is %g ,max_acc is %g,index: %d" % (step, loss_value, float(acc_1[0]),float(acc_2[0]),max_test_accuracy,max_acc_index))
            #if i % 1000 == 0:
                #saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)




def main(argv=None):
    traindata, trainlabel, valdata, vallabel, testdata, testlabel=load_data();
    #mnist = input_data.read_data_sets("../../../datasets/MNIST_data", one_hot=True)
    #train(mnist)

    my_data=My_DataSet(traindata,trainlabel)
    train(my_data, valdata, vallabel, testdata, testlabel)

if __name__ == '__main__':
    main()


