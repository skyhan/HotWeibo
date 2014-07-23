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
        for sel in response.xpath('//div[@class="WB_detail"]'):
            # title = sel.xpath('a/text()').extract()
            # link = sel.xpath('a/@href').extract()
            desc = sel.xpath('/div[@class="WB_text"]/text()').extract()
            print desc
            # print title, link, desc

        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)