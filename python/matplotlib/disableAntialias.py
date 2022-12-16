import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cv2
from skimage.metrics import structural_similarity as ssim
from csv import reader
import math

def match(imfil1,imfil2):    
    img1=cv2.imread(imfil1)    
    (h,w)=img1.shape[:2]    
    img2=cv2.imread(imfil2)    
    resized=cv2.resize(img2,(w,h))    
    (h1,w1)=resized.shape[:2]    
    img1=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)    
    img2=cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    return ssim(img1,img2)

def mse(imfil1,imfil2):
    img1 = cv2.imread(imfil1)
    img2 = cv2.imread(imfil2)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    # cv2.imshow('image', diff)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse


def full_frame(width, height, dpi):
    import matplotlib as mpl
    # First we remove any padding from the edges of the figure when saved by savefig. 
    # This is important for both savefig() and show(). Without this argument there is 0.1 inches of padding on the edges by default.
    mpl.rcParams['savefig.pad_inches'] = 0
    figsize = (width/dpi, height/dpi)
    fig = plt.figure(figsize=figsize,dpi=dpi)
    # Then we set up our axes (the plot region, or the area in which we plot things).
    # Usually there is a thin border drawn around the axes, but we turn it off with `frameon=False`.
    ax = plt.axes([0,0,1,1], frameon=False)
    # Then we disable our xaxis and yaxis completely. If we just say plt.axis('off'),
    # they are still used in the computation of the image padding.
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Even though our axes (plot region) are set to cover the whole image with [0,0,1,1],
	# by default they leave padding between the plotted data and the frame. We use tigher=True
	# to make sure the data gets scaled to the full extents of the axes.
    plt.autoscale(tight=True)


def myplot(csvData, width, height, dpi):
    full_frame(width,height,dpi)
    t=[]
    v=[]
    with open(csvData, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader) # This skips the first row of the CSV file.
        for row in csv_reader:
            t.append(int(row[0]))
            v.append(float(row[1]))
    v_min=min(v)
    v_max=max(v)
    t_min=min(t)
    t_max_temp=max(t)
    t_max=math.ceil((t_max_temp-t_min)/width)*width+t_min
    print('v_min=',v_min)
    print('v_max=',v_max)
    print('t_min=',t_min)
    print('t_max_temp=',t_max_temp)
    print('t_max=',t_max)
    plt.plot(t,v,'k',linewidth=0.01,antialiased=False)
    plt.xlim(t_min, t_max)
    plt.ylim(v_min, v_max)
    plt.savefig(csvData+'.png')

w=1000
h=800
dpi=50

# compare raw and M4-sampled data png
myplot('test.csv',w,h,dpi)
myplot('test-M4.csv',w,h,dpi)
print('the SSIM is ',match('test.csv.png','test-M4.csv.png'))
print('the mse is :', mse('test.csv.png','test-M4.csv.png'))

# check antialias condition
myplot('tmp.csv',3,3,dpi)

