import jieba, jieba.posseg
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

txt_filename = './story.txt'
result_filename = './短文-人物词频.csv'

# 打开有故事的文件并读取里面内容放到text里面
with open(txt_filename, 'r', encoding='utf-8') as f:
    text = f.read()

all_names = []
# text里面所有的字word都过一遍，如果有词符合 tag=nr，即其属性为人名，则将word添加到人名列表里面
for word, tag in jieba.posseg.cut(text):
    if tag == 'nr':
        all_names.append(word)

# 统计人名出现的次数，将人名作为字典的key，而对应它出现的次数作为value
occurrences = {}
for name in all_names: 
    if name == '梁祝':
        occurrences['梁山伯'] = occurrences.get('梁山伯', 0) + 1
        occurrences['祝英台'] = occurrences.get('祝英台', 0) + 1
        continue
    elif name == '祝' or name == '英台':
        name = '祝英台' 
    elif name == '梁' or name == '山伯':
        name = '梁山伯'

    if name in occurrences:
        occurrences[name] += 1
    else:  
        occurrences[name] = 1

occurrences = {name: count for name, count in occurrences.items() if count > 1} # 筛选出现超过一次的人名
print(occurrences)
data = list(occurrences.items())
data.sort(key=lambda x: x[1], reverse=True) # 换一下顺序从，最多到最少出现的次数
print(data)

bar_chart = Bar()
bar_chart.add_xaxis([item[0] for item in data])
bar_chart.add_yaxis("人物词频", [item[1] for item in data])
bar_chart.set_global_opts(title_opts=opts.TitleOpts(title="人物词频统计"))
bar_chart.render("人物词频统计.html")

