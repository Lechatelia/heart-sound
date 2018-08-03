#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from socket import *

HOST = '192.168.1.102'
PORT = 6789
BUFFSIZE = 2048
ADDR = (HOST, PORT)
wav_name=["wav/normal__201105011626.wav"]

if __name__=='__main__':

    tctimeClient = socket(AF_INET, SOCK_STREAM)
    tctimeClient.connect(ADDR)
    print('connect to %s:%s sucessfully!' % ADDR)
    while True:
        print("输入发送数据")
        try:
            data = input(">")
        except KeyboardInterrupt:
            print('over')
            tctimeClient.close()
            break
        else:
            if not data:
                break
            # if data=='send':
            else:
                tctimeClient.send(data.encode())

                print('receive:\t{num}'.format(num=tctimeClient.recv(BUFFSIZE).decode()))
                # tctimeClient.send(data.encode())
                # predict = tctimeClient.recv(BUFFSIZE).decode()
                # if not data:
                #     break
                # print(predict)
    tctimeClient.close()