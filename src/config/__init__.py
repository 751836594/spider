#!/usr/bin/env python
# encoding: utf-8

"""
@version: 3.6
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: __init__.py
@time: 2018/1/29 下午4:03
"""
import os


def get_env():
    """
    获取运行环境
    """
    file_name = '/'.join((os.path.dirname(os.path.abspath(__file__)), 'config_mode'))
    with open(file_name) as f:
        env = f.read()
        if env:
            return env.strip()
        else:
            return ''


def get_ns():
    """
    获取运行环境
    """
    file_name = '/'.join((os.path.dirname(os.path.abspath(__file__)), 'config_ns'))
    with open(file_name) as f:
        env = f.read()
        if env:
            return env.strip()
        else:
            return ''


config_env = get_env()

# 命名空间
config_ns = get_ns()

if config_env == 'online':
    from .online import *
elif config_env == 'dev':
    from .dev import *
else:
    raise Exception('配置错误:config_env:%s' % (config_env,))
