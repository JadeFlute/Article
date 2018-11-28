# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


#保存文章，方法1
class ArticalPipeline(object):
    def __init__(self):
        self.file = codecs.open('artical.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item),ensure_ascii=False) + '\n')
        return item
    def spider_closed(self,spider):
        self.file.close()

#保存文章，方法2
class ArticalJsonPipeline(object):
    #使用scrapy自带的函数保存json文件
    def __init__(self):
        self.file = open('articaljson.json','wb')   # wb
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

#保存图片
class ImgPipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'front_img_path' in item:
            for ok,value in results:
                front_img_path = value['path']
                item['front_img_path'] = front_img_path
        return item


#将数据存储进数据库：同步
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','0','artical_spider',charset = 'utf8',use_unicode=True)
        self.cur = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = '''
            insert into artical(artical_url_md5,title,tag) VALUES(%s,%s,%s)
        '''
        try:
            self.cur.execute(insert_sql,(item['artical_url_md5'],item['title'],item['tag']))
            self.conn.commit()
        except:
            pass


#将数据存储进数据库：异步
class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        #获取设置值；字典中的键名是固定的
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        #处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)



