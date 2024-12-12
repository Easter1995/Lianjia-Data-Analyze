import pandas as pd
import re

# 返回小数平均值
def get_avg_float(str):
    if pd.isnull(str) or str == '':
        return None
    nums = re.findall(r'(\d+)', str)
    if nums:
        nums = [float(n) for n in nums]
        return sum(nums) / len(nums)

# 返回整数平均值
def get_avg_integer(str):
    if pd.isnull(str) or str == '':
        return None
    nums = re.findall(r'(\d+)', str)
    if nums:
        nums = [int(n) for n in nums]
        return int(sum(nums) / len(nums))

# 处理二手房的houseType字段
def get_house_type(str):
    info = str.split(' | ')
    data = {
        'rooms': None,
        'square': None,
    }
    # 房间
    nums = re.findall(r'(\d+)', info[0])
    data['rooms'] = nums[0]
    # 面积
    square = re.findall(r'(\d+\.?\d*)', info[1])
    data['square'] = float(square[0])
    return pd.Series(data)


file_path_new = 'original_data/NewHouse.json'
file_path_second = 'original_data/SecondHandHouse.json'
# 读取json数据
data_new = pd.read_json(file_path_new)
data_second = pd.read_json(file_path_second)

# 新房数据处理

# 去除空格
string_fields = ['name', 'location', 'type', 'houseType', 'square', 'unitPrice', 'totalPrice']
for field in string_fields:
    data_new[field] = data_new[field].astype(str).str.strip()
# 地理位置: 三个字段分别存储
data_new[['district', 'area', 'address']] = data_new['location'].str.split(' / ', expand=True, n=2)
# 房型: 提取平均房型
data_new['houseType_avg'] = data_new['houseType'].apply(get_avg_float)
# 面积：提取平均面积
data_new['square_avg'] = data_new['square'].apply(get_avg_float)
# 总价：单位为万/套
data_new['totalPrice_avg'] = data_new['totalPrice'].apply(get_avg_integer)
# 均价：单位为元(整数)
data_new['unitPrice_avg'] = data_new['unitPrice'].apply(get_avg_integer)

# 二手房数据处理

# 去除空格
string_fields = ['name', 'location', 'houseType', 'unitPrice', 'totalPrice']
for field in string_fields:
    data_second[field] = data_second[field].astype(str).str.strip()
# 地理位置：小区名+街道名
data_second[['community', 'street']] = data_second['location'].str.split('  - ', expand=True)
# 房型+面积：处理houseType字段
house_info = data_second['houseType'].apply(get_house_type)
data_second = pd.concat([data_second, house_info], axis=1) # 合并列
# 总价：单位为万/套
data_second['totalPrice_avg'] = data_second['totalPrice'].apply(get_avg_integer)
# 均价：单位为元(整数)
data_second['unitPrice_avg'] = data_second['unitPrice'].apply(get_avg_integer)

# 保存最终数据

# 新房数据
new_house_final_columns = {
    'name': '楼盘名称',
    'type': '类型',
    'district': '行政区',
    'area': '区域',
    'address': '地址',
    'houseType_avg': '平均房型(室)',
    'square_avg': '平均面积(㎡)',
    'totalPrice_avg': '总价(万元)',
    'unitPrice_avg': '均价(元/㎡)'
}
data_new_final = data_new[list(new_house_final_columns.keys())].rename(columns=new_house_final_columns)
data_new_final.to_csv('processed_data/processed_new_house.csv', index=False)

# 二手房数据
second_hand_final_columns = {
    'community': '小区',
    'street': '街道',
    'rooms': '房型(室)',
    'square': '面积(㎡)',
    'totalPrice_avg': '总价(万元)',
    'unitPrice_avg': '均价(元/㎡)'
}
data_secondhand_final = data_second[list(second_hand_final_columns.keys())].rename(columns=second_hand_final_columns)
data_secondhand_final.to_csv('processed_data/processed_second_hand_house.csv', index=False)