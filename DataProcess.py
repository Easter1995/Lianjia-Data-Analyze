import pandas as pd
import re
import os

city_names = ['bj', 'sh', 'sz', 'gz', 'dali']

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

    # 提取居室的信息
    combined_df['居室'] = combined_df['layout'].apply(extract_room)

    # 重命名列头为中文
    columns = {
        "city": "城市",
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