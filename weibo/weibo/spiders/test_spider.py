import scrapy

from scrapy.http import Request
from bs4 import BeautifulSoup

class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com/"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        print soup.prettify()
