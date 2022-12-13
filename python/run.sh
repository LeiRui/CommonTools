exportCsvPath=/data3/ruilei/iotdb/cli/target/iotdb-cli-1.0.1-SNAPSHOT/tools/export-csv.sh
myplotPath=/data3/ruilei/CommonTools/python/myplot.py

# user parameters for line chart visualization
user_line_chart_tqs=1591717867194
user_line_chart_tqe=1591926520123
user_line_chart_canvasPixelWidth=1000

# prepare to rewrite the user-provided raw data range query as M4 query
M4_adapt_time_interval=$(( (${user_line_chart_tqe}-${user_line_chart_tqs}+${user_line_chart_canvasPixelWidth} -1)/${user_line_chart_canvasPixelWidth} )) # ceil((user_line_chart_tqe-user_line_chart_tqs)/user_line_chart_canvasPixelWidth)
M4_adapt_tqe=$(( ${user_line_chart_tqs}+${M4_adapt_time_interval}*${user_line_chart_canvasPixelWidth} ))

# raw data query
bash ${exportCsvPath} -h 127.0.0.1 -p 6667 -u root -pw root -q "select ZT11529 from root.group_69.* where time>=${user_line_chart_tqs} and time<${M4_adapt_tqe}" -tf timestamp -td . -linesPerFile 300000 -f ~/test-raw

# M4 sampling query with different sampling time intervals,
# aiming to validate whether M4_adapt_time_interval is the optimal
for M4_time_interval in ${M4_adapt_time_interval}
do
    bash ${exportCsvPath} -h 127.0.0.1 -p 6667 -u root -pw root -q "select M4(ZT11529,'timeInterval'='${M4_time_interval}','displayWindowBegin'='${user_line_chart_tqs}','displayWindowEnd'='${M4_adapt_tqe}') from root.group_69.`1701`" -tf timestamp -td . -f ~/test-M4-${M4_time_interval}
    # plot and compare
    python3 ${myplotPath} 1000 800 ~/test-raw*.csv ~/test-M4-${M4_time_interval}*.csv
done