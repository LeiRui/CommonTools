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
    print('--------------------------------')
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


WIDTH = 1000
HEIGHT = 800

data_raw='test.csv'
output_raw='test.png'
m4_plot(data_raw,output_raw,WIDTH,HEIGHT)

data_M4='test-M4.csv'
output_M4='test-M4.png'
m4_plot(data_M4,output_M4,WIDTH,HEIGHT)
print('the SSIM of raw and M4 is :', match(output_raw,output_M4))
print('the mse of raw and M4 is :', mse(output_raw,output_M4))

data_M4_minus_one='test-M4-208652.csv'
output_M4_minus_one='test-M4-208652.png'
m4_plot(data_M4_minus_one,output_M4_minus_one,WIDTH,HEIGHT)
print('the SSIM of raw and M4-minus-one is :', match(output_raw,output_M4_minus_one))
print('the mse of raw and M4-minus-one is :', mse(output_raw,output_M4_minus_one))

data_M4_plus_one='test-M4-208654.csv'
output_M4_plus_one='test-M4-208654.png'
m4_plot(data_M4_plus_one,output_M4_plus_one,WIDTH,HEIGHT)
print('the SSIM of raw and M4-plus-one is :', match(output_raw,output_M4_plus_one))
print('the mse of raw and M4-plus-one is :', mse(output_raw,output_M4_plus_one))

data_M4_plus_two='test-M4-208655.csv'
output_M4_plus_two='test-M4-208655.png'
m4_plot(data_M4_plus_two,output_M4_plus_two,WIDTH,HEIGHT)
print('the SSIM of raw and M4-plus-two is :', match(output_raw,output_M4_plus_two))
print('the mse of raw and M4-plus-two is :', mse(output_raw,output_M4_plus_two))

data_M4_plus_three='test-M4-208656.csv'
output_M4_plus_three='test-M4-208656.png'
m4_plot(data_M4_plus_three,output_M4_plus_three,WIDTH,HEIGHT)
print('the SSIM of raw and M4-plus-three is :', match(output_raw,output_M4_plus_three))
print('the mse of raw and M4-plus-three is :', mse(output_raw,output_M4_plus_three))

data_M4_plus_four='test-M4-208657.csv'
output_M4_plus_four='test-M4-208657.png'
m4_plot(data_M4_plus_four,output_M4_plus_four,WIDTH,HEIGHT)
print('the SSIM of raw and M4-plus-four is :', match(output_raw,output_M4_plus_four))
print('the mse of raw and M4-plus-four is :', mse(output_raw,output_M4_plus_four))

data_M4_plus_five='test-M4-208658.csv'
output_M4_plus_five='test-M4-208658.png'
m4_plot(data_M4_plus_five,output_M4_plus_five,WIDTH,HEIGHT)
print('the SSIM of raw and M4-plus-five is :', match(output_raw,output_M4_plus_five))
print('the mse of raw and M4-plus-five is :', mse(output_raw,output_M4_plus_five))

data_M4_doubleTimeInterval='test-M4-doubleTimeInterval.csv'
output_M4_doubleTimeInterval='test-M4-doubleTimeInterval.png'
m4_plot(data_M4_doubleTimeInterval,output_M4_doubleTimeInterval,WIDTH,HEIGHT)
print('the SSIM of raw and M4-doubleTimeInterval is :', match(output_raw,output_M4_doubleTimeInterval))
print('the mse of raw and M4-doubleTimeInterval is :', mse(output_raw,output_M4_doubleTimeInterval))
