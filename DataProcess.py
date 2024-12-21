import re
import pandas as pd

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

    # 异常值判断函数
    def is_valid(item):
        # 车库和未知户型去除
        if item["name"] and "车库" in item["name"]:
            return False
        if item["layout"] and "未知" in item["layout"]:
            return False
        # 单价异常值去除
        if item["price_per_m2"] <= 2:
            return False
        # 面积异常值去除
        if item["square"] < 10 or item["square"] > 2000:
            return False
        # 总价格异常值去除
        if item["price"] < 100:
            return False
        return True

    for name in city_names:
        unique_data = set()  # 用于去重后的数据存储
        data = pd.read_json(f'original_data/{name}.json')

        # 数据清洗和去重处理
        data['城市'] = data['city'].map(city_mapping)
        data['居室'] = data['layout'].apply(extract_room)
        
        # 过滤异常值
        cleaned_data = data[data.apply(is_valid, axis=1)]
        
        # 将每一行的数据转化为元组，添加到集合中实现去重
        for index, row in cleaned_data.iterrows():
            row_tuple = tuple(row.values)  # 获取整行的值作为元组
            unique_data.add(row_tuple)  # 将元组添加到集合中去重

        cleaned_data = pd.DataFrame(list(unique_data), columns=cleaned_data.columns)  # 转换回DataFrame格式

        # 重命名列头
        cleaned_data = cleaned_data.rename(columns=columns)
        
        # 导出每个城市的处理后的数据
        cleaned_data.to_csv(f'processed_data/{name}.csv', index=False)

        # 将清洗后的数据合并到整体数据中
        merged_data.append(cleaned_data)

    # 合并所有城市的数据
    combined_df = pd.concat(merged_data, ignore_index=True)

    # 导出数据到csv文件
    combined_df.to_csv('processed_data/renting_data.csv', index=False, encoding='utf-8-sig')

    print('data processed successfully......')
    
def extract_room(layout):
    if not layout or not isinstance(layout, str):  # 如果为空或非字符串
        return ''  # 返回空字符串
    match = re.search(r'(\d+)(?=室|房间)', layout)
    if match:
        return int(match.group(1))  # 返回匹配到的数字
    else:
        return ''


# 各城市数据统计
def calculate_city_statistics():
    print('city rent price analyza start...')
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
    summary.to_csv('processed_data/renting_price_sta.csv', index=False, encoding='utf-8-sig')
    print('city rent price analyza end...')


# 计算5个城市居室的情况
def calculate_layout_statistics():
    print('city rent layout-price analyza start...')
    df = pd.read_csv('processed_data/renting_data.csv')
    
    # 将四居室以上合并为 "四居室以上"
    df['居室'] = df['居室'].apply(lambda x: 4.0 if x >= 4 else x)
    
    grouped = df.groupby(['城市代号', '城市', '居室'])
    
    # 计算均价、最高价、最低价、中位数 
    summary = grouped['价格（元/月）'].agg(
        avg='mean',
        max='max',
        low='min',
        mid='median'
    ).reset_index()

    summary = summary.round({
        'avg': 2,
        'max': 2,
        'low': 2,
        'mid': 2
    })
    
    summary.to_csv('processed_data/renting_layout_sta.csv', index=False, encoding='utf-8-sig')
    print('city rent layout-price analyza end...')


# 计算5个城市不同板块的均价
def calculate_street_statistics(city_name):
    print('city rent street-price analyza end...')

    df = pd.read_csv(f'processed_data/{city_name}.csv')
    grouped = df.groupby(['城市代号', '城市', '街道', '区域'])
    # 计算均价
    summary = grouped['价格（元/月）'].agg(avg='mean').reset_index()
    summary = summary.round({'avg': 2})
    summary.to_csv(f'processed_data/street_price/{city_name}.csv', index=False, encoding='utf-8-sig')
    print('city rent street-price analyza end...')


data_merge() # 将五个城市的数据合并
calculate_city_statistics() # 计算各城市的租金统计数据
calculate_layout_statistics() # 计算各居室类型的租金统计数据
for city in city_names:
    calculate_street_statistics(city) # 计算各城市不同板块的租金数据