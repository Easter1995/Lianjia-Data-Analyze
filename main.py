from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# 同时启动两个爬虫
settings = get_project_settings()
crawler = CrawlerProcess(settings)
crawler.crawl('new')
crawler.crawl('second')

crawler.start()