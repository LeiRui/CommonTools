# Readme

## 1. prepare data

Import test data into IoTDB:

```shell
./import-csv.sh -h 127.0.0.1 -p 6667 -u root -pw root -f ~/test.csv
```

Then using the following IoTDB export-csv command to export csv data, which are already in this repository:

```shell
exportCsvPath=/data3/ruilei/iotdb/cli/target/iotdb-cli-1.0.1-SNAPSHOT/tools/export-csv.sh
myplotPath=myplot.py

# user parameters for line chart visualization
user_line_chart_tqs=1591717867194
user_line_chart_tqe=1591926520123
user_line_chart_canvasPixelWidth=1000

# prepare to rewrite the user-provided raw data range query as M4 query
M4_adapt_time_interval=$(( (${user_line_chart_tqe}-${user_line_chart_tqs}+${user_line_chart_canvasPixelWidth} -1)/${user_line_chart_canvasPixelWidth} )) # ceil((user_line_chart_tqe-user_line_chart_tqs)/user_line_chart_canvasPixelWidth)
M4_adapt_tqe=$(( ${user_line_chart_tqs}+${M4_adapt_time_interval}*${user_line_chart_canvasPixelWidth} ))

# raw data query
bash ${exportCsvPath} -h 127.0.0.1 -p 6667 -u root -pw root -q "select ZT11529 from root.group_69.* where time>=${user_line_chart_tqs} and time<${M4_adapt_tqe}" -tf timestamp -td . -linesPerFile 300000 -f ~/test-raw

# M4 query
M4_time_interval=${M4_adapt_time_interval}
bash ${exportCsvPath} -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='${M4_time_interval}','displayWindowBegin'='${user_line_chart_tqs}','displayWindowEnd'='${M4_adapt_tqe}') from root.group_69.`1701`" -tf timestamp -td . -f ~/test-M4-${M4_time_interval}

# plot and compare
python ${myplotPath} 1000 800 ~/test-raw*.csv ~/test-M4-${M4_time_interval}*.csv
```



## 2. using python.cairos to plot

As mentioned in the original M4 paper, the author uses [cairos](https://github.com/pygobject/pycairo) to plot the line chart. So `cairos_plot.py` tries to reproduce the plot process.

```python
python cairos_plot.py
```

The program will render pngs for the `test.csv`, `test-M4.csv`, `test-M4-doubleTimeInterval.csv`, and compare the differences between the raw data png and M4 sampling data pngs.

## 3. current results

pngs are as follows:

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



## 4. TODOS

The mse of raw and M4 is not zero, which should be zero according to the original M4 paper.

One possible reason is that the line width may play some role in the rendering mechanism of cairos, which is not discussed in the original M4 paper.
