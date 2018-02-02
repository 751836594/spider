#!/usr/bin/env python
# encoding: utf-8

"""
@version: 2.7
@author: steven
@license: Apache Licence 
@contact: 751836594@qq.com
@site: 
@software: PyCharm
@file: crm_sale_update.py
@time: 2017/8/22 下午2:49
"""
import json

import pika

from config import rabbit_mq, config_ns

virtual_host = '/' + config_ns

_last_connection = {'last': None}


def put_queue(queue_name, message):
    """
    推送队列
    :param queue_name:
    :param message:
    :return:
    """
    connection = get_conn_mq()
    channel = connection.channel()

    channel.exchange_declare(exchange='blog', exchange_type='topic', durable=True)
    channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange='blog',
                       queue=queue_name,
                       routing_key=queue_name)
    channel.basic_qos(prefetch_count=1)

    if isinstance(message, dict):
        message = json.dumps(message)
    channel.basic_publish(exchange='blog',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print((" [x] Sent %r" % (message,)))


def get_conn_mq():
    """
    获取队列连接对象
    :return:
    """
    if _last_connection['last'] is None:
        credentials = pika.PlainCredentials(rabbit_mq['username'], rabbit_mq['password'])
        conn_mq = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbit_mq['host'],
                port=rabbit_mq['port'],
                credentials=credentials,
                virtual_host=virtual_host,
                heartbeat_interval=0,
                retry_delay=3
            )
        )
        _last_connection['last'] = conn_mq
    return _last_connection['last']
