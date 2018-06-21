#! -*- encoding:utf-8 -*-
import re
import time

from ..user_settings import weibo_username, weibo_password

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request

class WeiboSpider(CrawlSpider):
    # use scrapy to login weibo

    name = 'weibo'
    allowed_domains = ['weibo.com', 'sina.com.cn']

    def start_requests(self):
        username = weibo_username
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=miniblog&callback=sinaSSOController.preloginCallBack&user=%s&client=ssologin.js(v1.3.14)&_=%s'.format(
            username, str(time.time()).replace('.', ''))
        print url
        return [Request(url=url, method='get', callback=self.parse_item)]

    rules = (
        Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse', follow=True),
    )

    def parse_item(self, response):
        print response.body
        hxs = HtmlXPathSelector(response)
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        return i

    def post_message(self, response):
        serverdata = re.findall('{"retcode":0,"servertime":(.*?),"nonce":"(.*?)"}', response.body, re.I)[0]
        print serverdata
        servertime = serverdata[0]
        print servertime
        nonce = serverdata[1]
        print nonce
        formdata = {"entry" : 'miniblog',
                    "gateway" : '1',
                    "from" : "",
                    "savestate" : '7',
                    "useticket" : '1',
                    "ssosimplelogin" : '1',
                    "username" : '**********',
                    "service" : 'miniblog',
                    "servertime" : servertime,
                    "nonce" : nonce,
                    "pwencode" : 'wsse',
                    "password" : '*********',
                    "encoding" : 'utf-8',
                    "url" : 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                    "returntype" : 'META'}

        return [FormRequest(url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.14)',
                                formdata = formdata,callback=self.parse_item) ]