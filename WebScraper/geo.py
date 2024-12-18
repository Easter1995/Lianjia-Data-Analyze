import pandas as pd
import requests
import json
import time

# 城市代码和名称的映射
city_codes = ['bj', 'sh', 'gz', 'sz', 'dali']

city_names = {
    'bj': '北京',
    'sh': '上海',
    'gz': '广州',
    'sz': '深圳',
    'dali': '大理'
}

def get_one_point(city_info):
    url = 'https://apis.map.qq.com/ws/geocoder/v1'
    city = city_info['城市']
    params = {
        'address': f"{city}市{city_info['区域']}区{city_info['街道']}",
        'key': 'IRFBZ-F2CKZ-VR4XH-ZMLT5-YAMDK-EZFWY'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if data.get('status') == 0:
        result = data.get('result')
        location = result.get('location') if result else None
        if location:
            return {
                'longitude': location.get('lng'),
                'latitude': location.get('lat')
            }
        else:
            return None
    else:
        print(f"API 错误: {data.get('message', '未知错误')}")
        return None

def crawl_point(city_code):
    # 读取 CSV 文件
    file_path = f'processed_data/street_price/{city_code}.csv'
    origin = pd.read_csv(file_path)
    print(f"开始处理城市代码: {city_code} ({city_names[city_code]})")

    data = []
    for index, row in origin.iterrows():
        # 获取经纬度信息
        point = get_one_point(row)
        if point:
            print(f"成功获取: {city_names[city_code]} {row['区域']} {row['街道']}")
            data.append({
                'city_code': city_code,
                'city_name': city_names[city_code],
                'district': row['区域'],
                'street': row['街道'],
                'x': point['latitude'],
                'y': point['longitude'],
            })
        time.sleep(0.3)

    # 保存到 JSON 文件
    output_path = f'original_data/pos/{city_code}.json'
    with open(output_path, 'w+', encoding='utf-8') as pos_file:
        json.dump(data, pos_file, indent=4, ensure_ascii=False)
    print(f"完成处理城市代码: {city_code}")

def crawl_pos():
    for city_code in city_codes:
        crawl_point(city_code)
        time.sleep(1)

crawl_pos()