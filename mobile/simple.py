# -*- coding:utf-8 -*- 
"""
Created on 7/31/17  3:03 PM
Author : Jason

"""
import pymongo
from mobile import comment_analysis

# Create a instance from CLASS mobile_analysis
analysis = comment_analysis.mobile_analysis()

# Connect to MongoDB
client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['spider']
collection = db['zol']
reviews = collection.find_one()

# Fetch a comment from MongoDB
comment = reviews['phone_reviews'][0]['comment']['summary']

# Set up the word distance(default value is 5)
analysis.set_word_distance(5)

# Get a positive keyword list and a negative keyword list based on your original comment
pos, neg = analysis.analyse_sentiment(comment)

print "positive keyword:"
for n in neg:
    print n
print "negative keyword:"
for p in pos:
    print p
