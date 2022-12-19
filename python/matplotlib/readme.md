# matplotlib
![image](https://user-images.githubusercontent.com/33376433/208372659-7ad8d45c-de98-4b92-96d7-df02fb793234.png)

plt.plot(t,v,'k',linewidth=1,antialiased=True):

![image](https://user-images.githubusercontent.com/33376433/208371192-8f391968-824e-403a-9a8a-c01c64043cbd.png)


plt.plot(t,v,'k',linewidth=1,antialiased=False)

![image](https://user-images.githubusercontent.com/33376433/208371272-960c8082-56c7-4784-ab15-e2ce71f3a081.png)

## how to disable antialias matplotlib

昨天知道了cairos无法真的关掉antialias，最多是从灰度图用一个阈值二分化得到二值图像，antialias仍然对结果像素有影响作用。

--

https://matplotlib.org/2.0.2/examples/pylab_examples/image_interp.html


### interpolation overview

https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html

>   If *interpolation* is None, it defaults to the `rcParams["image.interpolation"]` (default: `'antialiased'`). If the interpolation is `'none'`, then no interpolation is performed for the Agg, ps and pdf backends. Other backends will default to `'antialiased'`.
>
>   For the Agg, ps and pdf backends, `interpolation='none'` works well when a big image is scaled down, while `interpolation='nearest'` works well when a small image is scaled up.

![image-20221216174325967](readme.assets/image-20221216174325967.png)



### plt.imshow

https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html

Display data as **an image, i.e., on a 2D regular raster.**

>   **interpolation**: str, default: `rcParams["image.interpolation"]` (default: `'antialiased'`)
>
>   The interpolation method used.
>
>   Supported values are 'none', 'antialiased', 'nearest', 'bilinear', 'bicubic', 'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos', 'blackman'.
>
>   **If *interpolation* is 'none', then no interpolation is performed on the Agg, ps, pdf and svg backends. Other backends will fall back to 'nearest'. Note that most SVG renderers perform interpolation at rendering and that the default interpolation method they implement may differ.**
>
>   If *interpolation* is the default 'antialiased', then 'nearest' interpolation is used if the image is upsampled by more than a factor of three (i.e. the number of display pixels is at least three times the size of the data array). If the upsampling rate is smaller than 3, or the image is downsampled, then 'hanning' interpolation is used to act as an anti-aliasing filter, unless the image happens to be upsampled by exactly a factor of two or one.
>
>   See [Interpolations for imshow](https://matplotlib.org/stable/gallery/images_contours_and_fields/interpolation_methods.html) for an overview of the supported interpolation methods, and [Image antialiasing](https://matplotlib.org/stable/gallery/images_contours_and_fields/image_antialiasing.html) for a discussion of image antialiasing.
>
>   Some interpolation methods require an additional radius parameter, which can be set by *filterrad*. Additionally, the antigrain image resize filter is controlled by the parameter *filternorm*.
>
>   ---
>
>   **interpolation_stage**{'data', 'rgba'}, default: 'data'
>
>   If 'data', interpolation is carried out on the data provided by the user. If 'rgba', the interpolation is carried out after the colormapping has been applied (visual interpolation).

### Rasterization for vector graphics

https://matplotlib.org/stable/gallery/misc/rasterization_demo.html

-   Setting rasterization only affects vector backends such as PDF, SVG, or PS.

-   **The storage size and the resolution of the rasterized artist is determined by its physical size and the value of the `dpi` parameter passed to [`savefig`](https://matplotlib.org/stable/api/figure_api.html#matplotlib.figure.Figure.savefig).**





### dpi, pixel 

https://stackoverflow.com/questions/47633546/relationship-between-dpi-and-figure-size

A figure of `figsize=(w,h)` will have `px, py = w*dpi, h*dpi  # pixels`

<img src="readme.assets/image-20221216182318902.png" alt="image-20221216182318902" style="zoom:80%;" />

还是不太懂



### 精确控制savefig像素大小 / matplotlib savefig without axis or padding

#### trial 1: NO

```python
w=800
h=200
dpi=50

data_file='test.csv'
timestamp=pd.to_datetime(pd.read_csv(data_file).iloc[:,0])
value=pd.read_csv(data_file).iloc[:,1].to_numpy()

fig=plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi, frameon=False)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
plt.plot(timestamp,value,'k')
plt.savefig(data_file+'.png', bbox_inches='tight',pad_inches=0)
```

不行，虽然fig像素是对了，是800*200像素，但是坐标轴的位置还是留着空着，原因：

>   If we just say plt.axis('off'),
>   # they are still used in the computation of the image padding.



#### trial-2: YES!!!!

https://gist.github.com/kylemcdonald/bedcc053db0e7843ef95c531957cb90f

```python
def full_frame(width=None, height=None, dpi=None):
    import matplotlib as mpl
    # First we remove any padding from the edges of the figure when saved by savefig. 
    # This is important for both savefig() and show(). Without this argument there is 0.1 inches of padding on the edges by default.
    mpl.rcParams['savefig.pad_inches'] = 0
    figsize = None if width is None else (width/dpi, height/dpi)
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
    
full_frame()
plt.plot(X)
plt.savefig('fig.png')
plt.show()
```



## 观察

```
time,value
0,0
1,3
3,3
```

v_min= 0.0
v_max= 3.0
t_min= 0
t_max_temp= 3
t_max= 3

https://pixspy.com/

![image-20221216192948148](readme.assets/image-20221216192948148.png)

也就是说，x轴映射的t范围是[0,3]，y轴映射的v范围是[0,3]，连线的三个(t-v)点是(0,0),(1,3),(3,3)

>   (t-tmin)/(tmax-tmin)*WIDTH

Q1: 从t-v到x-y的映射是如何的？如果按照等比例映射，则三个(x-y)点是(0,0),(1,3),(3,3)

Q2: 从x-y到i-j的映射是如何的？

![image-20221216193433567](readme.assets/image-20221216193433567.png)

是这样吗？然后线宽超过1的那种

-   设置line.set_antialiased(False) # turn off antialiasing 或者 plt.plot(t,v,'k',linewidth=1,antialiased=False)之后：

![image-20221216193818773](readme.assets/image-20221216193818773.png)

这是？这是把灰度图按照阈值0二分化？

https://github.com/matplotlib/matplotlib/issues/6134/

-   把数据点修改成如下之后：

```
time,value
0,0
1,1.5
3,3
```



![image-20221216194952362](readme.assets/image-20221216194952362.png)

![image-20221216195400427](readme.assets/image-20221216195400427.png)

是这样吗？看起来好像是根据像素各自内经过的面积决定像素灰度深浅。但是第一列第二行的各自深度是比第二列第三行的格子浅的，但是从我画的线条看起来似乎前者经过的长度更长啊，难道是data interpolation？不是看线条经过像素格子的长度？