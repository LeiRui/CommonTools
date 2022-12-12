# 

# Readme

## 1. prepare data

Using the following IoTDB export-csv command to export csv data, which are already in this repository.

-   raw data `test.csv`:

```bash
.\export-csv.bat -h 127.0.0.1 -p 6667 -u root -pw root -q "select ZT11529 from root.group_69.`1701`" -tf timestamp -td . -linesPerFile 300000
```

-   M4 data `test-M4.csv`:

```bash
.\export-csv.bat -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='208653','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.`1701`" -tf timestamp -td .
```

-   M4 data but using double sampling time interval (which is not the ideal usage of M4) `test-M4-doubleTimeInterval.csv`:

```bash
.\export-csv.bat -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='417306','displayWindowBegin'='1591717867194','displayWindowEnd'='1591926520194') from root.group_69.`1701`" -tf timestamp -td .
```

## 2. using python.cairos to plot

As mentioned in the original M4 paper, the author uses ==cairos== to plot the line chart.

```python
python cairos_plot.py
```

The program will render pngs for the `test.csv`, `test-M4.csv`, `test-M4-doubleTimeInterval.csv`, and compare the differences between the raw data png and M4 sampling data pngs.





