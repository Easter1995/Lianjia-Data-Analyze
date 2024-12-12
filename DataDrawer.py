import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# 设置字体为黑体(SimHei)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取处理后的新房和二手房数据
new_house_df = pd.read_csv('processed_data/processed_new_house.csv')
second_hand_df = pd.read_csv('processed_data/processed_second_hand_house.csv')

# 可视化1：绘制楼盘价格分布的散点图
# 纵横轴分别代表单价和总价，楼盘类型通过散点的颜色区分

plt.figure(figsize=(10, 6))

# 获取类型列表
types = new_house_df['类型'].unique()
colors = plt.cm.tab10.colors[:len(types)]
type_color_dict = dict(zip(types, colors))

# 为每个类型分配颜色
colors_mapped = new_house_df['类型'].map(type_color_dict)

plt.scatter(new_house_df['均价(元/㎡)'], new_house_df['总价(万元)'], c=colors_mapped)

# 创建图例
legend_elements = [Line2D([0], [0], marker='o', color='w', label=type_name,
                          markerfacecolor=color, markersize=10)
                   for type_name, color in type_color_dict.items()]
plt.legend(handles=legend_elements, title='类型')

plt.xlabel('均价(元/㎡)')
plt.ylabel('总价(万元)')
plt.title('楼盘价格分布散点图')
plt.savefig('house_data_pics/unit_total_pic.png')

# 可视化2：绘制各行政区楼盘的直方图
# 每个行政区一个柱子，高度代表平均单价，宽度代表楼盘数量

# 按行政区分组，计算平均单价和楼盘数量
grouped = new_house_df.groupby('行政区').agg({
    '均价(元/㎡)': 'mean',
    '总价(万元)': 'mean',
    '楼盘名称': 'count'
}).rename(columns={'楼盘名称': '楼盘数量'}).reset_index()

# 规范化楼盘数量，以控制柱子的宽度在合理范围内
max_width = 0.8  # 最大柱子宽度
min_width = 0.2  # 最小柱子宽度

# 计算楼盘数量的范围
num_min = grouped['楼盘数量'].min()
num_max = grouped['楼盘数量'].max()

# 根据楼盘数量计算柱子宽度
grouped['width'] = min_width + (grouped['楼盘数量'] - num_min) / (num_max - num_min) * (max_width - min_width)

# 绘制平均单价的柱状图，柱子宽度根据楼盘数量调整
plt.figure(figsize=(12, 6))

# 计算每个柱子的中心位置
x = np.arange(len(grouped))
widths = grouped['width'].values

# 绘制柱状图
for i in range(len(grouped)):
    plt.bar(x[i], grouped['均价(元/㎡)'].iloc[i], width=widths[i], color='skyblue', align='center')

# 设置x轴刻度和标签
plt.xticks(x, grouped['行政区'])

# 在柱子上标注楼盘数量
for i in range(len(grouped)):
    plt.text(x[i], grouped['均价(元/㎡)'].iloc[i], f'数量:{grouped["楼盘数量"].iloc[i]}', ha='center', va='bottom')

plt.xlabel('行政区')
plt.ylabel('平均单价(元/㎡)')
plt.title('各行政区楼盘平均单价与数量（柱子宽度代表楼盘数量）')
plt.savefig('house_data_pics/area_unit_number_pic.png')

# 将单价换为总价再绘制一张直方图，同样调整柱子宽度

plt.figure(figsize=(12, 6))

for i in range(len(grouped)):
    plt.bar(x[i], grouped['总价(万元)'].iloc[i], width=widths[i], color='orange', align='center')

# 设置x轴刻度和标签
plt.xticks(x, grouped['行政区'])

# 在柱子上标注楼盘数量
for i in range(len(grouped)):
    plt.text(x[i], grouped['总价(万元)'].iloc[i], f'数量:{grouped["楼盘数量"].iloc[i]}', ha='center', va='bottom')

plt.xlabel('行政区')
plt.ylabel('平均总价(万元)')
plt.title('各行政区楼盘平均总价与数量（柱子宽度代表楼盘数量）')
plt.savefig('house_data_pics/area_total_number_pic.png')

# 可视化3：增加其他表现数据特点的图表
# 设计思路：展示不同类型楼盘的数量分布，了解市场上不同类型的供应情况

type_counts = new_house_df['类型'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('楼盘类型分布')
plt.axis('equal')
plt.savefig('house_data_pics/house_type_pic.png')