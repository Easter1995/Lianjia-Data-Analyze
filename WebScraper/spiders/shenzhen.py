import scrapy


class ShenzhenSpider(scrapy.Spider):
    name = "shenzhen"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://sz.lianjia.com/zufang/"]

    def parse(self, response):
        pass
