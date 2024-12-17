import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

js_code = """
    document.addEventListener("DOMContentLoaded", function() {
        const chartContainer = document.querySelector(".chart-container");
        if (chartContainer) {
            chartContainer.style.margin = "auto";
            chartContainer.style.display = "flex";
            chartContainer.style.justifyContent = "center";
        }
    });
    """

# 5个城市的总体房租情况
def price_analyze():
    # 读取数据
    df = pd.read_csv('processed_data/renting_data_sta.csv')

    # 创建Bar图（柱状图）来展示每个城市的租金数据
    bar = Bar(init_opts=opts.InitOpts(width="900px", height="700px", page_title="租金统计图"))

    # 设置X轴和Y轴
    rent_types = ['租金均价', '租金最高价', '租金最低价', '租金中位数']

    shanghai = [float(df.loc[df['城市'] == '上海', col].values[0]) for col in rent_types]
    beijing = [float(df.loc[df['城市'] == '北京', col].values[0]) for col in rent_types]
    dali = [float(df.loc[df['城市'] == '大理', col].values[0]) for col in rent_types]
    guangzhou = [float(df.loc[df['城市'] == '广州', col].values[0]) for col in rent_types]
    shenzhen = [float(df.loc[df['城市'] == '深圳', col].values[0]) for col in rent_types]

    bar.add_xaxis(rent_types)
    bar.add_yaxis("上海", shanghai, color='#1f77b4')
    bar.add_yaxis("北京", beijing, color='#ff7f0e')
    bar.add_yaxis("大理", dali, color='#2ca02c')
    bar.add_yaxis("广州", guangzhou, color='#d62728')
    bar.add_yaxis("深圳", shenzhen, color='#9467bd')

    # 配置图表的全局选项
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="各城市租房月租分析"),
        legend_opts=opts.LegendOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(name="租金类型"),
        yaxis_opts=opts.AxisOpts(name="租金（元）"),
        tooltip_opts=opts.TooltipOpts(is_show=True)
    )

    # 设置对数坐标轴
    bar.set_global_opts(
        yaxis_opts=opts.AxisOpts(type_="log"),
        title_opts=opts.TitleOpts(title="不同城市租金统计"),
    )
    bar.add_js_funcs(js_code)
    # 渲染为HTML文件
    bar.render('house_data_tables/pyecharts/price_all.html')


price_analyze()
