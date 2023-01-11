import numpy as np
import pandas as pd
import pickle
#import sys
'''
#sys.path.append('~/.local/bin')
#from tqdm import tqdm

def frequentWord(word_array, article_array, k):
    # Initialize
    word_count_dic = {}
    for word in word_array:
        word_count_dic[word] = []
    
    # word counting: 해당 word가 있는 기사 인덱스를 word_count_dic에 배열로 삽입 
    length = len(article_array)
    for article_index in range(length):
        print('{0} / {1}'.format(article_index, length), end='\r')
        for word in word_array:
            if word in article_array[article_index]:
                word_count_dic[word].append(article_index)
    
    bigger_than_k = {}
    for word in word_array:
        if len(word_count_dic[word]) >= k:
            bigger_than_k[word] = word_count_dic[word]
    
    return bigger_than_k

def split(word_count_dic, article_related_stock, alpha_plus, alpha_minus):
    frequent_word_list = list(word_count_dic.keys())
    length = len(frequent_word_list)
    plus_word_set = []
    minus_word_set = []
    
    total_articles = 0
    for word_index in range(length):
        print('{0} / {1}'.format(word_index, length), end='\r')
        word = frequent_word_list[word_index]
        article_list_containing_word = word_count_dic[word] 
        total_articles = len(article_list_containing_word)
        plus_articles = 0
        for article_index in article_list_containing_word:
            if article_related_stock[article_index] > 0:
                plus_articles += 1
        rate = plus_articles / total_articles
        print("word: {}, rate: {}".format(word, rate))
        if rate > alpha_plus:
            plus_word_set.append(word)
        elif rate < alpha_minus:
            minus_word_set.append(word)
    # 여기서 얻어진 plus_word_set, minus_word_set은 O+, O-와는 다르다. 
    # plus_word_set, minus_word_set의 합집합이 sentimental word set이다.
    # 굳이 둘을 나눈 이유는 후에 O+, O- 분포와 비교하기 위해서이다. 
    # 이 단계에서 얻어진 plus/minus_word_set의 단어들이 O+, O-에서 어떤 스코어를 갖는지.
    return [plus_word_set, minus_word_set]

# constructing word array
word_file_path = '/home/aicp05/data/filtered_noun_word.dat'
articleFile = open(word_file_path)
word_string = ''
for word in articleFile:
    word_string = word 
word_array = word_string.split('::')
'''
# constructing article dataframe
samsung_file_path = '/home/aicp05/data/samsung_articles_with_stock(final).dat' 
articleDF = pd.read_pickle(samsung_file_path)
print(articleDF.columns)
article_array = articleDF['article']
article_related_stock = articleDF['after_stock'] - articleDF['before_stock']
'''
print(len(article_array))
print(len(article_related_stock))

fWordSet = frequentWord(word_array, article_array[:10], 2)
toFrequentFilePath = '/home/aicp05/data/frequentWord.pickle'
with open(toFrequentFilePath, 'wb') as f:
    pickle.dump(fWordSet, f)
f.close()

sWordSet = split(fWordSet, article_related_stock, 0.6, 0.4)
print("positive: {}".format(sWordSet[0]))
print("negative: {}".format(sWordSet[1]))
'''
n=1100
print(article_related_stock[n:n+100])