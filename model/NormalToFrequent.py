import numpy as np
import pandas as pd
import pickle
import sys

def makeNormalToFrequent(k, NPath, FPath):
    with open(NPath, 'rb') as N:
        normalDic = pickle.load(N)
    N.close()
    frequentDic = {}
    word_array = list(normalDic.keys())
    for word in word_array:
        if len(normalDic[word]) >= k:
            frequentDic[word] = normalDic[word]
    
    with open(FPath, 'wb') as F:
        pickle.dump(frequentDic, F)
    F.close()
    return frequentDic

if __name__ == '__main__':
    normalFilePath = sys.argv[1] #'/home/aicp05/data/normalWord.pickle'
    print('file path:', normalFilePath)
    toFrequentFilePath = './data/frequentWord.pickle'

    frequent = makeNormalToFrequent(200, normalFilePath, toFrequentFilePath)
    print(list(frequent.keys()))
    print(len(frequent))
# k == 200 => len(frequent) == 5635 
# k == 500 => len(frequent) == 2905
# k == 1000 => len(frequent) == 1634
# k == 10000 => len(frequent) == 106
