import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#此脚本用于Windows下文件夹中只存在图片时批量更名，若需在ubuntu下使用，只需将文件符\\换成/即可 共三处


def rename():
    relative_dir = input('intput relative_dir:\n')
    n = int(input('intput the first number:\n'))  # 起始编码数字，该数
    profix = relative_dir
    wd = getcwd()
    for root,dirs,files in os.walk('%s/%s'%(wd,relative_dir)):  #
        for file in files:
            newname=relative_dir+'/'+profix+'_'+str("%04d" %(n))+'.wav'  #文件命名格式  #2
            #用os模块中的rename方法对文件改名
            os.rename('%s/%s'%(relative_dir,file),newname)  #3
            n+=1


def rename_old():
    n=12 #起始编码数字，该数并不是被命名
    #relative_dir='pic2'  #图片存储相对路径相对路径
    relative_dir=input('intput relative_dir:\n')  #图片存储相对路径相对路径
    n=int(input('intput the first number:\n')) #起始编码数字，该数
    wd=getcwd()
    for root,dirs,files in os.walk('%s/%s'%(wd,relative_dir)):  #1
        for file in files:
            newname=relative_dir+'/Pic'+str("%04d" %(n))+'.JPG'  #文件命名格式  #2
            #用os模块中的rename方法对文件改名
            os.rename('%s/%s'%(relative_dir,file),newname)  #3
            n+=1

if __name__=='__main__':
    rename()