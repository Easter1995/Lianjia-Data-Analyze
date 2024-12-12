import scrapy
from WebScraper.items import NewHouse
from scrapy_selenium import SeleniumRequest

class NewSpider(scrapy.Spider):
    name = "new"
    allowed_domains = ["bj.fang.lianjia.com"]
    base_url = 'https://bj.fang.lianjia.com/loupan/'
    base_page = 3
    range_ = 5

    def start_requests(self):
        # 动态生成 URLs
        urls = [f"{self.base_url}pg{self.base_page + i}" for i in range(self.range_)]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        li_list = response.xpath('/html/body/div[3]/ul[2]/li')
        for item in li_list:
            house = NewHouse()
            house['name'] = item.xpath('./div/div[1]/h2/a/text()').get()
            region1 = item.xpath('./div/div[2]/span[1]/text()').get()
            region2 = item.xpath('./div/div[2]/span[2]/text()').get()
            region3 = item.xpath('./div/div[2]/a/text()').get()
            location = f"{region1} / {region2} / {region3}"
            house['location'] = location
            house['type'] = item.xpath('./div/div[1]/span[1]/text()').get()
            houseTypes = item.xpath('./div/a/span')
            houseType = ''
            for type in houseTypes:
                text = type.xpath('./text()').get()  # 用 get() 提取单个值
                if text:
                    houseType += text + '/'
            house['houseType'] = houseType.rstrip('/')
            house['square'] = item.xpath('./div/div[3]/span/text()').get()
            house['unitPrice'] = item.xpath('./div/div[6]/div[1]/span[1]/text()').get() + ' 元/㎡(均价)'
            house['totalPrice'] = item.xpath('./div/div[6]/div[2]/text()').get()
            yield house