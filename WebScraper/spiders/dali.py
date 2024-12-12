import scrapy


class DaliSpider(scrapy.Spider):
    name = "dali"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://dali.lianjia.com/zufang/"]

    def parse(self, response):
        pass
