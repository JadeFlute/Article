# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy import Request
import re
from Artical.items import BoleArticalItem,BoleArticalItemLoader
from Artical.utils.common import get_md5
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from datetime import datetime
from scrapy.loader import ItemLoader


class BoleSpider(scrapy.Spider):
    name = 'bole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    #收集404的url以及数量
    handle_httpstatus_list = [404]
    def __init__(self):
        self.fail_urls = []
        #设置一个信号：当爬虫关闭时，执行handle_spider_closed函数（打印错误url）；
        #ps：scrapy本身有一个信号是：当爬虫关闭时打印出爬虫状态。
        dispatcher.connect(self.handle_spider_closed,signals.spider_closed)

    def handle_spider_closed(self,spider,reason):
        #使用scrapy的状态收集器，收集失败的url；由于收集器不能存列表，使用join转换成字符串
        self.crawler.stats.set_value('failed_urls',','.join(self.fail_urls))

    def parse(self, response):

        if response.status == 404:
            self.fail_urls.append(response.url)
            #使用以下代码，scrapy会自动计算失败的url数量
            self.crawler.status.inc_value('failed_url')

        artical_a_list = response.xpath('//div[@id="archive"]//div[@class="post-thumb"]/a')
        for artical_a in artical_a_list:
            artical_url = artical_a.xpath('./@href').extract_first('')
            front_img_url = artical_a.xpath('./img/@src').extract_first('')
            yield Request(parse.urljoin(response.url,artical_url),meta={'front_img_url':front_img_url},callback=self.parse_detail)

        #获取下一页url
        next_page_url = response.xpath('//a[@class="next page-numbers"]/@href').extract()[0]
        yield Request(parse.urljoin(response.url,next_page_url), callback=self.parse)


    def parse_detail(self,response):
        # artical_item = BoleArticalItem()
        #
        # #前景图url
        # artical_item['front_img_url'] = [response.meta.get('front_img_url','')]
        #
        # #w文章url
        # artical_item['artical_url'] = response.url
        # #文章url，加密保存（节省空间）
        # artical_item['artical_url_md5'] = get_md5(response.url)
        #
        # #标题
        # artical_item['title'] = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        #
        # #发布时间
        # add_time = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].replace("·","").strip()
        # try:
        #     add_time = datetime.strptime(add_time,'%Y/%m/%d').date()
        # except Exception as e:
        #     add_time = datetime.now().date()
        # artical_item['add_time'] = add_time
        #
        # #标签
        # tag_list = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # artical_item['tag'] = '-'.join(tag_list)
        #
        # #正文
        # #方法1
        # content_data = response.xpath('//div[@class="entry"]/p | //div[@class="entry"]/h2')
        # content_all = ''
        # for cont in content_data:
        #     content_all += cont.xpath('string(.)').extract()[0]
        # artical_item['content'] = content_all
        #
        # #方法2
        # # content_data = response.xpath('//div[@class="entry"]')[0]
        # # content_all = content_data.xpath('string(.)').extract()[0]
        #
        # #点赞
        # support_a = response.xpath('//div[@class="post-adds"]/h10/text()').extract()
        # if support_a:
        #     support = int(support_a[0])
        #     # artical_item['support'] = int(support_a[0])
        # else:
        #     support = 0
        #     # artical_item['support'] = 0
        #
        # #收藏
        # collect_a = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract()[0]
        # collect_re = re.match(r'\s(\d+).*',collect_a)
        # if collect_re:
        #     artical_item['collect'] = int(collect_re.group(1))
        # else:
        #     artical_item['collect'] = 0


        front_img_url = response.meta.get('front_img_url')
        item_loader = BoleArticalItemLoader(item=BoleArticalItem(),response=response)

        item_loader.add_value('artical_url',response.url)
        item_loader.add_value('artical_url_md5',get_md5(response.url))
        item_loader.add_xpath('title','//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath('add_time','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_xpath('tag','//p[@class="entry-meta-hide-on-mobile"]/a/text()')
        item_loader.add_xpath('content','//div[@class="entry"]/p/text() | //div[@class="entry"]/h2/text()')
        item_loader.add_xpath('praise','//div[@class="post-adds"]//h10/text()')
        item_loader.add_xpath('collect','//div[@class="post-adds"]/span[2]/text()')
        item_loader.add_value('front_img_url',[front_img_url])

        artical_item = item_loader.load_item()

        yield artical_item
