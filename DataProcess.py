import pandas as pd
import re
import os

city_names = ['bj', 'sh', 'sz', 'gz', 'dali']
city_mapping = {
    'bj': '北京',
    'sh': '上海',
    'sz': '深圳',
    'gz': '广州',
    'dali': '大理'
}

# 数据预处理汇总
def data_merge():
    global city_names
    print("merge data......")

    # 合并数据
    merged_data = []

    for name in city_names:
        data = pd.read_json(f'original_data/{name}.json')
        merged_data.append(data)

    combined_df = pd.concat(merged_data, ignore_index=True)

    # 将 'city' 列中的英文名映射为中文名
    combined_df['城市'] = combined_df['city'].map(city_mapping)

    # 提取居室的信息
    combined_df['居室'] = combined_df['layout'].apply(extract_room)

    # 重命名列头为中文
    columns = {
        "city": "城市代号",
        "城市": "城市",
        "name": "房源名称",
        "district": "区域",
        "street": "街道",
        "community": "小区",
        "price": "价格（元/月）",
        "square": "面积（㎡）",
        "price_per_m2": "单价（元/㎡）",
        "direction": "朝向",
        "layout": "户型",
        "居室": "居室"
    }
    combined_df = combined_df.rename(columns=columns)

    # 导出数据到csv文件
    combined_df.to_csv('processed_data/renting_data.csv', index=False, encoding='utf-8-sig')
    print('data processed successfully......')
    
def extract_room(layout):
    if not layout or not isinstance(layout, str):  # 如果为空或非字符串
        return ''  # 返回空字符串
    return layout.split('室')[0] if '室' in layout else ''

data_merge()

# 各城市数据统计
def calculate_city_statistics():
    print("calculate data statistics......")
    df = pd.read_csv('processed_data/renting_data.csv')
    df['价格（元/月）'] = pd.to_numeric(df['价格（元/月）'], errors='coerce')
    df['单价（元/㎡）'] = pd.to_numeric(df['单价（元/㎡）'], errors='coerce')
    df.dropna(subset=['价格（元/月）', '单价（元/㎡）'], inplace=True)

    # 按城市分组，计算统计信息
    summary = df.groupby('城市').agg(
        租金均价=('价格（元/月）', 'mean'),
        租金最高价=('价格（元/月）', 'max'),
        租金最低价=('价格（元/月）', 'min'),
        租金中位数=('价格（元/月）', 'median'),
        单位面积租金均价=('单价（元/㎡）', 'mean'),
        单位面积租金最高价=('单价（元/㎡）', 'max'),
        单位面积租金最低价=('单价（元/㎡）', 'min'),
        单位面积租金中位数=('单价（元/㎡）', 'median')
    ).reset_index()

    # 保留两位小数
    summary = summary.round({
        '租金均价': 2,
        '租金最高价': 2,
        '租金最低价': 2,
        '租金中位数': 2,
        '单位面积租金均价': 2,
        '单位面积租金最高价': 2,
        '单位面积租金最低价': 2,
        '单位面积租金中位数': 2
    })

    # 保存汇总结果到 CSV
    summary.to_csv('processed_data/renting_data_sta.csv', index=False, encoding='utf-8-sig')
    print('calculate data statistics successfully......')

calculate_city_statistics()
