**项目结构：**

```
├── WebScraper
│   ├── __init__.py
│   ├── items.py 
│   ├── middlewares.py 
│   ├── pipelines.py
│   ├── settings.py 
│   └── spiders
│       ├── __init__.py
│       ├── new.py
│       └── second.py
├── scrapy.cfg
├── main.cfg
└── original_data
	├── NewHouse.json
	└── SecondHandHouse.json
```

**项目说明:**

- **settings.py**

  开启管道，定义selenium使用的浏览器driver及其位置。

- **middlewares.py**

  定义了`SeleniumMiddleware`类，用于在爬虫中通过 Selenium 控制浏览器进行页面抓取，在这里使用的Firefox的driver。

- **pipelines.py**

  定义了`NewHousePipeline`和`SecondHandHousePipeline`类，两个管道分别用于处理抓取的新房和二手房的数据。

- **main.py**

  用于同时启动两个爬虫，使用了`CrawlerProcess`。

- **items.py**

  定义了`NewHouse`和`SecondHandHouse`类，类里面定义了作业要求的信息。

- **new.py和second.py**

  定义了`NewSpider`类和`SecondSpider`，包括动态生成urls和用xpath来抓取特定数据的逻辑，以及二手房的部分定义了cookie。

- **NewHouse.json和SecondHandHouse.json**

  存储从新房页面爬取的数据；存储从二手房页面爬取的数据。

- 反爬：selenium作为中间件+添加请求Header+添加cookie