import pandas as pd
from pyecharts.charts import Bar, Grid, Bar3D, Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType

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

# 5个城市的板块均价分布
# def street_price_analyze():


# 单位月租和整体月租的分析
price_analyze()
# 居室价格的分析
layout_price_analyze()
# 5个城市的板块均价分布
# street_price_analyze()