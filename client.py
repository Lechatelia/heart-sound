#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from socket import *

HOST = 'localhost'
PORT = 6666
BUFFSIZE = 2048
ADDR = (HOST, PORT)
wav_name=["wav/normal__201105011626.wav"]

if __name__=='__main__':

    tctimeClient = socket(AF_INET, SOCK_STREAM)
    tctimeClient.connect(ADDR)
    print('connect to %s:%s sucessfully!' % ADDR)
    while True:
        print("输入send发送位置")
        data = input(">")
        if not data:
            break
        if data=='send':
            #tctimeClient.send(data[0].encode())
            tctimeClient.send(wav_name[0].encode())
            predict = tctimeClient.recv(BUFFSIZE).decode()
            if not data:
                break
            print(predict)
    tctimeClient.close()