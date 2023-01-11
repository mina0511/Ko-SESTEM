import pickle
import pandas as pd
import sys

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
        if rate > alpha_plus:
            plus_word_set.append([word, rate])
        elif rate < alpha_minus:
            minus_word_set.append([word, rate])
    return [plus_word_set, minus_word_set]

    
if __name__ == '__main__':
    samsung_file_path = './data/samsung_articles_with_stock.dat' 
    articleDF = pd.read_pickle(samsung_file_path)
    article_related_stock = articleDF['after_stock'] - articleDF['before_stock']

    with open("./data/frequentWord.pickle", 'rb') as f:
        fWordSet = pickle.load(f)
    f.close()
    sWordSet = split(fWordSet, article_related_stock, 0.52, 0.48)

    with open(sys.argv[1], 'wb') as sf:
        pickle.dump(sWordSet, sf)
    sf.close()
