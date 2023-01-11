from numpy.lib.financial import rate
import pandas as pd
import numpy as np
import pickle
import sys

def count(word, article):
    c = 0
    for articleWord in article:
        if word == articleWord:
            c += 1
    return c

def articleToRate(sentimentalWordList, articleArray):
    rateList = []
    i = 1
    aLen = len(articleArray)
    for article in articleArray:
        print("{0} / {1}".format(i, aLen), end='\r')
        rateList.append([])
        for word in sentimentalWordList:
            rateList[-1].append(count(word, article))
        i += 1
    return rateList



if __name__ == '__main__':
    samsung_file_path = './data/samsung_articles_with_stock.dat' 
    articleDF = pd.read_pickle(samsung_file_path)
    article_array = articleDF['article']

    sFilePath = sys.argv[1]
    with open(sFilePath, 'rb') as S:
        psWordList = pickle.load(S)
    sWordList = psWordList[0] + psWordList[1]
    onlyWord = []
    for pair in sWordList:
        onlyWord.append(pair[0])
    
    rL = articleToRate(onlyWord, article_array)
    toRateFilePath = '../articleRate.pickle'
    with open(toRateFilePath, 'wb') as R:
        pickle.dump(rL, R)
    
    print(rL[0:100])
    print(len(rL))

    
