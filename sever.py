import socket
import time
import threading
import datetime
import mysql
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

    def test_loop(self):
        while (1):
            try:
                data = self.sock.recv(1024)
            except OSError:
                print('Connection Error from socket %s:%s .' % self.addr)
                self.sock.close()
                break
            else:
                if not data:
                    print('Connection from %s:%s closed.' % self.addr)
                    self.sock.close()
                    break
                else :
                    print(data.decode('utf-8'))
                    self.sock.send(data)


    def close(self):
        self.s.close()

    def strlist_2_one_str(self,list):
        str=''
        if len(list)==0:
            return 'blank'
        for i in list:
            str=str+i
        return str
    #
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

                else:
                    data_list=data.decode('utf-8').split('\r\n')
                    print(data_list)
                    if data_list[0] == 'update':

                        if len(data_list)==6:
                            mysql.Add_info_to_SQL_no_id(data_list[2],data_list[3],int(data_list[4]),tel=int(data_list[5]))
                            # mysql.Add_info_to_SQL_no_id('zhujin','1997-03-27',1,tel=13772052853)
                            self.sock.send('over'.encode())
                        else:
                            print(data_list)
                            print('update information error from APP')
                    elif data_list[0]=='use_list_get':
                        info_list=mysql.get_all_info()
                        # for i in range(len(info_list)):
                        #     self.sock.send(info_list[i].encode())
                        self.sock.send(self.strlist_2_one_str(info_list).encode())
                    elif data_list[0]=='use_diagnosis_get':
                        results=mysql.get_diagnosis_by_id(int(data_list[1]))
                        if len(results)==0:
                            results.append('blank')
                        print(len(results[0]))
                        # for i in results:
                        #     self.sock.send(i.encode())
                        self.sock.send(self.strlist_2_one_str(results).encode())
                        # print(self.strlist_2_one_str(results))

                    else:
                        print('unknown messsge:\t{mess}'.format(mess=data.decode('utf-8')))


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


if __name__ == '__main__':
    while True:
        # my_server=Server('localhost', 7777)
        my_server=Server('192.168.1.102', 7777)
        # my_server.test_loop()
        my_server.event_judge()
        print('you can now disconnect connection ')
        my_server.close()
        time.sleep(0.1)