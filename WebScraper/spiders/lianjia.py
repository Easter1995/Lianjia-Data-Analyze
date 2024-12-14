import scrapy
import re
from WebScraper.items import RentHouseItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By


class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    city_names = ['dali']
    # city_names = ['bj', 'sh', 'gz', 'sz', 'dali']
    cookies = {
        "lianjia_uuid": "f4e3d625-f9ef-4796-9fbf-1005748236ee",
        "Hm_lvt_46bf127ac9b856df503ec2dbf942b67e": "1731846490",
        "HMACCOUNT": "D904BD81485BDC57",
        "_jzqc": "1",
        "_ga": "GA1.2.511800293.1731846504",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221933a18487e10e5-05564b0cdb79cf-26011951-1327104-1933a18487f1196%22%2C%22%24device_id%22%3A%221933a18487e10e5-05564b0cdb79cf-26011951-1327104-1933a18487f1196%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D",
        "ftkrc_": "0248dd95-2625-40b5-8dbe-c03e4c9d833a",
        "lfrc_": "3af73b7d-5de7-4cd3-bdda-fd2781075775",
        "_ga_RCTBRFLNVS": "GS1.2.1732591395.14.1.1732591402.0.0.0",
        "_jzqx": "1.1731846496.1732618294.6.jzqsr=bj%2Elianjia%2Ecom|jzqct=/.jzqsr=bj%2Elianjia%2Ecom|jzqct=/ershoufang/",
        "_ga_KJTRWRHDL1": "GS1.2.1732618303.9.0.1732618303.0.0.0",
        "_ga_QJN1VP0CMS": "GS1.2.1732618303.9.0.1732618303.0.0.0",
        "Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e": "1732627892",
        "GUARANTEE_BANNER_SHOW": "true",
        "lianjia_ssid": "7ecace34-3b67-40bd-b76e-5f4f5812ec36",
        "select_city": "532900",
        "srcid": "eyJ0Ijoie1wiZGF0YVwiOlwiOTdlZjRkNzQ4OGY2ZWY2NWRmZWFmYTkyODQ0NWI2MjNiYTc4MDAxN2NkMDc2NzQyNmVlY2NjNDAzMThjZThmMGMyMjJmOTg5MGIzZDZlNmM3M2JjNzgzYjk5MWUxYWQxYWQxOTJmN2YzYzhiODBiODI2ZDI0YTllOTE2ZTAxNGY4NGUxMjRmNmFkMTllMWMxYWI3NDhhNTc1YjhiNDA0MzM4M2QwMjAxNDIzMzM0ODJlNDQ4NmI0MTRhMmY5NTJmZTM3ODYyMDI0ZTBjMzY5MjE1MmU0MzNmMjI4YTkzNmI3YmJjNjk3OTJlNzdmZmQwZmVlNzBkMDJhZTBjOGM4NFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJhZjFiYTkyMlwifSIsInIiOiJodHRwczovL2RhbGkubGlhbmppYS5jb20venVmYW5nLyIsIm9zIjoid2ViIiwidiI6IjAuMSJ9",
        "Hm_lpvt_46bf127ac9b856df503ec2dbf942b67e": "1732630462",
        "_jzqb": "1.17.10.1732624451.1"
    }

    def get_start_urls(self):
        urls = []
        for name in self.city_names:
            # 每个城市的起始url
            urls.append(f"https://{name}.lianjia.com/zufang/")
        return urls
    
    def get_district(self, response):
        city_name = response.meta['city_name']
        district_list = response.xpath('//*[@id="filter"]/ul[2]/li')
        for dis in district_list[1:]:
            dis_str = dis.xpath('./a/@href').get().strip().split('/')[2]
            # 每个区的起始url
            district_url = f"https://{city_name}.lianjia.com/zufang/{dis_str}/"
            yield SeleniumRequest(url=district_url, cookies=self.cookies, callback=self.get_area, meta={
                'city_name': city_name,
                'district_name': dis_str
            })

    def get_area(self, response):
        urls = []
        city_name = response.meta['city_name']
        area_href_list = response.xpath('//*[@id="filter"]/ul[4]/li/a')
        for area in area_href_list:
            area_str = area.xpath('./@href').get().strip().split('/')[2]
            area_url = f"https://{city_name}.lianjia.com/zufang/{area_str}/"
            urls.append(area_url)
            # 每个街道的起始url
            tmp_url = f"{area_url}pg1"
            urls.append(tmp_url)

        for url in urls[1:]:
            yield SeleniumRequest(url=url, cookies=self.cookies, callback=self.parse, meta={'city_name': city_name,})

    def start_requests(self):    
        for name in self.city_names:
            # 每个城市的起始url
            yield SeleniumRequest(url=f"https://{name}.lianjia.com/zufang/", cookies=self.cookies, callback=self.get_district, meta={'city_name': name})

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
