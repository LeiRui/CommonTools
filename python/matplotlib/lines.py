import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2
from skimage.metrics import structural_similarity as ssim

def match(imfil1,imfil2):    
    img1=cv2.imread(imfil1)    
    (h,w)=img1.shape[:2]    
    img2=cv2.imread(imfil2)    
    resized=cv2.resize(img2,(w,h))    
    (h1,w1)=resized.shape[:2]    
    img1=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)    
    img2=cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    return ssim(img1,img2)



w=800
h=200
dpi=50

# w=40
# h=30
# dpi=100


# data_file='/Users/chaosun/apache-iotdb-0.14.0-SNAPSHOT-all-bin/origin.csv'
# timestamp=pd.to_datetime(pd.read_csv(data_file).iloc[:,0])
# value=pd.read_csv(data_file).iloc[:,1].to_numpy()
# plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi)
# plt.gca().xaxis.set_major_locator(plt.NullLocator())
# plt.gca().yaxis.set_major_locator(plt.NullLocator())
# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
# plt.margins(0,0)
# plt.plot(timestamp,value,'k')
# plt.savefig('/Users/chaosun/origin.jpg', pad_inches=0)



# data_file='/Users/chaosun/apache-iotdb-0.14.0-SNAPSHOT-all-bin/sample_f=1d_k=19.csv'
# timestamp=pd.to_datetime(pd.read_csv(data_file).iloc[:,0])
# value=pd.read_csv(data_file).iloc[:,1].to_numpy()
# plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi)
# plt.gca().xaxis.set_major_locator(plt.NullLocator())
# plt.gca().yaxis.set_major_locator(plt.NullLocator())
# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
# plt.margins(0,0)
# plt.plot(timestamp,value,'k')
# plt.savefig('/Users/chaosun/test1.jpg', pad_inches=0)



# data_file='/Users/chaosun/apache-iotdb-0.14.0-SNAPSHOT-all-bin/m4_f=1d_k=19.csv'
# timestamp=pd.to_datetime(pd.read_csv(data_file).iloc[:,0])
# value=pd.read_csv(data_file).iloc[:,1].to_numpy()
# plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi)
# plt.gca().xaxis.set_major_locator(plt.NullLocator())
# plt.gca().yaxis.set_major_locator(plt.NullLocator())
# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
# plt.margins(0,0)
# plt.plot(timestamp,value,'k')
# plt.savefig('/Users/chaosun/test2.jpg', pad_inches=0)


# print('the SSIM of largestTriangleBucket is :', match('/Users/chaosun/origin.jpg','/Users/chaosun/test1.jpg'))
# print('the SSIM of M4Bucket is :', match('/Users/chaosun/origin.jpg','/Users/chaosun/test2.jpg'))




data_file='test.csv'
timestamp=pd.to_datetime(pd.read_csv(data_file).iloc[:,0])
value=pd.read_csv(data_file).iloc[:,1].to_numpy()
plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi)
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
plt.margins(0,0)
plt.plot(timestamp,value,linewidth=1,color='k')
# plt.plot(timestamp,value,color='k')
plt.savefig('scout.jpg', pad_inches=0)