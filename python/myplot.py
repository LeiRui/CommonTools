#!/usr/bin/python
# usage: python myplot.py WIDTH HEIGHT rawData samplingData
# example: python myplot.py 1000 800 test.csv test-M4.csv
# output: pngs for rawData and samplingData, and the difference of the two pngs measured in SSIM and mse
import math
import cairo
from csv import reader
import re
from matplotlib import pyplot as plt
import numpy as np
import csv
import pandas as pd
import cv2
from skimage.metrics import structural_similarity as ssim
import sys

def m4_mapping(r,r_min,r_max,canvas_length):
    # map position from r-space to cairos canvas-space
    return (r-r_min)/(r_max-r_min)*canvas_length

def m4_plot(data,output,width,height):
    print('------------m4_plot------------')
    print('data=',data)
    print('output=',output)
    print('WIDTH=',width)
    print('HEIGHT=',height)
    t=[]
    v=[]
    with open(data, 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader) # This skips the first row of the CSV file.
        for row in csv_reader:
            t.append(int(row[0]))
            v.append(float(row[1]))

    print('raw point number=',len(v))

    # # sort and remove repetition
    # zipped_lists = zip(t, v)
    # sorted_zipped_lists = sorted(zipped_lists)
    # sorted_t = [element for element,_ in sorted_zipped_lists]
    # sorted_v = [element for _, element in sorted_zipped_lists]
    # print(sorted_t)
    # print(sorted_v)
    # t=sorted_t
    # v=sorted_v

    v_min=min(v)
    v_max=max(v)

    t_min=min(t)
    t_max_temp=max(t)
    # Although cairos can plot using t_max_temp with (t_max_temp-t_min)/WIDTH being non-integral, 
    # the M4 query implemented in IoTDB:
    # "select M4(s1,'timeInterval'='(tqe-tqs)/w','displayWindowBegin'='tqs','displayWindowEnd'='tqe') from root.vehicle.d1"
    # cannot use non-integral timeInterval. 
    # That's why making it consistent by ceiling t_max_temp to t_max.
    t_max=math.ceil((t_max_temp-t_min)/WIDTH)*WIDTH+t_min

    print('v_min=',v_min)
    print('v_max=',v_max)
    print('t_min=',t_min)
    print('t_max_temp=',t_max_temp)
    print('t_max=',t_max)

    # s = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    s = cairo.ImageSurface(cairo.FORMAT_A1, WIDTH, HEIGHT)
    c = cairo.Context(s)
    c.set_antialias(cairo.ANTIALIAS_NONE)  # turn off antialias function

    # Transform to normal cartesian coordinate system
    m = cairo.Matrix(yy=-1, y0=HEIGHT)
    c.transform(m)

    # line properties
    c.set_line_width(1)

    x0=m4_mapping(t[0],t_min,t_max,WIDTH)
    y0=m4_mapping(v[0],v_min,v_max,HEIGHT)
    c.move_to(x0,y0) # the first point
    for i in range(1,len(t)): # line to the second point until the last point
        x=m4_mapping(t[i],t_min,t_max,WIDTH)
        y=m4_mapping(v[i],v_min,v_max,HEIGHT)
        c.line_to(x,y)
    c.stroke()

    s.write_to_png(output) #save as png
    s.finish()

def mse(imfil1,imfil2):
    img1 = cv2.imread(imfil1)
    img2 = cv2.imread(imfil2)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    cv2.imshow('image', diff)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse

def match(imfil1,imfil2):    
    img1=cv2.imread(imfil1)    
    (h,w)=img1.shape[:2]    
    img2=cv2.imread(imfil2)    
    resized=cv2.resize(img2,(w,h))    
    (h1,w1)=resized.shape[:2]    
    img1=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)    
    img2=cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    return ssim(img1,img2)


print('usage: python myplot.py WIDTH HEIGHT rawData samplingData')
print('example: python myplot.py 1000 800 test.csv test-M4.csv')
print('output: pngs for rawData and samplingData, and the difference of the two pngs measured in SSIM and mse')
print('---------------args---------------')
print(sys.argv[0]) # prints python_script.py
print('width=',sys.argv[1]) # prints var1
print('height=',sys.argv[2]) # prints var2
print('rawData=',sys.argv[3]) # prints var3
print('samplingData=',sys.argv[4]) # prints var4

WIDTH = int(sys.argv[1])
HEIGHT = int(sys.argv[2])
rawData = sys.argv[3]
samplingData = sys.argv[4]

rawOutput=rawData+'.png'
m4_plot(rawData,rawOutput,WIDTH,HEIGHT)

samplingOutput=samplingData+'.png'
m4_plot(samplingData,samplingOutput,WIDTH,HEIGHT)

print('---------------compare pngs---------------')
print('the SSIM of raw and M4 is :', match(rawOutput,samplingOutput))
print('the mse of raw and M4 is :', mse(rawOutput,samplingOutput))
