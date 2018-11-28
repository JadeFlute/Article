# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from Artical.tools.get_proxy import Get_Random_Ip


class ArticalSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ArticalDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


#随机切换user-agent
class RandomUserAgentMiddleWare(object):
    def __init__(self,crawler):
        super(RandomUserAgentMiddleWare,self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        def get_ua():
            #实现ua.ua_type
            return getattr(self.ua,self.ua_type)
        b = get_ua()
        request.headers.setdefault('User-Agent',get_ua())


#随机选择ip
class RandomProxyMiddleWare(object):
    def process_request(self, request, spider):
        gp = Get_Random_Ip()
        request.meta['proxy'] = gp.get_ip()
# {'http':'ip:端口'}

# class RandomProxyMiddleWare(object):
#     def process_request(self, request, spider):
#         request.meta['proxy']

#在scrapy中使用selenium
#下面注释掉的代码可以放在spider（bole）中

# from selenium import webdriver
from scrapy.http import HtmlResponse
class JSPageMiddleware(object):
    # def __init__(self):
    #     super(JSPageMiddleware,self).__init__()
    #     self.browser = webdriver.Chrome(executable_path="E:/chromedriver/chromedriver.exe")
    #     # 设置一个信号：当爬虫关闭时，浏览器退出。
    #     dispatcher.connect(self.spider_closed,signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    def process_request(self, request, spider):
        if spider.name == "bole":
            # browser = webdriver.Chrome(executable_path="E:/chromedriver/chromedriver.exe")
            spider.browser.get(request.url)
            import time
            time.sleep(3)
            print ("访问:{0}".format(request.url))
            # scrapy在路过中间件时，如果发现url给了HtmlResponse，
            # 就不会把url交给downloader，而是直接返回给spider
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)








