import scrapy
import random
import time
from WebScraper.items import RentHouseItem
from scrapy_selenium import SeleniumRequest

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["bj.lianjia.com"]
    range_ = 100 # 爬取100页
    city_names = ['dali']
    # city_names = ['bj', 'sh', 'gz', 'sz', 'dali']

    def get_urls(self):
        urls = []
        for name in self.city_names:
            urls.append(f"https://{name}.lianjia.com/zufang")
            urls_tmp = [f"https://{name}.lianjia.com/zufang/pg{i}" for i in range(2, self.range_ + 1)]
            urls.extend(urls_tmp)
        urls
    
    def start_requests(self):
        urls = self.get_urls()
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        page_empty = bool(response.xpath('//div[@class="content__empty1"]'))  # 超出页数范围,会有这个标签
        if not page_empty:
            content_list = response.xpath('//*[@id="content"]/div[1]/div[1]/div')
            for content in content_list:
                # 去除广告
                ad = content.xpath('.//p[@class="content__list--item--ad"]/text()').get()
                if ad:
                    continue
                house = RentHouseItem()
                house['name'] = content.xpath('./div/p[1]/a/text()').get()
                house['district'] = content.xpath('./div/p[2]/a[1]/text()').get()
                house['street'] = content.xpath('./div/p[2]/a[2]/text()').get()
                house['community'] = content.xpath('./div/p[2]/a[3]/text()').get()
                price = content.xpath('./div/span/em/text()').get()
                # 如果是价格区间，则取其平均数
                if '-' in price:
                    start, end = map(int, price.split('-'))
                    average = (start + end) / 2
                    price = str(average)
                house['price'] = price
                house['square'] = content.xpath('./div/p[2]/text()[3]/text()').get()
                house['direction'] = content.xpath('./div/p[2]/text()[4]/text()').get()
                house['layout'] = content.xpath('./div/p[2]/text()[5]/text()').get()
                yield house

            # 随机休眠1-2秒
            delay = random.uniform(1, 2)
            time.sleep(delay)