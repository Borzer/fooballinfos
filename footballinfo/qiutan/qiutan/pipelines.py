# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi

class QiutanPipeline(object):
    def __init__(self):
        dbparms = dict(
            db='py19',
            user='root',
            password='',
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4'
        )
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    def process_item(self, item, spider):
        # 指定操作方法和操作的数据
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 指定异常处理方法
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    # 执行具体的插入
    # 根据不同的item 构建不同的sql语句并插入到mysql中
    def do_insert(self, cursor, item):
        try:
            insert_sql, params = item.get_item1()
            cursor.execute(insert_sql, params)
        except:
            print('正在爬取数据！=3=')

        try:
            insert_sql, match_data = item.get_item3()
            cursor.execute(insert_sql, match_data)
        except:
            print('正在爬取数据！=3=')

        try:
            insert_sql, data = item.get_item2()
            cursor.execute(insert_sql, data)
        except:
            print('正在爬取数据！=3=')

        try:
            insert_sql, player_data = item.get_item4()
            cursor.execute(insert_sql, player_data)
        except:
            print('正在爬取数据！=3=')
