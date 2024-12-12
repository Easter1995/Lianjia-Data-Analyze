import json
import codecs

class NewHousePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        # 检查爬虫名称是否匹配
        if spider.name == 'new':
            self.file = codecs.open('original_data/NewHouse.json', 'w+', encoding='UTF-8')
            self.file.write('[\n')

    def process_item(self, item, spider):
        if spider.name == 'new':
            item_json = json.dumps(dict(item), ensure_ascii=False)
            # 检查文件是否有内容
            if self.file.tell() > 2:
                self.file.write(',\n')
            self.file.write('\t' + item_json)
        return item

    def close_spider(self, spider):
        if spider.name == 'new' and self.file:
            self.file.write('\n]')
            self.file.close()

class SecondHandHousePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'second':
            self.file = codecs.open('original_data/SecondHandHouse.json', 'w+', encoding='UTF-8')
            self.file.write('[\n')

    def process_item(self, item, spider):
        if spider.name == 'second':
            item_json = json.dumps(dict(item), ensure_ascii=False)
            # 检查文件是否有内容
            if self.file.tell() > 2:
                self.file.write(',\n')
            self.file.write('\t' + item_json)
        return item

    def close_spider(self, spider):
        if spider.name == 'second' and self.file:
            self.file.write('\n]')
            self.file.close()

class BeijingRentHousePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'beijing':
            self.file = codecs.open('original_data/Beijing.json', 'w+', encoding='UTF-8')
            self.file.write('[\n')

    def process_item(self, item, spider):
        if spider.name == 'beijing':
            item_json = json.dumps(dict(item), ensure_ascii=False)
            # 检查文件是否有内容
            if self.file.tell() > 2:
                self.file.write(',\n')
            self.file.write('\t' + item_json)
        return item

    def close_spider(self, spider):
        if spider.name == 'beijing' and self.file:
            self.file.write('\n]')
            self.file.close()

class ShanghaiRentHousePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'shanghai':
            self.file = codecs.open('original_data/Shanghai.json', 'w+', encoding='UTF-8')
            self.file.write('[\n')

    def process_item(self, item, spider):
        if spider.name == 'shanghai':
            item_json = json.dumps(dict(item), ensure_ascii=False)
            # 检查文件是否有内容
            if self.file.tell() > 2:
                self.file.write(',\n')
            self.file.write('\t' + item_json)
        return item

    def close_spider(self, spider):
        if spider.name == 'shanghai' and self.file:
            self.file.write('\n]')
            self.file.close()

class GuangzhouRentHousePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'guangzhou':
            self.file = codecs.open('original_data/Guangzhou.json', 'w+', encoding='UTF-8')
            self.file.write('[\n')

    def process_item(self, item, spider):
        if spider.name == 'guangzhou':
            item_json = json.dumps(dict(item), ensure_ascii=False)
            # 检查文件是否有内容
            if self.file.tell() > 2:
                self.file.write(',\n')
            self.file.write('\t' + item_json)
        return item

    def close_spider(self, spider):
        if spider.name == 'guangzhou' and self.file:
            self.file.write('\n]')
            self.file.close()

class ShenzhenRentHousePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'shenzhen':
            self.file = codecs.open('original_data/Shenzhen.json', 'w+', encoding='UTF-8')
            self.file.write('[\n')

    def process_item(self, item, spider):
        if spider.name == 'shenzhen':
            item_json = json.dumps(dict(item), ensure_ascii=False)
            # 检查文件是否有内容
            if self.file.tell() > 2:
                self.file.write(',\n')
            self.file.write('\t' + item_json)
        return item

    def close_spider(self, spider):
        if spider.name == 'shenzhen' and self.file:
            self.file.write('\n]')
            self.file.close()

class DaliRentHousePipeline:
    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        if spider.name == 'dali':
            self.file = codecs.open('original_data/Dali.json', 'w+', encoding='UTF-8')
            self.file.write('[\n')

    def process_item(self, item, spider):
        if spider.name == 'dali':
            item_json = json.dumps(dict(item), ensure_ascii=False)
            # 检查文件是否有内容
            if self.file.tell() > 2:
                self.file.write(',\n')
            self.file.write('\t' + item_json)
        return item

    def close_spider(self, spider):
        if spider.name == 'dali' and self.file:
            self.file.write('\n]')
            self.file.close()