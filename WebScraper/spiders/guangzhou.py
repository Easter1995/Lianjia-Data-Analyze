import scrapy


class GuangzhouSpider(scrapy.Spider):
    name = "guangzhou"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://gz.lianjia.com/zufang/"]

    def parse(self, response):
        pass
