# -*- coding:utf-8 -*- 
"""
Created on 7/19/17  12:09 PM
Author : Jason

"""

import jieba
import pymongo

# Connect to the MongoDB
client = pymongo.MongoClient('192.168.200.47', 27017)
db = client['spider']
collection = db['zol']

keywords = [line.strip().decode('utf-8') for line in open("../word_bank/keywords.txt")]
stopw = [line.strip().decode('utf-8') for line in open("../word_bank/stopword.txt")]

# load the self-built word bank into Jieba
jieba.load_userdict("../word_bank/ciku.txt")

sentPosWords = []
sentNegWords = []
negfile = open('../word_bank/neg.txt')
posfile = open('../word_bank/pos.txt')
negfile2 = open('../word_bank/neg_siat.txt')
posfile2 = open('../word_bank/pos_siat.txt')

neglines = negfile.readlines()
poslines = posfile.readlines()
neglines2 = negfile2.readlines()
poslines2 = posfile2.readlines()

# Load the word bank
for negline in neglines:
    if negline.strip() != u''.encode('utf8'):
        sentNegWords.append(negline.strip())

for posline in poslines:
    if posline.strip() != u''.encode("utf8"):
        sentPosWords.append(posline.strip())

for negline2 in neglines2:
    if negline.strip() != u''.encode('utf8'):
        sentNegWords.append(negline2.strip())

for posline2 in poslines2:
    if posline.strip() != u''.encode("utf8"):
        sentPosWords.append(posline2.strip())

"""
# word segmentation
Input: the original comments
Output: a keyword list

"""
def segment_jieba(text):
    default_mode = jieba.cut(text)
    seg_text = []
    for seg in default_mode:
        if seg not in stopw:
            seg_text.append(seg)

    notags=' '.join(seg_text)
    # print notags
    return seg_text

"""
# sentiment analysis
Input: the word list from comment pretreated by Jieba
Output: positive keyword list and negative keyword list

"""
def analyse_sentiment(comment_word):

    distance = 5
    neg_word = []
    pos_word = []
    distance_list =[]

    for i in range(1, distance+1):
        distance_list.append(-i)
        distance_list.append(i)

    for i in range(len(comment_word)):
        word = comment_word[i]
        for j in range(len(keywords)):
            if word == keywords[j]:
                flag = i
                for dist in distance_list:
                    idx = flag + dist

                    if idx > 0 and idx < len(comment_word):
                        e_word = comment_word[idx]
                        e_word = e_word.encode('utf-8')
                        for pos in sentPosWords:
                            if e_word == pos:
                                neg_word.append(word)
                        for neg in sentNegWords:
                            if e_word == neg:
                                pos_word.append(word)
    return neg_word, pos_word


"""
main function

"""
for post in collection.find():
    try:
        reviews = post['phone_reviews']
        for i in range(len(reviews)):
            comment = reviews[i]['comment']['summary']
            comment_words = segment_jieba(comment)
            nw, pw = analyse_sentiment(comment_words)
            for p in pw:
                print p

            print "--------------"

            for n in nw:
                print n
    except Exception as e:
        print 'Reason:', e









