# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import mysql.connector
from twisted.enterprise import adbapi


class MySqlAsyncPipeline(object):
    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_db')
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '12345678')
        self.dbpool = adbapi.ConnectionPool('mysql.connector', host=host, db=db, user=user, passwd=passwd, port=port, charset='utf8')

    def close_spider(self, spider):
        self.dbpool.close();

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self.insert_db, item)
        return item

    def insert_db(self, tx, item):
        values = (
            item['isbn'],
            item['book_name'],
            item['author'],
            item['price'],
            item['good_rate'],
            item['pub_time'],
            item['book_size'],
            item['press'],
        )
        sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        tx.execute(sql, values)


class DdbookPipeline(object):

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_db')
        host = spider.settings.get('MYSQL_HOST', '127.0.0.1')
        port = spider.settings.get('MYSQL_PORT', 3306)
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', '12345678')
        self.cnx = mysql.connector.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset='utf8')
        self.cur = self.cnx.cursor()

    def close_spider(self, spider):
        self.cur.commit()
        self.cur.close()
        self.cnx.close()

    def process_item(self, item, spider):
        self.insert_db(item)
        return item

    def insert_db(self, item):
        values = (
            item['isbn'],
            item['book_name'],
            item['author'],
            item['price'],
            item['good_rate'],
            item['pub_time'],
            item['book_size'],
            item['press'],
        )

        sql = 'INSERT INTO books VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
        self.cur.execute(sql, values)
        self.cur.execute('commit')
