import  numpy as np
import tensorflow as tf
import os
import xlwt
dir='dataset/'
import csv
import audio_processing
from skimage import io
import matplotlib.pyplot as plt
out_file = open('./chongfu.txt', 'a+')
out_file.write("jsoasladasass\n")

#Python3.4以后的新方式，解决空行问题

img=io.imread('123.jpg')
plt.subplot(2,2,1)
plt.subplot(2, 2, 1)  # 将窗口分为两行两列四个子图，则可显示四幅图片
plt.title('origin image')  # 第一幅图片标题
plt.imshow(img)  # 绘制第一幅图片

print(img.shape)
print(img[:, :, 0].shape)



plt.subplot(2, 2, 2)  # 第二个子图
plt.title('R channel')  # 第二幅图片标题
plt.imshow(img[:, :, 0], plt.cm.gray)  # 绘制第二幅图片,且为灰度图
plt.axis('off')  # 不显示坐标尺寸

plt.subplot(2, 2, 3)  # 第三个子图
plt.title('G channel')  # 第三幅图片标题
plt.imshow(img[:, :, 1], plt.cm.gray)  # 绘制第三幅图片,且为灰度图
plt.axis('off')  # 不显示坐标尺寸

plt.subplot(2, 2, 4)  # 第四个子图
plt.title('B channel')  # 第四幅图片标题
plt.imshow(img[:, :, 2], plt.cm.gray)  # 绘制第四幅图片,且为灰度图
plt.axis('off')  # 不显示坐标尺寸


plt.savefig('hah.png')
plt.show()

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