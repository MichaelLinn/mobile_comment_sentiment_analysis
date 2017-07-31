# -*- coding:utf-8 -*- 
"""
Created on 7/27/17  4:48 PM
Author : Jason

"""
import pymongo
import mysql.connector


category = []
config = {
    'user': 'root',
    'password': '123456',
    'host': '192.168.200.206',
    'database': 'lenovoforum2',
}


client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['spider']

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

query = ("SELECT distinct(category) FROM keyword_order")

cursor.execute(query)

for cur in cursor:
    # tmp = cur[0].encode('utf-8')
    category.append(cur)


query = ("SELECT DISTINCT(child_category) FROM keyword_order WHERE category=%s ")

for item in category:
    cursor.execute(query,(item))
    print "-------", item[0], "-------"
    subcategory = []
    for cur in cursor:
        subcategory.append(cur[0].encode('utf-8'))

    post = {"category": item[0].encode('utf-8'),
            "subcategory": subcategory}
    collection = db.mobile_category
    collection.insert_one(post)



