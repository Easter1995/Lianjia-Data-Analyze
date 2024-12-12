import scrapy


class ShanghaiSpider(scrapy.Spider):
    name = "shanghai"
    allowed_domains = ["bj.lianjia.com"]
    start_urls = ["https://sh.lianjia.com/zufang/"]

    def parse(self, response):
        pass
