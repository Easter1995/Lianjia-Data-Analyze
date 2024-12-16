import scrapy
from WebScraper.items import RentHouseURLs

class UrlSpiderSpider(scrapy.Spider):
    name = "url_spider"
    allowed_domains = ["lianjia.com"]
    city_names = ['bj']
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
            yield scrapy.Request(url=area_url, cookies=self.cookies, callback=self.parse_url, meta={
                'city_name': city_name,
                'district_name': dis_name,
                'area_name': area_str,
                'url': area_url,
            })

    def get_district(self, response):
        city_name = response.meta['city_name']
        district_list = response.xpath('//*[@id="filter"]/ul[2]/li')
        for dis in district_list[1:]:
            dis_str = dis.xpath('./a/@href').get().strip().split('/')[2]
            # 每个区的起始url
            district_url = f"https://{city_name}.lianjia.com/zufang/{dis_str}/"
            yield scrapy.Request(url=district_url, cookies=self.cookies, callback=self.get_area, meta={
                'city_name': city_name,
                'district_name': dis_str
            })

    def start_requests(self):    
        # for name in self.city_names:
            # 每个城市的起始url
        yield scrapy.Request(url=f"https://sz.lianjia.com/zufang/yantianqu/", cookies=self.cookies, callback=self.get_area, meta={'city_name': 'sz', 'district_name': 'yantianqu'})