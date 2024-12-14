import scrapy
from WebScraper.items import RentHouseItem
from scrapy_selenium import SeleniumRequest

class DaliSpider(scrapy.Spider):
    name = "dali"
    allowed_domains = ["dali.lianjia.com"]
    base_url = 'https://dali.lianjia.com/zufang/'
    range_ = 100

    def start_requests(self):
        # 动态生成 URLs
        urls = [f"{self.base_url}pg{i}" for i in range(1, self.range_ + 1)]
        urls.append(self.base_url)
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        content_list = response.xpath('//*[@id="content"]/div[1]/div[1]/div')
        for item in content_list:
            house = RentHouseItem()
            name = item.xpath('./div/p[1]/a/text()').get().split()
            house['name'] = name[0]
            district = ""
            for i in range(1, 4):
                district += item.xpath(f'./div/p[2]/a[{i}]')
            house['district'] = district
            
