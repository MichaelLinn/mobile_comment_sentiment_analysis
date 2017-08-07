# -*- coding:utf-8 -*- 
"""
Created on 8/1/17  11:21 AM
Author : Jason

"""
import pymongo
from mobile.comment_analysis import mobile_analysis


category = []
config = {
    'user': 'root',
    'password': '123456',
    'host': '192.168.200.206',
    'database': 'lenovoforum2',
}

client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['spider']
# Select collection
collection = db.mobile_category

# insert a new subcategory into an appointed category
category = "外观"
new_category = "什么鬼"
collection.update({'category':category},
                  {'$push':{'subcategory': new_category}})
