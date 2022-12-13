# 

## 

# Experiments on visualization quality using M4 sampling data

## 1. experimental process

Firstly, import test data into IoTDB:

```shell
./import-csv.sh -h 127.0.0.1 -p 6667 -u root -pw root -f ~/test.csv
```

Then use export-csv tool to export raw data and sampled data as the following examples show.

```shell
./export-csv.sh -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='208653','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.`1701`" -tf timestamp -td .
```

```shell
./export-csv.sh -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='417306','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.`1701`" -tf timestamp -td .
```

Finally, use customized python programs to plot pngs, and compare the differences between these pngs plotted from raw and sampled data.



## 2. about python plot 

As mentioned in the original M4 paper, the author uses [cairos](https://github.com/pygobject/pycairo) to plot the line chart. So the customized python plot programs (`cairos_plot.py` and `myplot.py`) try to reproduce the plot process.



## 3. experimental results

### (1) cairos_plot.py

-   for `test.csv`

![test](test.png)

-   for `test-M4.csv`:

![test-M4](test-M4.png)

the SSIM of raw and M4 is : 0.9949333406406351

the mse of raw and M4 is : 0.0007025

-   for `test-M4-doubleTimeInterval.csv`:

![test-M4-doubleTimeInterval](test-M4-doubleTimeInterval.png)

the SSIM of raw and M4-doubleTimeInterval is : 0.9737598563976496

the mse of raw and M4-doubleTimeInterval is : 0.00575375

### (2) run.sh

`run.sh` automatically iterates the sampling time intervals from `M4_TIME_INTERVAL-5` to `M4_TIME_INTERVAL+10`, to validate whether `M4_TIME_INTERVAL` is the optimal.

```bash
ruilei@fit07:~/CommonTools/python$ ./run.sh 
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:18.829 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select ZT11529 from root.group_69.* where time>=1591717867194 and time<1591926520194
22:27:18.843 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 1080267, request: 1080267
Export completely!
============-5==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:19.240 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208648','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:19.283 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28821, request: 28821
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086480_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086480_0.csv
output= /data3/ruilei/test-M4-2086480_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2358
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9934396196930736
the mse of raw and M4 is : 0.00095875
==============================
============-4==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:20.332 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208649','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:20.375 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28761, request: 28761
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086490_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086490_0.csv
output= /data3/ruilei/test-M4-2086490_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2353
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9936826560569231
the mse of raw and M4 is : 0.00090875
==============================
============-3==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:21.424 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208650','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:21.466 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28737, request: 28737
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086500_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086500_0.csv
output= /data3/ruilei/test-M4-2086500_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2351
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9938430566190456
the mse of raw and M4 is : 0.0009
==============================
============-2==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:22.516 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208651','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:22.558 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28509, request: 28509
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086510_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086510_0.csv
output= /data3/ruilei/test-M4-2086510_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2332
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9942279403673532
the mse of raw and M4 is : 0.00082125
==============================
============-1==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:23.602 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208652','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:23.645 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28449, request: 28449
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086520_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086520_0.csv
output= /data3/ruilei/test-M4-2086520_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2327
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9945249488609698
the mse of raw and M4 is : 0.0007425
==============================
============0==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:24.690 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208653','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:24.733 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28533, request: 28533
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086530_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086530_0.csv
output= /data3/ruilei/test-M4-2086530_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2334
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9949333406406351
the mse of raw and M4 is : 0.0007025
==============================
============1==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:25.782 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208654','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:25.824 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28545, request: 28545
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086540_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086540_0.csv
output= /data3/ruilei/test-M4-2086540_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2335
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9954137648091267
the mse of raw and M4 is : 0.000615
==============================
============2==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:26.865 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208655','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:26.908 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28269, request: 28269
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086550_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086550_0.csv
output= /data3/ruilei/test-M4-2086550_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2312
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9953368904281807
the mse of raw and M4 is : 0.00062125
==============================
============3==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:27.948 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208656','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:27.990 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28353, request: 28353
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086560_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086560_0.csv
output= /data3/ruilei/test-M4-2086560_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2319
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9952926010891635
the mse of raw and M4 is : 0.00064
==============================
============4==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:29.033 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208657','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:29.075 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28509, request: 28509
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086570_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086570_0.csv
output= /data3/ruilei/test-M4-2086570_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2332
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9950693650577634
the mse of raw and M4 is : 0.00066625
==============================
============5==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:30.112 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208658','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:30.154 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28449, request: 28449
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086580_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086580_0.csv
output= /data3/ruilei/test-M4-2086580_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2327
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9947287870208467
the mse of raw and M4 is : 0.00074375
==============================
============6==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:31.200 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208659','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:31.241 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28605, request: 28605
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086590_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086590_0.csv
output= /data3/ruilei/test-M4-2086590_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2340
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9944972244002501
the mse of raw and M4 is : 0.00079125
==============================
============7==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:32.280 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208660','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:32.322 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28665, request: 28665
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086600_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086600_0.csv
output= /data3/ruilei/test-M4-2086600_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2345
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9939720309804837
the mse of raw and M4 is : 0.00091625
==============================
============8==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:33.360 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208661','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:33.407 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28737, request: 28737
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086610_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086610_0.csv
output= /data3/ruilei/test-M4-2086610_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2351
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9936933450047762
the mse of raw and M4 is : 0.00095
==============================
============9==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:34.449 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208662','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:34.491 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28497, request: 28497
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086620_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086620_0.csv
output= /data3/ruilei/test-M4-2086620_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2331
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9933714716007891
the mse of raw and M4 is : 0.00103625
==============================
============10==============
------------------------------------------
Starting IoTDB Client Export Script
------------------------------------------
22:27:35.532 [main] DEBUG org.apache.iotdb.session.Session - TEndPoint(ip:127.0.0.1, port:6667) execute sql select M4(ZT11529,'timeInterval'='208663','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.*
22:27:35.575 [main] DEBUG org.apache.iotdb.rpc.AutoResizingBuffer - org.apache.iotdb.rpc.AutoResizingBuffer@5b87ed94 expand from 1024 to 28461, request: 28461
Export completely!
usage: python myplot.py WIDTH HEIGHT rawData samplingData
example: python myplot.py 1000 800 test.csv test-M4.csv

---------------args---------------
/data3/ruilei/CommonTools/python/myplot.py
width= 1000
height= 800
rawData= /data3/ruilei/test-raw0_0.csv
samplingData= /data3/ruilei/test-M4-2086630_0.csv
------------m4_plot------------
data= /data3/ruilei/test-raw0_0.csv
output= /data3/ruilei/test-raw0_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 273767
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
------------m4_plot------------
data= /data3/ruilei/test-M4-2086630_0.csv
output= /data3/ruilei/test-M4-2086630_0.csv.png
WIDTH= 1000
HEIGHT= 800
raw point number= 2328
v_min= 0.0
v_max= 90.1
t_min= 1591717867194
t_max_temp= 1591926520123
t_max= 1591926520194
---------------compare pngs---------------
the SSIM of raw and M4 is : 0.9932465245851196
the mse of raw and M4 is : 0.00105125
==============================
```





## 4. observations and todos

1.   The mse of raw and M4 is not zero, which should be zero according to the original M4 paper.

     One guess is that the line width may cause some extra pixels to be colored in the rendering mechanism of cairos, which is not discussed in the original M4 paper.

2.   In this experiment `run.sh`, when the sampling interval varies from `M4_TIME_INTERVAL-5` to `M4_TIME_INTERVAL+10`, the minumum mse happens when the sampling interval equals `M4_TIME_INTERVAL+1`, not `M4_TIME_INTERVAL`. In other words, `M4_TIME_INTERVAL` is not optimal?
3.   Changing the line width of cairos from `1` to `0.5` or `2` will increase mse.
4.   It is inconvenient to use customized python plot program for real users. Use Echart instead.
