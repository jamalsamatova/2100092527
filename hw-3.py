from pyecharts.charts import Bar, Line
from pyecharts import options as opts
import csv

years = []
gdp = []

# 打开具有中国近四十年的GDP，由于我是从国外网站找到的可能不太符合实际数据
with open('china_gdp.csv') as f:
    reader = csv.reader(f) # 读取数据
    for row in reader: 
        years.append(row[0]) # 将每年添加到年份的列表
        gdp.append(float(row[1])) # 将每年的gdp添加到列表

bar = Bar()
bar.add_xaxis(years) # 年份设定为横轴
bar.add_yaxis('GDP', gdp) # 国内生产总值设定为纵轴

line = Line() # 加一个线
line.add_xaxis(years)
line.add_yaxis('GDP', gdp, label_opts=opts.LabelOpts(is_show=False), symbol_size=8, linestyle_opts=opts.LineStyleOpts(width=2))

combo_chart = bar.overlap(line)

combo_chart.set_global_opts(
    title_opts=opts.TitleOpts(title="1978至2021年中国国内生产总值"),
    xaxis_opts=opts.AxisOpts(name='Year'),
    yaxis_opts=opts.AxisOpts(name='GDP()'),
    datazoom_opts=[opts.DataZoomOpts(range_start=0, range_end=40)] # 可调的时间段
)

combo_chart.render('china_gdp.html')