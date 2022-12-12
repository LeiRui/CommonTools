#!/usr/bin/python
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

def m4_mapping(r,r_min,r_max,canvas_length):
    # map position from r-space to cairos canvas-space
    return (r-r_min)/(r_max-r_min)*canvas_length

def m4_plot(data,output,width,height):
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

    # # sort and remove repetite
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
    # round t_max to comply with M4 paper usage. 
    # NOTE that the input M4 sampling data should also comply with the time intervals. That is, 
    # select M4(s1,'timeInterval'='(tqe-tqs)/w','displayWindowBegin'='tqs','displayWindowEnd'='tqe') from root.vehicle.d1
    # where tqe should also be treated like this.
    # Although cairos can plot using t_max_temp with (t_max_temp-t_min)/WIDTH being non-integral, 
    # the M4 sampling implemented in IoTDB cannot use non-integral timeInterval. That's why making it consistent. 
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


# Using the following IoTDB export-csv command to export csv data:
# .\export-csv.bat -h 127.0.0.1 -p 6667 -u root -pw root -q "select ZT11529 from root.group_69.`1701`" -tf timestamp -td . -linesPerFile 300000
# .\export-csv.bat -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='208653','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.`1701`" -tf timestamp -td .
# .\export-csv.bat -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='417306','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.`1701`" -tf timestamp -td .

WIDTH = 1000
HEIGHT = 800

data_raw='test.csv'
output_raw='test.png'
m4_plot(data_raw,output_raw,WIDTH,HEIGHT)

data_M4='test-M4.csv'
output_M4='test-M4.png'
m4_plot(data_M4,output_M4,WIDTH,HEIGHT)

data_M4_doubleTimeInterval='test-M4-doubleTimeInterval.csv'
output_M4_doubleTimeInterval='test-M4-doubleTimeInterval.png'
m4_plot(data_M4_doubleTimeInterval,output_M4_doubleTimeInterval,WIDTH,HEIGHT)

print('the SSIM of raw and M4 is :', match(output_raw,output_M4))
print('the mse of raw and M4 is :', mse(output_raw,output_M4))

print('the SSIM of raw and M4-doubleTimeInterval is :', match(output_raw,output_M4_doubleTimeInterval))
print('the mse of raw and M4-doubleTimeInterval is :', mse(output_raw,output_M4_doubleTimeInterval))

