import scrapy
from WebScraper.items import RentHouseURLs
from scrapy_selenium import SeleniumRequest

class UrlSpiderSpider(scrapy.Spider):
    name = "url_spider"
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
        "_ga_QJN1VP0CMS": "GS1.2.1734013530.3.0.1734013530.0.0.0"
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'WebScraper.pipelines.URLPipeline': 543
        }
    }

    def parse_url(self, response):
        city_name = response.meta['city_name']
        dis_name = response.meta['district_name']
        area_name = response.meta['area_name']
        area_url = response.meta['url']
        total_page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').get(default='0')
        total_num = response.xpath('//*[@id="content"]/div[1]/p/span[1]/text()').get(default='0')
        url = RentHouseURLs()
        url['city'] = city_name
        url['district'] = dis_name
        url['area'] = area_name
        url['url'] = area_url
        url['total'] = total_num
        url['pages'] = total_page
        yield url

    def get_area(self, response):
        area_href_list = response.xpath('//*[@id="filter"]/ul[4]/li/a')
        city_name = response.meta['city_name']
        dis_name = response.meta['district_name']

        for area in area_href_list[1:]:
            area_str = area.xpath('./@href').get().strip().split('/')[2]
            area_url = f"https://{city_name}.lianjia.com/zufang/{area_str}/pg1"
            area_name = area.xpath('./text()').get()
            yield SeleniumRequest(url=area_url, cookies=self.cookies, callback=self.parse_url, meta={
                'city_name': city_name,
                'district_name': dis_name,
                'area_name': area_name,
                'url': area_url,
            })

    def get_district(self, response):
        city_name = response.meta['city_name']
        district_list = response.xpath('//*[@id="filter"]/ul[2]/li')
        for dis in district_list[1:]:
            dis_str = dis.xpath('./a/@href').get().strip().split('/')[2]
            dis_name = dis.xpath('./a/text()').get()
            # 每个区的起始url
            district_url = f"https://{city_name}.lianjia.com/zufang/{dis_str}/"
            yield SeleniumRequest(url=district_url, cookies=self.cookies, callback=self.get_area, meta={
                'city_name': city_name,
                'district_name': dis_name
            })

    def start_requests(self):    
        for name in self.city_names:
            # 每个城市的起始url
            yield SeleniumRequest(url=f"https://{name}.lianjia.com/zufang/", cookies=self.cookies, callback=self.get_district, meta={'city_name': name})
