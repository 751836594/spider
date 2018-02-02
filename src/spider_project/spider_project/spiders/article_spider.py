#!/usr/bin/env python
# encoding: utf-8

"""
@version: 3.6
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: jianshu_spider.py
@time: 2018/1/23 下午3:02
"""
import os

import fcntl
import scrapy
import html2text
from scrapy import Selector

from lib.article import article_url_list
from tools.db_helper import *


class ArticleSpider(scrapy.Spider):
    name = "article"
    dir_path = '%s/../html/' % os.path.dirname(os.path.realpath(__file__))

    def start_requests(self):
        urls = article_url_list()
        for item in urls:
            yield scrapy.Request(url=item['url'], callback=self.parse, cookies=self.format_cookie(), headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'})

    def parse(self, response):
        self.craw(response=response)

    def write(self, data):
        """
        写入文件
        :param data:
        :return:
        """
        # exit()
        file_path = '%s/互联网.json' % (self.dir_path)
        # 打开文件
        file_object = open(file_path, 'a+')
        # 文件加锁
        fcntl.flock(file_object, fcntl.LOCK_EX)
        # 文件写入数据
        file_object.write('%s\n' % data)
        # 文件解锁
        fcntl.flock(file_object, fcntl.LOCK_UN)
        # 释放句柄
        file_object.close()

    @staticmethod
    def format_cookie():
        s = '_ga=GA1.2.26096315.1501133975; remember_user_token=W1s2MDY5NTQ5XSwiJDJhJDEwJC5oN05SSVU2ZGtvOHdWLmVWdEZyTWUiLCIxNTE1NTc1ODcxLjkxOTY5OTciXQ%3D%3D--314c30dee64a6a6ad8c3dc60951c856bfa752ed1; read_mode=day; default_font=font2; locale=zh-CN; _m7e_session=51772d1260dfb93f9d40173b4f1f9e0e; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1516243739,1516349671,1516615662,1516674267; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%226069549%22%2C%22%24device_id%22%3A%2215f46f0cb9916a-018b56c6157445-31667c00-1296000-15f46f0cb9ab05%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22index-collections%22%7D%2C%22first_id%22%3A%2215f46f0cb9916a-018b56c6157445-31667c00-1296000-15f46f0cb9ab05%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1516689721'

        s_l = s.split(';')
        s_d = {}
        for item in s_l:
            t_l = item.split('=')
            s_d[t_l[0]] = t_l[1]

        return s_d

    def download(self, response):
        """
        下载抓取html页面样本
        :param response:
        :return:
        """
        # page = response.url.split("=")[-1]
        filename = 'content-%s.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    def craw(self, response):
        """
        数据处理和入库
        :param response:
        :return:
        """
        uuids = Selector(response=response).xpath(
            '//div[@class="note-bottom"]/div[@data-vcomp="recommended-notes"]/@data-note-id').extract()
        hxs = Selector(response=response).xpath(
            '//div[@class="note"]/div[@class="post"]/div[@class="article"]/div[@class="show-content"]').extract()

        content = hxs[0].replace('//', 'https://').replace('data-original-src', 'src').replace(
            '<div class="image-caption">mark</div>', '')

        res = html2text.html2text(content)
        uuid = uuids[0]
        with DbHelper() as conn:
            row = {
                'uuid': uuid,
                'content': res.replace('-\n', '-')
            }
            insert_row(conn, 'jianshu_content', row)
            # queue.put_queue('cover', {'uuid': "from crm_sale.biz import queue"})
