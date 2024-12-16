import json
import os

class URLPipeline:
    def __init__(self):
        self.files = {}  # 存储打开的文件句柄
        self.first_item = {}  # 用于标记每个城市是否已经写入过第一个 item

    def open_spider(self, spider):
        # 创建目录以保存 JSON 文件
        if not os.path.exists("url_data"):
            os.makedirs("url_data")

    def process_item(self, item, spider):
        city_name = item['city']
        
        if city_name not in self.files:
            # 为每个城市创建文件，写入一个开头的 '['，开始写入 JSON 数组
            file_path = f"url_data/{city_name}.json"
            self.files[city_name] = open(file_path, 'w+', encoding='utf-8')
            self.files[city_name].write('[\n')
            self.first_item[city_name] = True  # 标记这个城市是第一项

        # 写入单个 item 数据
        item_json = json.dumps(dict(item), ensure_ascii=False)
        
        # 如果不是第一项，添加逗号
        if not self.first_item[city_name]:
            self.files[city_name].write(',\n')
        
        # 写入数据并标记已经写过第一项
        self.files[city_name].write('\t' + item_json)
        self.first_item[city_name] = False

        return item

    def close_spider(self, spider):
        # 关闭每个城市的文件，并确保格式正确（写入']'结束）
        for city_name, file in self.files.items():
            file.write('\n]')  # 写入文件结尾符号
            file.close()
    

# 爬取北上广深数据的管道
class LianjiaPipeline:
    def __init__(self):
        self.files = {}  # 存储打开的文件句柄
        self.first_item = {}  # 用于标记每个城市是否已经写入过第一个 item

    def open_spider(self, spider):
        # 创建目录以保存 JSON 文件
        if not os.path.exists("original_data"):
            os.makedirs("original_data")

    def process_item(self, item, spider):
        city_name = item['city']
        
        if city_name not in self.files:
            # 为每个城市创建文件，写入一个开头的 '['，开始写入 JSON 数组
            file_path = f"original_data/{city_name}.json"
            self.files[city_name] = open(file_path, 'w+', encoding='utf-8')
            self.files[city_name].write('[\n')
            self.first_item[city_name] = True  # 标记这个城市是第一项

        # 写入单个 item 数据
        item_json = json.dumps(dict(item), ensure_ascii=False)
        
        # 如果不是第一项，添加逗号
        if not self.first_item[city_name]:
            self.files[city_name].write(',\n')
        
        # 写入数据并标记已经写过第一项
        self.files[city_name].write('\t' + item_json)
        self.first_item[city_name] = False

        return item

    def close_spider(self, spider):
        # 关闭每个城市的文件，并确保格式正确（写入']'结束）
        for city_name, file in self.files.items():
            file.write('\n]')  # 写入文件结尾符号
            file.close()
