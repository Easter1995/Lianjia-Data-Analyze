# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouse(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    location = scrapy.Field()
    houseType = scrapy.Field()
    square = scrapy.Field()
    unitPrice = scrapy.Field()
    totalPrice = scrapy.Field()
class SecondHandHouse(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    houseType = scrapy.Field()
    unitPrice = scrapy.Field()
    totalPrice = scrapy.Field()

class RentHouseItem(scrapy.Item):
    city = scrapy.Field() # 城市名字
    name = scrapy.Field() # 楼盘名字
    district = scrapy.Field() # 行政区
    street = scrapy.Field() # 街道
    community = scrapy.Field() # 小区
    price = scrapy.Field() # 价格 元/月
    square = scrapy.Field() # 面积 平方米
    price_per_m2 = scrapy.Field() # 单位面积的价格 元
    direction = scrapy.Field() # 朝向
    layout = scrapy.Field() # 房型

class RentHouseURLs(scrapy.Item):
    city = scrapy.Field() # 城市
    district = scrapy.Field() # 行政区
    area = scrapy.Field() # 街道 
    url = scrapy.Field() # 第一页的url
    total = scrapy.Field() # 总数据量
    pages = scrapy.Field() # 总页数