import json
import pandas as pd
from pyecharts.charts import Bar, Grid, Bar3D, Geo, Radar, Line
from pyecharts import options as opts
from pyecharts.globals import GeoType
from collections import defaultdict
import matplotlib as mpl

js_code = """
    document.addEventListener("DOMContentLoaded", function() {
        const chartContainer = document.querySelector(".chart-container");
        if (chartContainer) {
            chartContainer.style.margin = "auto";
            chartContainer.style.display = "flex";
            chartContainer.style.justifyContent = "center";
            chartContainer.style.padding = "20px";
            
        }
    });
    """
city_codes = ['bj', 'sh', 'gz', 'sz', 'dali']
city_names = {
    'bj':'北京',
    'sh':'上海',
    'gz':'广州',
    'sz':'深圳',
    'dali':'大理'
}

# 根据类型的最大值来产生颜色
def generate_color(max_value):
    res = []
    cur = 0
    path = 1000
    while cur <= max_value:
        res.append({'min': cur, 'max': cur + path, 'color': '#'})
        cur += path
        path = 100000 if cur >= 100000 else (10000 if cur >= 10000 else 1000)
    cmap = mpl.cm.get_cmap('RdYlBu_r', len(res))(range(len(res)))
    for i in range(len(res)):
        rgb = cmap[i]
        code = '#'
        for j in range(3):
            code += str(hex(int(rgb[j]*255)))[-2:].replace('x', '0').upper()
        res[i]['color'] = code
    return res

# 5个城市的总体房租情况
def price_analyze():
    # 读取数据
    df = pd.read_csv('processed_data/renting_price_sta.csv')

    # 创建Bar图（柱状图）来展示每个城市的租金数据
    bar_all = Bar(init_opts=opts.InitOpts(width="900px", height="700px", page_title="租金统计图"))

    # 设置X轴和Y轴
    data_types = ['租金均价', '租金最高价', '租金最低价', '租金中位数']

    shanghai = [float(df.loc[df['城市'] == '上海', col].values[0]) for col in data_types]
    beijing = [float(df.loc[df['城市'] == '北京', col].values[0]) for col in data_types]
    dali = [float(df.loc[df['城市'] == '大理', col].values[0]) for col in data_types]
    guangzhou = [float(df.loc[df['城市'] == '广州', col].values[0]) for col in data_types]
    shenzhen = [float(df.loc[df['城市'] == '深圳', col].values[0]) for col in data_types]

    bar_all.add_xaxis(data_types)
    bar_all.add_yaxis("上海", shanghai, color='#1f77b4')
    bar_all.add_yaxis("北京", beijing, color='#ff7f0e')
    bar_all.add_yaxis("大理", dali, color='#2ca02c')
    bar_all.add_yaxis("广州", guangzhou, color='#d62728')
    bar_all.add_yaxis("深圳", shenzhen, color='#9467bd')

    # 配置图表的全局选项
    bar_all.set_global_opts(
        title_opts=opts.TitleOpts(title="各城市租房月租分析", pos_left="center"),
        legend_opts=opts.LegendOpts(is_show=True, pos_right=True),
        xaxis_opts=opts.AxisOpts(name="租金类型"),
        yaxis_opts=opts.AxisOpts(name="月租(元/月)", type_="log"),
        tooltip_opts=opts.TooltipOpts(is_show=True)
    )
    
    # 创建Bar图（柱状图）来展示每个城市的租金数据
    bar_unit = Bar(init_opts=opts.InitOpts(width="900px", height="700px", page_title="租金统计图"))
    
    # 设置X轴和Y轴
    data_types = ['单位面积租金均价', '单位面积租金最高价', '单位面积租金最低价', '单位面积租金中位数']
    shanghai = [float(df.loc[df['城市'] == '上海', col].values[0]) for col in data_types]
    beijing = [float(df.loc[df['城市'] == '北京', col].values[0]) for col in data_types]
    dali = [float(df.loc[df['城市'] == '大理', col].values[0]) for col in data_types]
    guangzhou = [float(df.loc[df['城市'] == '广州', col].values[0]) for col in data_types]
    shenzhen = [float(df.loc[df['城市'] == '深圳', col].values[0]) for col in data_types]

    bar_unit.add_xaxis(data_types)
    bar_unit.add_yaxis("上海", shanghai, color='#1f77b4')
    bar_unit.add_yaxis("北京", beijing, color='#ff7f0e')
    bar_unit.add_yaxis("大理", dali, color='#2ca02c')
    bar_unit.add_yaxis("广州", guangzhou, color='#d62728')
    bar_unit.add_yaxis("深圳", shenzhen, color='#9467bd')

    # 配置图表的全局选项
    bar_unit.set_global_opts(
        title_opts=opts.TitleOpts(title="各城市租房单位面积租金分析", pos_bottom=True, pos_left="center"),
        xaxis_opts=opts.AxisOpts(name="租金类型", position="top"),
        yaxis_opts=opts.AxisOpts(name="租金(元/㎡)", type_="log", is_inverse=True),
        tooltip_opts=opts.TooltipOpts(is_show=True),
        legend_opts=opts.LegendOpts(is_show=False) 
    )

    # 将两个Bar图结合为Grid图
    grid = Grid(init_opts=opts.InitOpts(width='1200px',height='770px',page_title="租金统计"))
    grid.add(bar_all, grid_opts=opts.GridOpts(pos_top='12%',pos_bottom='50%')) # 组合月租金图
    grid.add(bar_unit, grid_opts=opts.GridOpts(pos_top='56%')) # 组合单位面积月租金图
    grid.add_js_funcs(js_code)
    grid.render('house_data_tables/pyecharts/price_combine.html')  # 绘制保存

# 5个城市不同居室的房租情况
def layout_price_analyze():
    df = pd.read_csv('processed_data/renting_layout_sta.csv')
    
    layout_types = [1.0, 2.0, 3.0, 4.0]
    data_types = ['low', 'avg', 'mid', 'max']
    
    cities = df['城市代号'].unique()
    
    # 初始化 city_data 为字典，确保每个城市每个居室类型都是字典
    city_data = {city: {layout: {} for layout in layout_types} for city in cities}
    
    for city in cities:
        for layout in layout_types:
            for data_type in data_types:
                # 获取对应的价格数据
                price_value = df.loc[(df['城市代号'] == city) & (df['居室'] == layout), data_type].values
                if price_value:
                    # 确保存储在字典中
                    city_data[city][layout][data_type] = float(price_value[0])

    # 准备数据：x轴为居室类型和城市组合，y轴为价格类型，z轴为价格
    data = []
    city_name = {'bj': '北京', 'dali': '大理', 'gz': '广州', 'sh': '上海', 'sz': '深圳'}
    label = []
    layout_tags = ['\n一居', '\n二居', '\n三居', '\n四居及以上']
    city_name = {'bj': '北京', 'dali': '大理', 'sh': '上海', 'gz': '广州', 'sz': '深圳'}

    # 构造 x 轴标签：每个居室类型和城市的组合
    for tag in layout_tags:
        for city in city_name.values():
            label.append(f"{city}\n{tag}" if city == '北京' else f"{city}")


    # 构造 3D 数据，分别为 x, y, z
    
    for i in range(1, 5):
        n = 0  # 用于控制 y 轴位置
        for city in cities:
            tmp = city_data[city][float(f'{i}.0')]
            m = 0
            for key in tmp:
                data.append([(i-1)*5+n,m,tmp[key] if key != '最高租金' else int(tmp[key]/10) ])
                m += 1
            n += 1

    # 创建三维柱状图
    bar3d = Bar3D(init_opts=opts.InitOpts(width='1500px',height='750px',page_title="不同户型的月租分析"))
    
    bar3d.add(
        series_name='月租金',
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(
            type_='category',
            data=label,
            axislabel_opts=opts.LabelOpts(
                interval=0,
                rotate=45
            )
        ),
            yaxis3d_opts=opts.Axis3DOpts(
            name='数据类型',
            type_='category',
            data=['最小值', '平均值', '中位数', '最大值'],
            textstyle_opts=opts.TextStyleOpts(font_weight='bold', font_size=13)
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            name='月租金',
            type_='log',
            textstyle_opts=opts.TextStyleOpts(font_weight='bold', font_size=13)
        )
    )

    # 设置全局选项
    bar3d.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(
            max_=100000,
            range_color=["#313695","#4575B4","#74ADD1","#ABD9E9","#E0F3F8","#FFFFbF","#FEE090","#FDAE61","#F46D43","#D73027",],
        ),
        title_opts=opts.TitleOpts(title='各城市不同户型月租金数据分布'),
        legend_opts=opts.LegendOpts()
    )

    bar3d.add_js_funcs(js_code)

    # 渲染图表
    bar3d.render('house_data_tables/pyecharts/layout_price_3d.html')

# 5个城市的街道价格分析
def street_price_analyze(city_code):
    # 读取 CSV 文件
    df = pd.read_csv(f'processed_data/street_price/{city_code}.csv')
    with open(f'original_data/pos/{city_code}.json', 'r', encoding='utf-8') as f:
        pos_data = json.load(f)
    
    # 获取城市名称
    city_name = city_names[city_code]
    if city_code == 'dali':
        city_name = '大理白族自治州'
    g = Geo(init_opts=opts.InitOpts(width='1500px', height='750px', page_title='不同板块的平均月租'))

    g.add_schema(maptype=city_name)
    
    # 准备数据对
    data_pair = [(row['街道'], row['avg']) for _, row in df.iterrows()]
    data_pair.sort(key=lambda x:x[1])

    for data in pos_data:
        g.add_coordinate(data['street'], data['y'], data['x'])

    # 添加数据到Geo图
    g.add('', data_pair, type_=GeoType.EFFECT_SCATTER, symbol_size=5)
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    # 颜色映射
    max_price = max(price for _, price in data_pair)
    pieces = generate_color(max_price)
    g.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces),
        title_opts=opts.TitleOpts(title=f'{city_name}市不同板块平均月租分布图(元/月)', pos_left='5%')
    )

    # 渲染图表
    g.render(f'house_data_tables/street_price/{city_code}.html')
    
# 5个城市的不同朝向的价格分析
def direction_price_analyze():
    # 提取所有朝向
    directions = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]

    ori_avgs = []
    max_radar = 0

    # 统计每个城市的朝向的单价
    for city_code in city_codes:
        ori_prices = defaultdict(list)
        df = pd.read_csv(f'processed_data/{city_code}.csv')
        
        # 计算平均值，将南 北这样的朝向算进朝南和朝北
        for _, row in df.iterrows():
            price_per_m2 = row['单价（元/㎡）'] # 提取单价
            if isinstance(row['朝向'], str) and row['朝向'] != 'nan':
                oris = row['朝向'].split()
            else:
                continue  # 如果是 NaN 或无效值，跳过

            for ori in oris:
                if ori in directions:
                    ori_prices[ori].append(price_per_m2) # 将单价装入对应的朝向

        orientation_avg = {orientation: round(sum(prices) / len(prices), 2) for orientation, prices in ori_prices.items()}
        max_item = max(orientation_avg.values())
        if max_item > max_radar:
            max_radar = max_item

        ori_avgs.append({city_code: orientation_avg})
    
    # 画雷达图
    radar = (
        Radar(init_opts=opts.InitOpts(width='1500px', height='750px', page_title='5个城市不同朝向房屋价格分析'))
        .add_schema(
            schema=[opts.RadarIndicatorItem(name=direction, max_=max_radar) for direction in directions]
        )
    )
    color_list = ['#5793f3', '#d14a61', '#675bba', '#f58220', '#91cc75']  # 定义不同颜色列表，用于区分不同城市
    for index, data in enumerate(ori_avgs):
        city_code = list(data.keys())[0]
        city_name = city_names[list(data.keys())[0]]  # 获取对应的中文城市名称
        orientation_avg = data[city_code]
        values = [orientation_avg.get(direction, 0) for direction in directions]  # 获取对应方向的价格平均值，不存在则设为0
        radar.add(city_name, [values], color=color_list[index % len(color_list)],
                  label_opts=opts.LabelOpts(is_show=True))  # 添加数据到雷达图，设置不同颜色及显示标签

    radar.set_global_opts(
        title_opts=opts.TitleOpts(title="5个城市不同朝向房屋价格分析", pos_left='center'),
        legend_opts=opts.LegendOpts(pos_top='5%', pos_left='center')
    )

    radar.add_js_funcs(js_code)

    radar.render('house_data_tables/pyecharts/orientation_unit_price.html')
    
# 5个城市的人均gdp和单位面积租金分布的关系
def gdp_unit_price_analyze():
    with open('original_data/gdp/gdp.json', 'r', encoding='utf-8') as file:
        gdp_file = json.load(file)

    gdp = [item["gdp"] for item in gdp_file]
    salary = [item["salary"] for item in gdp_file]

    # 准备单位面积租金的数据
    data = {}
    data['avg'] = list()
    data['mid'] = list()
    for city_code in city_codes:
        df = pd.read_csv(f'processed_data/{city_code}.csv')
        avg_unit_price = round(df['单价（元/㎡）'].mean(), 2)
        mid_unit_price = round(df['单价（元/㎡）'].median(), 2)    
        data['avg'].append(avg_unit_price)
        data['mid'].append(mid_unit_price)
    
    # 初始化柱状图
    b = Bar(init_opts=opts.InitOpts(width='1400px', height='550px', page_title='人均gdp和单位面积租金分布关系分析'))
    b.add_xaxis([city_names[city_code] for city_code in city_codes])
    b.add_yaxis('单位面积月租金中位数', data['mid'], itemstyle_opts=opts.ItemStyleOpts(color='#f882b1'), z = 0)
    b.add_yaxis('单位面积月租金平均数', data['avg'], itemstyle_opts=opts.ItemStyleOpts(color='#ed9d5f'), z = 0)

    # 添加额外的坐标轴
    b.extend_axis(
        yaxis=opts.AxisOpts(name='人均GDP', name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'), position="right",
        axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#B22222")))
    )
    b.extend_axis(
        yaxis=opts.AxisOpts(name='人均工资', max_=max(salary), name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'), position="right", offset=60,
        axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="#5d2673")))
    )

    # 设置全局配置选项
    b.set_global_opts(
        legend_opts=opts.LegendOpts(selected_mode="mutiple", orient="horizontal", pos_bottom="bottom", pos_left='center'),
        title_opts=opts.TitleOpts(title="各城市相关数据分布概览", pos_left='%5'),
        yaxis_opts=opts.AxisOpts(
            name='租金',
            max_= max(map(int, data['avg'])) + 50,
            axislabel_opts=opts.LabelOpts(formatter="{value} 元/平米"),
            name_textstyle_opts=opts.TextStyleOpts(font_weight='bold'),
            splitline_opts=opts.SplitLineOpts(is_show=False)
        ),
        xaxis_opts=opts.AxisOpts(name='城市', position='bottom', axislabel_opts=opts.LabelOpts(font_weight='bold', font_size=13))
    )

    # 初始化折线图并添加数据
    l = Line(init_opts=opts.InitOpts(width='1100px', height='550px'))
    l.add_xaxis([city_names[city_code] for city_code in city_codes])
    l.add_yaxis('人均GDP', y_axis = gdp, yaxis_index=1, itemstyle_opts=opts.ItemStyleOpts(color='#B22222'),
        label_opts=opts.LabelOpts(font_weight='bold'),
        symbol_size=15, symbol='circle',
        linestyle_opts=opts.LineStyleOpts(width=2, type_="dashed"))

    l2 = Line(init_opts=opts.InitOpts(width='1100px', height='550px'))
    l2.add_xaxis([city_names[city_code] for city_code in city_codes])
    l2.add_yaxis('人均工资性收入', y_axis = salary, yaxis_index=2, itemstyle_opts=opts.ItemStyleOpts(color='#5d2673'),
        label_opts=opts.LabelOpts(font_weight='bold'),
        symbol_size=15, symbol='circle',
        linestyle_opts=opts.LineStyleOpts(width=2, type_="dashed"))

    # 叠加折线图到柱状图上
    b.overlap(l)
    b.overlap(l2)

    # 渲染图表
    b.add_js_funcs(js_code)
    b.render('house_data_tables/pyecharts/gdp_salary.html')


price_analyze() # 单位月租和整体月租的分析
layout_price_analyze() # 居室价格的分析
for city_code in city_codes:
    street_price_analyze(city_code) # 5个城市的板块均价分布
direction_price_analyze() # 5个城市的不同朝向的价格分析
gdp_unit_price_analyze() # 5个城市的人均gdp和单位面积租金分布的关系