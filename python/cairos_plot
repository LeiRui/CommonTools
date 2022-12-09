#!/usr/bin/python
import math
import cairo
from csv import reader
import re
from matplotlib import pyplot as plt
import numpy as np
import csv
import pandas as pd


def m4_mapping(r,r_min,r_max,canvas_length):
    # map position from r-space to canvas-space
    return (r-r_min)/(r_max-r_min)*canvas_length


t=[]
v=[]
with open('test.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    # This skips the first row of the CSV file.
    next(csv_reader)
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        t.append(int(row[0]))
        v.append(float(row[1]))

# print(t)
# print(v)
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

WIDTH = 10
HEIGHT = 10

v_min=min(v)
v_max=max(v)

t_min=min(t)
t_max_temp=max(t)
t_max=math.ceil((t_max_temp-t_min)/WIDTH)*WIDTH+t_min

print('v_min=',v_min)
print('v_max=',v_max)
print('t_min=',t_min)
print('t_max_temp=',t_max_temp)
print('t_max=',t_max)

# s = cairo.PSSurface("motivation-a.eps", WIDTH, HEIGHT)
# s.set_eps(True)

s = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
c = cairo.Context(s)
# c.set_antialias(cairo.ANTIALIAS_NONE)
c.set_source_rgb(1,1,1) # background color
c.paint()

# Transform to normal cartesian coordinate system
m = cairo.Matrix(yy=-1, y0=HEIGHT)
c.transform(m)

# line properties
c.set_source_rgb(0,0,0)
c.set_line_width(1)

x0=m4_mapping(t[0],t_min,t_max,WIDTH)
y0=m4_mapping(v[0],v_min,v_max,HEIGHT)
c.move_to(x0,y0) # the first point
for i in range(1,len(t)): # line to the second point until the last point
    x=m4_mapping(t[i],t_min,t_max,WIDTH)
    y=m4_mapping(v[i],v_min,v_max,HEIGHT)
    c.line_to(x,y)
c.stroke()

# # use max and min points in each pixel column to draw pixel columns
# num=math.floor(len(t)/2)
# print(num)
# for i in range(0,num):
#     vmin = v[i*2]
#     ymin=math.floor((vmin-v_min)/(v_max-v_min)*HEIGHT)
    
#     vmax = v[i*2+1]
#     ymax=math.ceil((vmax-v_min)/(v_max-v_min)*HEIGHT)

#     time = t[i*2]
#     pixelColumn = math.floor((time-t_min)/(t_max-t_min)*WIDTH)
#     if pixelColumn<WIDTH:
#         x = pixelColumn + 0.5
#     else: # =WIDTH
#         x = WIDTH - 0.5

#     # print(ymin)
#     # print(ymax)
#     # print(x)
#     # print()

#     c.move_to(x,ymin)
#     c.line_to(x,ymax)
# c.stroke()


s.write_to_png('motivation-a.png') #save as png
# s.show_page() #save as svg
s.finish()
