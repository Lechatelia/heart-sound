#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from socket import *

HOST = '192.168.1.102'
# HOST = 'localhost'
PORT = 6666
BUFFSIZE = 2048
ADDR = (HOST, PORT)
wav_name=["wav/normal__201105011626.wav"]
message1='update\r\n45454\r\nzhujinguo\r\n1997-03-27\r\n1\r\n13772052853'
message2='use_list_get'
message3='use_diagnosis_get\r\n1564221354'
message3='use_diagnosis_get\r\n123'

if __name__=='__main__':

    tctimeClient = socket(AF_INET, SOCK_STREAM)
    tctimeClient.connect(ADDR)
    print('connect to %s:%s sucessfully!' % ADDR)
    while True:
        print("输入发送数据")
        try:
            data = input(">")
        except KeyboardInterrupt:
            print('sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )over')
            tctimeClient.close()
            break
        else:
            if not data:
                break
            # if data=='send':
            elif data=='mess1':
                tctimeClient.send(message1.encode())
                print('receive:\t{num}'.format(num=tctimeClient.recv(BUFFSIZE).decode()))
            elif data=='mess2':
                tctimeClient.send(message2.encode())
                print('receive:\t{num}'.format(num=tctimeClient.recv(BUFFSIZE).decode()))
            elif data=='mess3':
                tctimeClient.send(message3.encode())
                print('receive:\t{num}'.format(num=tctimeClient.recv(BUFFSIZE).decode()))

            else:
                tctimeClient.send(data.encode())

                print('receive:\t{num}'.format(num=tctimeClient.recv(BUFFSIZE).decode()))
                # tctimeClient.send(data.encode())
                # predict = tctimeClient.recv(BUFFSIZE).decode()
                # if not data:
                #     break
                # print(predict)
    tctimeClient.close()