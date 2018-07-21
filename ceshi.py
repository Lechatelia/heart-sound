import  numpy as np
import tensorflow as tf
import os
import xlwt
dir='dataset/'
import csv
import audio_processing

out_file = open('./chongfu.txt', 'a+')
out_file.write("jsoasladasass\n")

#Python3.4以后的新方式，解决空行问题




# i=0
# with open('write.csv', 'w', newline='') as csv_file:
#     csv_writer = csv.writer(csv_file)
#     for file in os.listdir(dir):
#         # if os.path.isfile(file):
#         if file.split('.')[-1]=='wav':
#             print(file.split('_')[0])
#             i=i+1
#             csv_writer.writerow([file,'',file.split('_')[0]])  # 其中的'0-行, 0-列'指定表中的单元，'EnglishName'是向该单元写入的内容





'''
array_full=['aaa','bbb','ccc']
array_full=np.array(array_full)
print(array_full[1])
print(type(array_full))
print(array_full.shape)

a=[2]
#print(type(a))
#print(float(a[0]))


t1 = [[1, 2, 3], [4, 5, 6]]
t2 = [[7, 8, 9], [10, 11, 12]]
print(tf.concat( [t1, t2],0) )# [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
print(tf.concat( [t1, t2],1))# [[1, 2, 3, 7, 8, 9], [4, 5, 6, 10, 11, 12]]

arr=np.arange(0,20)
arr=np.reshape(arr,(4,5))
print(str(arr.shape))
print(arr)
print(arr[:,3:4])

num=20
a=range(0,num)
b=range(num,2*num)
a=np.array(a)
b=np.array(b)
perm0 = np.arange(num)
np.random.shuffle(perm0)
a = a[perm0]
b= b[perm0]
print(perm0)
print(a)
print(b)
print(np.concatenate((a,b),0))
'''