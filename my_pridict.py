import  my_inference
import audio_processing
import tensorflow as tf
import my_train
import numpy as np
import os

test_ckpt_path="model0726/hs_model-26001.meta"
ckpt_path="model0726/hs_model-26001"

predictions_map=['normal','extrahls','artifact','extrastole','murmur']

# saver = tf.train.import_meta_graph('MNIST_model/mnist_model-240001.meta')
# saver.restore(sess, tf.train.latest_checkpoint('MNIST_model/'))



def pridict(sess,features):
    '''
            This function is used to pridict the test data. Please finish pre-precessing in advance

            :param test_image_array: 2D numpy array with shape [num_pridict, 577]
            :return: the softmax probability with shape [num_pridict, num_labels]
            '''


    #x = tf.placeholder(tf.float32, [None, my_inference.INPUT_NODE], name='x-input')


    # Initialize a new session and restore a checkpoint
    #saver = tf.train.Saver(tf.all_variables())
    graph=tf.get_default_graph()
    x_in = graph.get_operation_by_name('x-input').outputs[0]
    y_in = graph.get_operation_by_name('y-input').outputs[0]
    keep_in = graph.get_operation_by_name('keep_prob').outputs[0]
    predictions=tf.get_collection("predicts")[0]
    pre = sess.run(predictions, feed_dict={x_in: features,y_in: (np.array([0,0,0,0,0])).reshape(-1,5),keep_in:1})[0]

    return pre

def predict_wav(sess,filename):
    features=audio_processing.extract_feature(filename)
    features=np.concatenate(features,0)
    # features = guiyi(features).astype('float32')
    features = np.reshape(features, [-1, 577])
    pro = pridict(sess,features)
    return pro

def guiyi(linedata):
    linedata[0:40] = [x - min(linedata[0:40]) for x in linedata[0:40]]
    linedata[0:40] = [x / (max(linedata[0:40]) - min(linedata[0:40])) for x in linedata[0:40]]
    linedata[40:52] = [x - min(linedata[40:52]) for x in linedata[40:52]]
    linedata[40:52] = [x / (max(linedata[40:52]) - min(linedata[40:52])) for x in linedata[40:52]]
    linedata[52:180] = [x - min(linedata[52:180]) for x in linedata[52:180]]
    linedata[52:180] = [x / (max(linedata[52:180]) - min(linedata[52:180])) for x in linedata[52:180]]
    linedata[180:187] = [x - min(linedata[180:187]) for x in linedata[180:187]]
    linedata[180:187] = [x / (max(linedata[180:187]) - min(linedata[180:187])) for x in linedata[180:187]]
    linedata[187:193] = [x - min(linedata[187:193]) for x in linedata[187:193]]
    linedata[187:193] = [x / (max(linedata[187:193]) - min(linedata[187:193])) for x in linedata[187:193]]
    linedata[193:] = [x - min(linedata[193:]) for x in linedata[193:]]
    linedata[193:] = [x / (max(linedata[193:]) - min(linedata[193:])) for x in linedata[193:]]
    return linedata

def predict_wav_list(sess,wav_list):
    for wav in wav_list:
        pre_pro = predict_wav(sess, wav).tolist()
        print("hear sound：："+wav+"\tprob：\t"+str(pre_pro))
        print("prindictions:\t" + predictions_map[pre_pro.index(max(pre_pro))])

def predict_wav_indir(sess,dir,first=False):
    if first:
        mode='w'
    else:
        mode='a+'
    out_file = open('pre_pro1.txt',mode)
    for file in os.listdir(dir):
        pre_pro = predict_wav(sess, dir+file).tolist()
        if(max(pre_pro)<0.35):
            index=2
        else:
            index=pre_pro.index(max(pre_pro))
        out_file.write(file+'\t\t'+predictions_map[index]+"\tprob：\t"+str(pre_pro)+"\n")


if __name__=='__main__':
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(test_ckpt_path)
        saver.restore(sess, ckpt_path)
        print('Model restored from: '+test_ckpt_path)

        #预测文件夹
        dir = ['../dataset3/extrastole/','../dataset3/murmur/','../dataset3/artifact/','../dataset3/normal/','../dataset3/extrahls/']
        for i in range(len(dir)):
            predict_wav_indir(sess,dir[i],first=(i==0))
        # 具体某一病例#具体某一病例
        # predict_wav_list(sess,
        #                  [
        #                      "wav/normal__201105011626.wav",
        #                      "wav/extrahls__201101161027.wav",
        #                      "wav/artifact__201106040947.wav",
        #                      "wav/murmur__201101051114.wav"
        #                  ])
