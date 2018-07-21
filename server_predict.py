import  my_inference
import audio_processing
import tensorflow as tf
import mnist_train
import numpy as np
import socket
import time

test_ckpt_path="MNIST_model/mnist_model-1001.meta"
ckpt_path="MNIST_model/mnist_model-1001"

predictions_map=['normal','extrahls','artifact','extrastole','murmur']
predict_wav_dir=[]

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
    features = guiyi(features).astype('float32')
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
    end=[]
    for wav in wav_list:
        pre_pro = predict_wav(sess, wav).tolist()
        print("hear sound：："+wav+"\tprob：\t"+str(pre_pro))
        print("prindictions:\t" + predictions_map[pre_pro.index(max(pre_pro))])
        end.append( predictions_map[pre_pro.index(max(pre_pro))])
    return end

def TCP(sock, addr,sess):  # TCP服务器端处理逻辑

    print('Accept new connection from %s:%s.' % addr)  # 接受新的连接请求

    while True:
        data = sock.recv(2048)  # 接受其数据
        time.sleep(1)  # 延迟
        if not data or data.decode() == 'quit':  # 如果数据为空或者'quit'，则退出
            break
        data=data.decode('utf-8')
        print(data)
        predict_wav_dir.append(data)
        end=predict_wav_list(sess,
                         [data
                         ])
        for pre_end in end:
            sock.send(pre_end.encode())  # 发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')
        # sock.send(data.decode('utf-8').upper().encode())  # 发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')

    sock.close()  # 关闭连接
    print('Connection from %s:%s closed.' % addr)


if __name__=='__main__':
    with tf.Session() as sess:
        saver = tf.train.import_meta_graph(test_ckpt_path)
        saver.restore(sess, ckpt_path)
        print('Model restored from: '+test_ckpt_path)


        s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)  # 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
        s.bind(('127.0.0.1', 6666))  # 绑定本机IP和任意端口(>1024)
        s.listen(1)  # 监听，等待连接的最大数目为1
        print('Server is running...')

        while True:
            sock, addr = s.accept()  # 接收一个新连接
            TCP(sock, addr,sess)  # 处理连接



