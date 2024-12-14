import scrapy
import re
from WebScraper.items import RentHouseItem
from scrapy_selenium import SeleniumRequest

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    range_ = 1 # 爬取100页
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
        cookies = {
            "lianjia_uuid": "62838a59-dcb3-4aaf-8822-a30552ec67fc",
            "select_city": "110000",
            "_jzqckmp": "1",
            "sajssdk_2015_cross_new_user": "1",
            "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%2219366856e6c2585-030802f29c35ab-4c657b58-1474560-19366856e6d20be%22%2C%22%24device_id%22%3A%2219366856e6c2585-030802f29c35ab-4c657b58-1474560-19366856e6d20be%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.bing.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.bing.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D",
            "_ga": "GA1.2.1930313920.1732591852",
            "_gid": "GA1.2.1649179390.1732591852",
            "lianjia_ssid": "c0eb2e71-fd3d-ab83-2826-4b66f276220c",
            "Hm_lvt_46bf127ac9b856df503ec2dbf942b67e": "1732591841,1732607542,1732619326",
            "HMACCOUNT": "C7C4DF0C8FC7B7A3",
            "_jzqc": "1",
            "_jzqa": "1.3002874785734019600.1732591841.1732620120.1732624451.3",
            "_jzqx": "1.1732591841.1732624451.3.jzqsr=bing%2Ecom|jzqct=/.jzqsr=bj%2Elianjia%2Ecom|jzqct=/ershoufang/pg3/",
            "crosSdkDT2019DeviceId": "r558a3-8pbec2-ngcrn2iaghcqw9b-q85wx1qk2",
            "Hm_lvt_efa595b768cc9dc7d7f9823368e795f1": "1732627962",
            "Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1": "1732628235",
            "ftkrc_": "292c3b05-c798-4f41-b4f1-731a083f6fcc",
            "lfrc_": "0491943e-7806-4059-b894-2e7fc3319139",
            "_ga_RCTBRFLNVS": "GS1.2.1732628402.5.1.1732628481.0.0.0",
            "_ga_QJN1VP0CMS": "GS1.2.1732624465.3.1.1732629209.0.0.0",
            "_ga_KJTRWRHDL1": "GS1.2.1732624465.3.1.1732629209.0.0.0",
            "login_ucid": "2000000456377707",
            "lianjia_token": "2.00155c1cb7428ab43004f13586c1b7b015",
            "lianjia_token_secure": "2.00155c1cb7428ab43004f13586c1b7b015",
            "security_ticket": "PPF22BIWqADLdc1B1Gd+g6FkhsBGuvWYcXoWe/8gSYn6MWK2Hq8nZH4VqA9y6PNjT62rr8/IIOqUazJK2PvzzvF9cQN5isXCm11k5r8yNqrLu43HosjrXucyih6savjOjdQO9mR6Vg1cO64lAuW8xz2D3fkPNUgxyFrZXwpT+BI=",
            "Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e": "1732630462",
            "_jzqb": "1.17.10.1732624451.1"
        }
        urls = self.get_urls()
        for url in urls:
            yield SeleniumRequest(url=url, cookies=cookies, callback=self.parse, meta={'city_name': url.split('.')[0][8:]})

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
