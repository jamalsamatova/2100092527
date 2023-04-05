# 通过访问统计近期发生地震的地区的网站进行爬虫及其可视化
# 由于这里涉及到网页爬虫，可能需要一点时间等结果出来
import requests
from bs4 import BeautifulSoup as BS

response = requests.get('http://ds.iris.edu/seismon/eventlist/index.phtml') # 访问网站
html = response.text 
soup = BS(html, features='html.parser')
latlon = soup.find_all('td', class_ = 'latlon') # 在html里搜索
magnitudes = soup.find_all('td', class_='mag') # 搜索
regions = soup.find_all('td', class_='region') #搜索所有地区
all_cases = {} 
# 下面将所有地区及其对应参数放到一个字典里
for i in range(0,len(regions)):
    latitude = latlon[i*2].text
    longitude = latlon[i*2+1].text
    magnitude = magnitudes[i].text
    region = regions[i].text.replace('\n','')
    all_cases[region] = [latitude, longitude, float(magnitude)]
print(all_cases)

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType

geo = Geo()
for case, info in all_cases.items():
    geo.add_coordinate(name=case, latitude=info[0], longitude=info[1]) # 将每个地区及其坐标点添加到坐标库

geo.add_schema(maptype="world")

for case, info in all_cases.items():
    # 跟据震级设定点的大小
    if info[2] <= 3:
        s = 5
    elif info[2] <= 4.5:
        s = 10
    elif info[2] <= 6.5:
        s = 15
    else:
        s = 20
    geo.add("",[(case, info[2])], type_=ChartType.SCATTER, symbol_size=s) 

geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(min_= 1, max_ = 9), # 震级都是以1到9衡量的
                    title_opts=opts.TitleOpts(title="近期地震地区"))

geo.render('./world_earthquakes.html')