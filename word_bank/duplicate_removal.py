# -*- coding:utf-8 -*- 
"""
Created on 8/7/17  7:17 PM
Author : Jason

"""

filename = "../word_bank/neg_siat.txt"



def remove_duplicate(filename):

    words = []
    with open(filename,'rt') as f:
        for line in f:
            words.append(line.strip())
    print len(words)
    words = list(set(words))
    print len(words)

    with open("../word_bank/neg_key.txt","wt") as f:
        for item in words:
            f.write(item + "\n")


remove_duplicate(filename)


