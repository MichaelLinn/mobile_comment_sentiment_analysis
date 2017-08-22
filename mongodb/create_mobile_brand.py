# -*- coding:utf-8 -*- 
"""
Created on 8/16/17  3:07 PM
Author : Jason

"""
import pymongo

client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['spider']
collection = db.mobile_brand

list = ['HUAWEI', 'LENOVO', 'VIVO', 'APPLE', 'OPPO', 'SAMSUNG']
for item in list:
    post = {"brand_name": item}
    collection.insert_one(post)

