# -*- coding:utf-8 -*- 
"""
Created on 8/7/17  3:24 PM
Author : Jason

"""
import pymongo
from mobile import comment_analysis

anaysis = comment_analysis.mobile_analysis()
anaysis.set_word_distance(8)
# Connect to MongoDB
client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['spider']

# Select collection in the MongoDB
collection = db['HUAWEI']


"""
do the sentiment analysis and statistic on comment of a specific mobilephone brand
# Input: one document in the collection of the Mobilephone

"""
def stat_commemt(comment_record):
    remain = 0
    list = comment_record['reviews']
    pos = []
    neg = []
    id = comment_record['_id']
    for l in list:
        review = l['review']

        p,n = anaysis.analyse_sentiment(review)
        if len(p) != 0 or len(n) != 0:
            remain = remain + 1
        pos.extend(p)
        neg.extend(n)


    cat_pos = {}
    cat_neg = {}
    category_mobile = db['mobile_category']
    cursor = category_mobile.find()

    for cur in cursor:
        cat = cur['category']
        print "-------", cat, "-------"
        for item in cur['subcategory']:
            for i in range(len(pos)):
                if pos[i] == item:
                    cat_pos[cat] = cat_pos.get(cat, 0) + 1

            for i in range(len(neg)):
                if neg[i] == item:
                    cat_neg[cat] = cat_neg.get(cat, 0) + 1


    #insert positive and negative features into the specific Mobilephone document in MongoDB
    collection.update_one(
        {"_id": id},
        {
        "$set":{
            "positive": cat_pos,
            "negative": cat_neg
        }
        }
    )

    return len(list), remain


# main function
s = 0
r = 0
cursor = collection.find()

for cur in cursor:
    s_t, r_t = stat_commemt(cur)
    s = s + s_t
    r = r + r_t

print "sum:", s
print "remain:", r
print "percentage:", float(r/s)
