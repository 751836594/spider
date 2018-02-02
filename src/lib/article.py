#!/usr/bin/env python
# encoding: utf-8

"""
@version: 3.6
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: article.py
@time: 2018/1/29 下午4:44
"""
from tools.db_helper import *


def article_url_list():
    sql = '''select url from article'''
    with DbHelper() as conn:
        res = select_all(conn, sql)

    return res
