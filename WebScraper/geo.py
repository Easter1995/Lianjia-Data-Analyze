import requests
import json
import time

city_codes = ['bj','sh','gz','sz','xm']

city_names = {
    'bj':'北京',
    'sh':'上海',
    'gz':'广州',
    'sz':'深圳',
    'dali':'大理'
}

def get_one_point(city_info):
    url = 'https://apis.map.qq.com/ws/geocoder/v1'
    city = city_names[city_info['city']]
    params = {
        'address': city + city_info['district'] + city_info['area'],
        'key': 'IRFBZ-F2CKZ-VR4XH-ZMLT5-YAMDK-EZFWY'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果请求出现4xx、5xx等错误状态码，抛出异常
        data = response.json()  # 直接将响应解析为JSON格式的数据（相当于json.loads(response.text)）
        if data.get('status') == 0:  # 假设接口返回的成功状态码是0，根据实际接口文档调整判断逻辑
            result = data.get('result')
            location = result.get('location') if result else None
            if location:
                return {
                    'longitude': location.get('lng'), # 获取经度信息，不同接口可能字段名有差异，按需调整
                    'latitude': location.get('lat')  # 获取纬度信息
                }
            else:
                return None
        else:
            return None
    except requests.RequestException as e:
        return None

def crawl_point(city_code):
    with open(f'url_data/{city_code}.json', 'r', encoding='utf-8') as file:
        origin = json.load(file)
    data = []
    for city_info in origin:
        if city_info['total'] == '0':
            continue
        point = get_one_point(city_info)
        print(f'{city_names[city_info['city']]}{city_info['area']}{city_info['area']}')
        if point:
            data.append({
                'city_code': city_info['city'],
                'city_name': city_names[city_info['city']],
                'district': city_info['district'],
                'street': city_info['area'],
                'total': city_info['total'],
                'x': point['latitude'],
                'y': point['longitude'],
            })
        time.sleep(0.1)
    
    with open(f'original_data/pos/{city_code}.json', 'w+', encoding='utf-8') as pos_file:
        json.dump(data, pos_file, indent=4, ensure_ascii=False)
        pos_file.close()

def crawl_pos():
    for city_code in city_codes:
        crawl_point(city_code)
        time.sleep(0.5)

crawl_pos()
