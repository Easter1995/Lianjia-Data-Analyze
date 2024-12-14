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
    direction = scrapy.Field() # 朝向
    layout = scrapy.Field() # 房型