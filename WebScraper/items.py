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