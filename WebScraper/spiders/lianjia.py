import scrapy
import re
from WebScraper.items import RentHouseItem
from scrapy_selenium import SeleniumRequest

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    range_ = 100 # 爬取100页
    # city_names = ['dali']
    city_names = ['bj', 'sh', 'gz', 'sz', 'dali']

    def get_urls(self):
        urls = []
        for name in self.city_names:
            urls.append(f"https://{name}.lianjia.com/zufang")
            urls_tmp = [f"https://{name}.lianjia.com/zufang/pg{i}" for i in range(2, self.range_ + 1)]
            urls.extend(urls_tmp)
        return urls
    
    def start_requests(self):
        urls = self.get_urls()
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse, meta={'city_name': url.split('.')[0][8:]})

    def parse(self, response):
        page_empty = bool(response.xpath('//div[@class="content__empty1"]'))  # 超出页数范围,会有这个标签
        city_name = response.meta['city_name']  # 从 URL 中提取城市名称
        if not page_empty:
            content_list = response.xpath('//*[@id="content"]/div[1]/div[1]/div')
            for content in content_list:
                # 去除广告
                ad = content.xpath('.//p[@class="content__list--item--ad"]/text()').get()
                if ad:
                    continue
                house = RentHouseItem()
                house['city'] = city_name
                house['name'] = content.xpath('./div/p[1]/a/text()').get().strip()
                house['district'] = content.xpath('./div/p[2]/a[1]/text()').get()
                house['street'] = content.xpath('./div/p[2]/a[2]/text()').get()
                house['community'] = content.xpath('./div/p[2]/a[3]/text()').get()
                price = content.xpath('./div/span/em/text()').get()
                # 如果是价格区间，则取其平均数
                if '-' in price:
                    start, end = map(int, price.split('-'))
                    price = str((start + end) / 2)
                house['price'] = int(price)
                des = content.xpath('.//p[@class="content__list--item--des"]').get().strip()
                sq = re.search(r'([\d.]+)㎡', des).group(1)
                house['square'] = float(sq)
                dir = re.search(r'<i>/</i>(.*)<i>/</i>', des).group(1)
                house['direction'] = dir.strip()
                lay = re.search(r'<i>/</i>\n(.*)<span class="hide">', des).group(1)
                house['layout'] = lay.strip()
                yield house
