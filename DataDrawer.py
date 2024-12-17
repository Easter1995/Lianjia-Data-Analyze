import pandas as pd
from pyecharts.charts import Bar, Grid
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
    df = pd.read_csv('processed_data/renting_data_sta.csv')

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
    grid = Grid(init_opts=opts.InitOpts(width='1200px',height='770px'))
    grid.add(bar_all, grid_opts=opts.GridOpts(pos_top='12%',pos_bottom='50%')) # 组合月租金图
    grid.add(bar_unit, grid_opts=opts.GridOpts(pos_top='56%')) # 组合单位面积月租金图
    grid.add_js_funcs(js_code)
    grid.render('house_data_tables/pyecharts/price_combine.html')  # 绘制保存


price_analyze()