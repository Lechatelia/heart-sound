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
    def __init__(self,ip,port,sess=None):
        self.wav_length=10
        self.sess=sess
        self.s = socket.socket(socket.AF_INET,
                          socket.SOCK_STREAM)  # 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)

        # s.bind(('192.168.1.103', 6666))  # 绑定本机IP和任意端口(>1024)
        self.s.bind((ip, port))  # 绑定本机IP和任意端口(>1024)
        self.s.listen(1)  # 监听，等待连接的最大数目为1
        print('Server is running...')
        self.sock, self.addr = self.s.accept()  # 接收一个新连接
        print('Accept new connection from %s:%s.' % self.addr)  # 接受新的连接请求
        # TCP(sock, addr)  # 处理连接

    def receive_wav(self,wav_name):
        # Length=32000
        Length = self.wav_length
        length = 0
        with open(wav_name, 'wb') as f:
            while (length < Length):
                data = self.sock.recv(5000)  # 接受其数据
                if data:
                    # if not data or data.decode() == 'quit':  # 如果数据为空或者'quit'，则退出
                    #     break
                    print("receiced:\t")
                    print(len(data))
                    f.write(data)
                    length += len(data)
                    if length == Length:
                        f.close()
                        break
                    # print(data.decode('utf-8'))
                    # sock.send(data.decode('utf-8').upper().encode())  # 发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')
                else:
                    self.sock.close()  # 关闭连接
                    print('Connection from %s:%s closed.' % self.addr)
                    break
            print('transmit ok')

    def close(self):
        self.s.close()
    #
    # def event_judge(self,pridict=False):
    #     while(1):
    #         if self.sock.recv(1024).decode('utf-8')=='wav':
    #             self.sock.send('recvwav'.encode())
    #             time = str(datetime.datetime.now()).split('.')[0].replace(':','_')
    #             my_server.receive_wav('{name}.wav'.format(name=time))
    #             if pridict:
    #                 # server_predict.predict_wav(self.sess,'{name}.wav'.format(name=time))
    #                 end=server_predict.predict_wav(self.sess,"wav/normal__201105011626.wav")
    #                 self.sock.send(end.encode())
    #             print(time)






def TCP(sock, addr):  # TCP服务器端处理逻辑


    ready = True
    while ready:
        data = sock.recv(3000)  # 接受其数据
        if not len(data)==0:
            time.sleep(1)  # 延迟
            # if not data or data.decode() == 'quit':  # 如果数据为空或者'quit'，则退出
            #     break
            print("receiced:\t")
            print(data)
            # with open('test.wav','wb') as f :
                # f.write(data)
                # f.close()
            # print(data.decode('utf-8'))
            # sock.send(data.decode('utf-8').upper().encode())  # 发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')
        else:
            sock.close()  # 关闭连接
            print('Connection from %s:%s closed.' % addr)
            ready=False

def receive_wav(sock, addr):  # TCP服务器端处理逻辑

    # Length=32000
    Length=10
    length=0
    with open('test.wav', 'wb') as f:
        while (length<Length):
            data = sock.recv(5000)  # 接受其数据
            if  data:
                # if not data or data.decode() == 'quit':  # 如果数据为空或者'quit'，则退出
                #     break
                print("receiced:\t")
                print(len(data))
                f.write(data)
                length+=len(data)
                if length==Length:
                    f.close()
                    break
                # print(data.decode('utf-8'))
                # sock.send(data.decode('utf-8').upper().encode())  # 发送变成大写后的数据,需先解码,再按utf-8编码,  encode()其实就是encode('utf-8')
            else:
                sock.close()  # 关闭连接
                print('Connection from %s:%s closed.' % addr)
                break
        print('transmit ok')

if __name__=='__main__':

    while True:
        my_server=Server('localhost', 6666)
        my_server.event_judge()
        print('you can now disconnect connection ')
        my_server.close()