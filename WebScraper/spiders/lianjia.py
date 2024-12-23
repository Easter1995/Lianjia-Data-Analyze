import scrapy
import re

import scrapy.resolver
from WebScraper.items import RentHouseItem
from scrapy_selenium import SeleniumRequest
import time
import json

class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    allowed_domains = ["lianjia.com"]
    city_names = ['bj', 'sh', 'sz', 'gz', 'dali']
    
    cookies = {
        "lianjia_uuid": "33bb9625-0e1b-40ac-8a0f-884b7c574e94",
        "Hm_lvt_46bf127ac9b856df503ec2dbf942b67e": "1732357750,1732608637,1732627932,1734012811",
        "_jzqa": "1.3216189913405561000.1732110614.1732627931.1734013518.4",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%2219349d67f0566b-03ccf1f445401c-e525627-1327104-19349d67f06d42%22%2C%22%24device_id%22%3A%2219349d67f0566b-03ccf1f445401c-e525627-1327104-19349d67f06d42%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D",
        "ftkrc_": "6d97c3ac-6236-4934-9c6e-3a8789d47a13",
        "lfrc_": "ddf035a8-9a2e-4cfd-8a63-c6b8dd091865",
        "_ga": "GA1.2.1928467867.1732110659",
        "_ga_QJN1VP0CMS": "GS1.2.1734013530.3.0.1734013530.0.0.0",
        "_ga_RCTBRFLNVS": "GS1.2.1732357751.2.0.1732357751.0.0.0",
        "_ga_KJTRWRHDL1": "GS1.2.1734013530.4.0.1734013530.0.0.0",
        "login_ucid": "2000000455074951",
        "lianjia_token": "2.0012803a70453ab31b032d134151f3baf8",
        "lianjia_token_secure": "2.0012803a70453ab31b032d134151f3baf8",
        "security_ticket": "EUtjTccMx5nei42GfXNMtiAZuyZg66PYjxCd99yBl203g6oQB6ZLtVDRO+mOTmVhn17L9on4JzzWuDlZ0KwPBlIJv0TIW0zs3frUCoIxO/AEoCJu99OLlFAJ305bLnFBuhedNr9Yym8VkspxLWqm2vTe/qbDAu8qyQD9kylBxHo=",
        "select_city": "110000",
        "beikeBaseData": "%7B%22parentSceneId%22%3A%222021652502261744129%22%7D",
        "lianjia_ssid": "dbfc4eb1-cc69-4759-827a-a02d98eea938",
        "hip": "1VzdKhw6CmsWTeLG6KzwTT93Oq5zbaXCYiyxxWNyQ4c7Ghyu3_NCDCGSGNiKEuAZlcue9dE7gzJRCU7SUVBNa2v_-12IH1cfud4Utzl5-3ExLhPZqbAOPOlDH5mtSW6L_zhDmAnGQJyikrqc4rD1NLVNZ_RAj2VlEjPAGIk_kmsXT33J25Uc2OUmfA%3D%3D"
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'WebScraper.pipelines.LianjiaPipeline': 543
        }
    }

    def start_requests(self):    
        # 读取 JSON 文件
        for name in self.city_names: # 实现五个城市的数据一起抓取
            with open(f'url_data/{name}.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 遍历 JSON 文件中的数据
            for entry in data:
                total = int(entry['total'])
                pages = int(entry['pages'])
                base_url = entry['url']
                
                # 如果 total 为 0，跳过这个 entry
                if total == 0:
                    continue
                
                # 构造分页 URL，从 pg1 到 pg{pages}
                for page in range(1, pages + 1):
                    url = base_url.replace('pg1', f'pg{page}')
                    yield scrapy.Request(url, callback=self.parse, meta={'city': entry['city'], 'district': entry['district'], 'area': entry['area']})

    def parse(self, response):
        captcha_button = response.xpath('//*[@id="captcha"]/div')
        if captcha_button:
            self.logger.info("Captcha detected. Pausing execution...")
            time.sleep(30)  # 暂停30秒，你可以根据需要调整
            return

        page_empty = bool(response.xpath('//div[@class="content__empty1"]'))  # 超出页数范围,会有这个标签
        city_name = response.meta['city']  # 从 URL 中提取城市名称
        
        if not page_empty:
            content_list = response.xpath('//*[@id="content"]/div[1]/div[1]/div')
            for content in content_list:
                # 去除广告
                ad = content.xpath('.//p[@class="content__list--item--ad"]/text()').get()
                if ad:
                    continue
                
                # 跳过一些不规范的数据
                room_left = content.xpath('.//p[@class="content__list--item--des"]//span[@class="room__left"]')
                if room_left:
                    continue

                house = RentHouseItem()
                house['city'] = city_name
                house['name'] = content.xpath('./div/p[1]/a/text()').get().strip()
                house['district'] = content.xpath('./div/p[2]/a[1]/text()').get() or None
                house['street'] = content.xpath('./div/p[2]/a[2]/text()').get() or None
                house['community'] = content.xpath('./div/p[2]/a[3]/text()').get() or None
                price = content.xpath('./div/span/em/text()').get()
                # 如果是价格区间，则取其平均数
                if '-' in price:
                    start, end = map(int, price.split('-'))
                    price = str((start + end) / 2)
                if '.' in price:
                    house['price'] = int(float(price))  # 转换为浮动数后再转为整数
                else:
                    house['price'] = int(price)  # 直接转换为整数
                des = content.xpath('.//p[@class="content__list--item--des"]').get().strip()
                try:
                    sq = re.search(r'([\d.]+)㎡', des).group(1)
                    house['square'] = float(sq)
                    house['price_per_m2'] = round(float(price) / float(sq), 2)
                except AttributeError:
                    house['square'] = None
                    house['price_per_m2'] = None

                try:
                    dir = re.search(r'<i>/</i>(.*)<i>/</i>', des).group(1)
                    house['direction'] = dir.strip()
                except AttributeError:
                    house['direction'] = None 

                try:
                    lay = re.search(r'<i>/</i>\n(.*)<span class="hide">', des).group(1)
                    house['layout'] = lay.strip()
                except AttributeError:
                    house['layout'] = None
                yield house
