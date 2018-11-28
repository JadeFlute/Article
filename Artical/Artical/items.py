# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from datetime import datetime
import re


def add_time_handle(value):
    add_time_pre = ''
    for t in value:
        add_time_pre += t
    add_time = add_time_pre.replace("·","").strip()
    try:
        add_time = datetime.strptime(add_time, '%Y/%m/%d').date()
    except Exception as e:
        add_time = datetime.now().date()
    return add_time


def content_handle(value):
    content_all = ''
    for cont in value:
        content_all += cont.strip()
    return content_all


def num_handle(value):
    res = re.match(r'.*(\d+).*', value)
    if res:
        return int(res.group(1))
    else:
        return 0


def return_value(value):
    return value


#使用input_processor=MapCompose()来处理匹配的值，提高函数的重用率，方便修改；
class BoleArticalItem(scrapy.Item):
    artical_url = scrapy.Field()
    artical_url_md5 = scrapy.Field()

    title = scrapy.Field()
    add_time = scrapy.Field(
        # 对字段的值进行处理；可以写多个处理函数
        input_processor=MapCompose(add_time_handle)
    )
    tag = scrapy.Field(
        output_processor=Join('-')
    )
    content = scrapy.Field(
        input_processor=MapCompose(content_handle),
        output_processor = MapCompose(return_value)
    )
    praise = scrapy.Field(
        input_processor=MapCompose(num_handle)
    )
    collect = scrapy.Field(
        input_processor=MapCompose(num_handle)
    )

    front_img_url = scrapy.Field(
        # 写一个函数，返回本身值；然后调用来
        # 覆盖default_output_processor = TakeFirst()的作用
        output_processor=MapCompose(return_value)
    )
    front_img_path = scrapy.Field()


class BoleArticalItemLoader(ItemLoader):
    # 因为使用itemloader获取的值都是列表，
    # 所以重写类来取第一个：处理函数有输入和输出，这是改写默认输出
    default_output_processor = TakeFirst()










































