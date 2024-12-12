import scrapy


class BeijingSpider(scrapy.Spider):
    name = "beijing"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://bj.lianjia.com"]

    def parse(self, response):
        pass
