# -*- coding: utf-8 -*-

"""
Python library for SAE event dispatch
"""

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging
import threading
import socket
import struct
import time
import json
import random
import string
from kafka import KafkaProducer

import json
import re

import pymysql
import xlrd
import requests
import urllib3
import sys

from hashlib import md5
from jproperties import Properties

#topic = "qihoosoc-preAgg-event"
topic = "hes-sae-group-0"
partition = 0

def ip():
    from random import randrange
    invalid = [10, 127, 169, 172, 192]
    first = randrange(1, 256)
    while first in invalid:
        first = randrange(1, 256)
    ip = ".".join([str(first), str(randrange(1, 256)), str(randrange(1, 256)), str(randrange(1, 256))])
    return ip
#
#web攻击命令执行

content = json.loads(r'{"receive_time":1544604757386,"event_level":0,"url":"http://landini.az/greeting-ecards","occur_time":1544604757386,"windows_event_id":5156,"dst_address":"8.8.8.8","event_name":"web访问","domain_name":"morning$circle.net","rule_id":"b3ccf7e5-3936-4c2b-b0d1-fba03fee404e","dst_port":8080,"original_log":"src:8.7.7.7,dst:8.8.8.8,domain:morning$circle.net,url:http://landini.az/greeting-ecards","file_hash":"54e1c3722102182bb133912ad4442e19","id":1150745862875136,"event_type":"/36JHPF2P0007/VNJN6T3B4eb9","src_address":"8.7.7.7","sa_da":"8.7.7.7_8.8.8.8","rule_name":"test","dev_address":"172.16.101.44","data_source":"Linux操作厂商"}')

def run():
    bootstrap_server = "10.229.1.187:19092"
    try:
        producer = KafkaProducer(bootstrap_servers=bootstrap_server, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    except Exception, e:
        print "exception,", e
        sys.exit(-1)
    for i in range(0,1):
        current_time = int(time.time() * 1000)
        content["occur_time"] = current_time
        src = ip()
        #content['src_address'] = '::FFFF:10.16.17.80'#src
        dst = ip()
        #content['dst_address'] = '::FFFF:2.16.17.80'#dst
        content["id"] = id_generator()
        content['event_name'] = r'web访问'
        content['event_level'] = "警告"
        print content
        producer.send(topic=topic, value=content, partition=0)
        #time.sleep(0.001)
        producer.flush()


def id_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


run()