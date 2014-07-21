import scrapy

from scrapy.http import Request

from ..weibo_login import wblogin
from ..settings import weibo_username, weibo_password

class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.com"]
    start_urls = [
        "http://weibo.com/u/2641787312/"
    ]

    def start_requests(self):
        login_cookie = wblogin(weibo_username, weibo_password)
        for url in self.start_urls:
            yield Request(url, cookies=login_cookie)

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)