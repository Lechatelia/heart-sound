import  my_inference
import audio_processing
import tensorflow as tf
import mnist_train
import numpy as np
import socket
import time
import my_pridict
from sever import Server
import mysql

test_ckpt_path="model0726/hs_model-81001.meta"
ckpt_path="model0726/hs_model-81001"

predictions_map=['normal','extrahls','artifact','extrastole','murmur']
predict_wav_dir=[]

# saver = tf.train.import_meta_graph('MNIST_model/mnist_model-240001.meta')
# saver.restore(sess, tf.train.latest_checkpoint('MNIST_model/'))

import socket
import time
import threading
import datetime
# import server_predict
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
#
# # s.bind(('192.168.1.103', 6666))  # 绑定本机IP和任意端口(>1024)
# s.bind(('127.0.0.1', 6666))  # 绑定本机IP和任意端口(>1024)
#
# s.listen(1)  # 监听，等待连接的最大数目为1
#
# print('Server is running...')


class Server():
    def __init__(self,ip,port,sess):
        self.wav_length=32812
        # self.wav_length=10
        self.sess=sess
        self.s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)  # 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('192.168.1.103', 6666))  # 绑定本机IP和任意端口(>1024)
        self.s.bind((ip, port))  # 绑定本机IP和任意端口(>1024)
        self.s.listen(1)  # 监听，等待连接的最大数目为1
        print('Server is running...waitting a connection')
        self.sock, self.addr = self.s.accept()  # 接收一个新连接
        print('Accept new connection from %s:%s.' % self.addr)  # 接受新的连接请求
        # TCP(sock, addr)  # 处理连接

    def reset(self,ip,port,sess):
        self.s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)  # 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # s.bind(('192.168.1.103', 6666))  # 绑定本机IP和任意端口(>1024)
        self.s.bind((ip, port))  # 绑定本机IP和任意端口(>1024)
        self.s.listen(1)  # 监听，等待连接的最大数目为1
        print('Server is reset...waitting a connection')
        self.sock, self.addr = self.s.accept()  # 接收一个新连接
        print('Accept new connection from %s:%s.' % self.addr)  # 接受新的连接请求
        # TCP(sock, addr)  # 处理连接

    def receive_wav(self,wav_name):
        # Length=32000
        Length = self.wav_length
        length = 0
        counter=0
        with open(wav_name, 'wb') as f:
            while (length < Length):
                # data = self.sock.recv(5000)  # 接受其数据

                self.s.settimeout(2)
                try:
                    data = self.sock.recv(1024)  # 接受其数据
                except socket.timeout:
                    print("time out")
                    for i in range(Length-length):
                        f.write(chr(0x00).encode())
                    print(str(length ))
                    print(str(len(data)))
                    break
                except ConnectionResetError:
                    # self.reset()
                    self.sock.close()  # 关闭连接
                    print('ConnectionResetError')
                    print(str(length))
                    print(str(len(data)))

                    break
                if data:
                    # if not data or data.decode() == 'quit':  # 如果数据为空或者'quit'，则退出
                    #     break
                    print("receiced:\t")
                    print(len(data))
                    f.write(data)
                    length += len(data)
                    # time.sleep(0.001)
                    if length == Length:
                        f.close()
                        break
                    else:
                        # pass
                        self.sock.send('get'.encode())
                        print('get')
                        # if counter%4==0:
                        #     self.sock.send('get'.encode())
                        #     print('get')
                        # counter=counter+1

                    # print(data.decode('utf-8'))
                    # sock.send(data.decode('utf-8').upper().encode())  # 发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')
                else:
                    self.sock.close()  # 关闭连接
                    print('Connection from %s:%s closed.' % self.addr)
                    break
            print('transmit ok')

    def close(self):
        self.s.close()

    def event_judge(self,pridict=False):
        while(1):
            try:
                data=self.sock.recv(1024)
            except OSError:
                print('Connection Error from socket %s:%s .' % self.addr)
                self.sock.close()
                break
            else:
                if not data:
                    print('Connection from %s:%s closed.' % self.addr)
                    self.sock.close()
                    break
                elif data.decode('utf-8')=='wav_start':
                    self.sock.send('wav_start'.encode())
                    print('wav_start')
                    # receive ID

                    id =self.sock.recv(1024)
                    while(id.decode('utf-8')=='wav_start'):
                        id = self.sock.recv(1024)
                    self.sock.send(id)
                    # receive wav
                    time = str(datetime.datetime.now()).split('.')[0].replace(':','_')
                    self.receive_wav('{name}.wav'.format(name=time))
                    if pridict:
                        pre_pro=predict_wav(self.sess,'{name}.wav'.format(name=time))
                        # pre_pro=predict_wav(self.sess,"wav/normal__201105011626.wav")
                        diagnosis=predictions_map[pre_pro.index(max(pre_pro))]
                        print(diagnosis)
                        if(max(pre_pro)==1):
                            possibility=0.9999
                        else:
                            possibility=max(pre_pro)
                        result='result{0}{1:*<4}'.format(str(pre_pro.index(max(pre_pro))+1),str(possibility*10000).split('.')[0])
                        try:
                            self.sock.send(result.encode())
                        except OSError:
                            print('不够就结束啦')
                            break
                        print(result)
                    print(time)
                    # 在局域网下无法使用
                    mysql.Add_Diagnosis_to_SQL(int(id),diagnosis,max(pre_pro),wav_dir='{name}.wav'.format(name=time))
                    if(self.sock.recv(1024).decode('utf-8')=='wav_end'):
                        self.sock.send('wav_end'.encode())
                        print('wav end')
                    else :
                        print("communication error: wav_end")

                elif data.decode('utf-8')=='acquire_info':
                    print('acquire_info start')
                    self.sock.send('acquire_info'.encode())
                    id=int(self.sock.recv(1024))
                    self.sock.send( mysql.Acquire_Info_by_ID(id).encode())
                    if(self.sock.recv(1024).decode('utf-8')=='info_end'):
                        self.sock.send('info_end'.encode())
                        print('info end')
                    else :
                        print("communication error: info_end")

                elif data.decode('utf-8')=='get_time':
                    print('get_time start')
                    self.sock.send( str(datetime.datetime.now()).encode())
                    if(self.sock.recv(1024).decode('utf-8')=='time_end'):
                        self.sock.send('time_end'.encode())
                        print('time end')
                    else :
                        print("communication error: info_end")

                elif data.decode('utf-8')=='ID_update':
                    print('ID update')
                    idname=mysql.Update_all_name_id_by_str()
                    self.sock.send(('ID_'+str(len(idname))).encode())
                    if (self.sock.recv(1024).decode('utf-8') == 'ready'):
                        self.sock.send(self.strlist_2_one_str(idname).encode())
                        # for i in idname:
                            # self.sock.send(i.encode())
                    else:
                        print("no ready end")
                    if(self.sock.recv(1024).decode('utf-8')=='update_end'):
                        self.sock.send('update_end'.encode())
                        print('ID update end')
                    else :
                        print("communication error: update_end")
                else:
                    print('unknown messsge:\t{mess}'.format(mess=data.decode('utf-8')))

    def strlist_2_one_str(self, list):
        str = ''
        if len(list) == 0:
            return 'blank'
        for i in list:
            str = str + i
        return str


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
    features = audio_processing.extract_feature(filename)
    features = np.concatenate(features, 0)
    # features = guiyi(features).astype('float32')
    features = np.reshape(features, [-1, 577])
    pro = pridict(sess, features)
    return pro.tolist()

# def guiyi(linedata):
#     linedata[0:40] = [x - min(linedata[0:40]) for x in linedata[0:40]]
#     linedata[0:40] = [x / (max(linedata[0:40]) - min(linedata[0:40])) for x in linedata[0:40]]
#     linedata[40:52] = [x - min(linedata[40:52]) for x in linedata[40:52]]
#     linedata[40:52] = [x / (max(linedata[40:52]) - min(linedata[40:52])) for x in linedata[40:52]]
#     linedata[52:180] = [x - min(linedata[52:180]) for x in linedata[52:180]]
#     linedata[52:180] = [x / (max(linedata[52:180]) - min(linedata[52:180])) for x in linedata[52:180]]
#     linedata[180:187] = [x - min(linedata[180:187]) for x in linedata[180:187]]
#     linedata[180:187] = [x / (max(linedata[180:187]) - min(linedata[180:187])) for x in linedata[180:187]]
#     linedata[187:193] = [x - min(linedata[187:193]) for x in linedata[187:193]]
#     linedata[187:193] = [x / (max(linedata[187:193]) - min(linedata[187:193])) for x in linedata[187:193]]
#     linedata[193:] = [x - min(linedata[193:]) for x in linedata[193:]]
#     linedata[193:] = [x / (max(linedata[193:]) - min(linedata[193:])) for x in linedata[193:]]
#     return linedata

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


        # s = socket.socket(socket.AF_INET,
        #                   socket.SOCK_STREAM)  # 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
        # s.bind(('127.0.0.1', 6666))  # 绑定本机IP和任意端口(>1024)
        # s.listen(1)  # 监听，等待连接的最大数目为1
        # print('Server is running...')
        #
        # while True:
        #     sock, addr = s.accept()  # 接收一个新连接
        #     TCP(sock, addr,sess)  # 处理连接
        while True:
            my_server = Server('192.168.1.102', 6666,sess)
            # my_server = Server('localhost', 6666,sess)
            my_server.event_judge(pridict=True)
            print('you can now disconnect connection ')
            my_server.close()
            time.sleep(1)




