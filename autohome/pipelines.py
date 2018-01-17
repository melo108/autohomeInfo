# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutohomePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipeline(object):

    def __init__(self,mongo_db,mongo_url,mongo_port,mongo_table):
        self.mongo_db=mongo_db
        self.mongo_url=mongo_url
        self.mongo_port=mongo_port
        self.mongo_table=mongo_table

    @classmethod
    def from_crawler(cls,crawler):
        mongo_db = crawler.settings.get("MONGO_DB")
        mongo_url = crawler.settings.get("MONGO_URL")
        mongo_port = crawler.settings.get("MONGO_PORT")
        mongo_table = crawler.settings.get("MONGO_TABLE")
        return cls(mongo_db,mongo_url,mongo_port,mongo_table)

    def open_spider(self,spider):
        from pymongo import MongoClient
        self.client = MongoClient(self.mongo_url,self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.table = self.db[self.mongo_table]

    def process_item(self,item,spider):
        self.table.insert(dict(item))
        print(item["title"],'-------','已经写入mongo')
        return item

    def close_spider(self,spider):
        self.client.close()
