# -*- coding:utf-8 -*- 
"""
Created on 7/31/17  3:04 PM
Author : Jason

"""
import jieba

class mobile_analysis:

    # keyword bank
    keywords_file = "../word_bank/keywords.txt"
    # stopword bank
    stopword_file = "../word_bank/stopword.txt"
    # 指定自己自定义的词典，以便包含jieba词库里没有的词，提高jieba分词的精度
    self_built_wordbank_file = "../word_bank/ciku.txt"
    # positive word bank
    posword_file = '../word_bank/pos_siat.txt'
    # negative word bank
    negword_file = '../word_bank/neg_siat.txt'
    # set word distance
    distance = 5

    def __init__(self, keyword_file = keywords_file, stopword_file = stopword_file,
                 selfbuilt_wordbank = self_built_wordbank_file, pos_file = posword_file, neg_file = negword_file ):
        self.keywords = self.load_keywords(keyword_file)
        self.stopwords = self.load_stopwords(stopword_file)
        self.pos_words = self.load_poswords(pos_file)
        self.neg_words = self.load_negwords(neg_file)
        self.selfbuilt_words = selfbuilt_wordbank

    def set_word_distance(self, distance):
        self.distance = distance

    def load_keywords(self, filename):
        keywords = [line.strip().decode('utf-8') for line in open(filename)]
        return keywords

    def load_stopwords(self, filename):
        stopwords = [line.strip().decode('utf-8') for line in open(filename)]
        return stopwords

    def load_poswords(self, filename):
        pos_word = []
        pos_file = open(filename)
        lines = pos_file.readlines()
        for line in lines:
            if line.strip() != u''.encode('utf8'):
                pos_word.append(line.strip())
        return pos_word

    def load_negwords(self, filename):
        neg_word = []
        neg_file = open(filename)
        for line in neg_file.readlines():
            if line.strip() != u''.encode('utf8'):
                neg_word.append(line.strip())
        return neg_word

    """
    # word segmentation
    Input: the original comments
    Output: a keyword list

    """
    def segment_jieba(self, text):

        jieba.load_userdict(self.selfbuilt_words)

        default_mode = jieba.cut(text)
        seg_text = []
        for seg in default_mode:
            if seg not in self.stopwords:
                seg_text.append(seg)

        notags = ' '.join(seg_text)
        # print notags
        return seg_text

    """
    # sentiment analysis
    Input: the word list from comment pretreated by Jieba
    Output: positive keyword list and negative keyword list

    """
    def analyse_sentiment(self, comment):

        distance = self.distance
        neg_word = []
        pos_word = []
        distance_list = []

        comment_word = self.segment_jieba(comment)

        for i in range(1, distance + 1):
            distance_list.append(-i)
            distance_list.append(i)

        for i in range(len(comment_word)):
            word = comment_word[i]
            for j in range(len(self.keywords)):
                if word == self.keywords[j]:
                    flag = i
                    for dist in distance_list:
                        idx = flag + dist
                        if idx > 0 and idx < len(comment_word):
                            e_word = comment_word[idx]
                            e_word = e_word.encode('utf-8')
                            for pos in self.pos_words:
                                if e_word == pos:
                                    neg_word.append(word)
                            for neg in self.neg_words:
                                if e_word == neg:
                                    pos_word.append(word)

        return pos_word, neg_word
