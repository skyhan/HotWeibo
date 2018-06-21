import scrapy

from scrapy.http import Request
from bs4 import BeautifulSoup

from ..weibo_login import wblogin
from ..user_settings import weibo_username, weibo_password

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
        formed_body = self.remove_back_slant(response.body)
        soup = BeautifulSoup(formed_body)
        print soup.find_all('div')
        print soup.find_all('div', class_='WB_info')
        print soup.prettify()

        # for sel in response.xpath('//div'):
        #     #print sel
        #     pass
        #
        # for sel in response.xpath('//div[@class="WB_detail"]'):
        #     # title = sel.xpath('a/text()').extract()
        #     # link = sel.xpath('a/@href').extract()
        #     print sel
        #     desc = sel.xpath('/div[@class="WB_text"]/text()').extract()
        #     print desc
        #     # print title, link, desc

        filename = response.url.split("/")[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)

    def remove_back_slant(self, str):
        return str.replace('\/', '/').replace('\\"', '"')