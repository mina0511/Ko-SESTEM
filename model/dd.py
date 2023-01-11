import pickle

decade_positive_word_set = []
decade_negative_word_set = []

for year in range(2010, 2019):
    dic1 = []
    positive = []
    negative = []
    positive_word_set = []
    negative_word_set = []



    with open('./data/O_{}.pickle'.format(year), "rb") as O:
        dic = pickle.load(O) 
        for i in range(len(dic[0])):
            j = dic[0][i]-dic[1][i]
            dic1.append(j)
            if j > 0:
                positive.append(i)
            if j < 0:
                negative.append(i)
#        print(len(dic[0]))
 #       print(positive)
#        print(negative)

    with open('./data/sentimentalWord{}.pickle'.format(year), "rb") as a:
        words = pickle.load(a)
        word_total = words[0]+words[1]
        for i in range(len(words[0])+len(words[1])):
            if i in positive:
                positive_word_set.append(word_total[i][0])
            if i in negative:
                negative_word_set.append(word_total[i][0])
        decade_positive_word_set.append(positive_word_set)
        decade_negative_word_set.append(negative_word_set)
        print("================== NEGATIVE WORD SET {}==================".format(year))
        for word in negative_word_set:
            print(word, end=" | ")
        print()
        print("=======================================================")
        print()
        print("================== POSITIVE WORD SET {}==================".format(year))
        for word in positive_word_set:
            print(word, end=" | ")
        print()
        print("=======================================================")
        print()
negative_concat = []
positive_concat = []

for i in range(len(decade_positive_word_set)):
    assert(len(decade_positive_word_set) == len(decade_negative_word_set))
    
    negative_concat += decade_negative_word_set[i]
    positive_concat += decade_positive_word_set[i]

negative_sorted = []
positive_sorted = []

for word in set(negative_concat):
    negative_sorted.append((word, negative_concat.count(word)))

for word in set(positive_concat):
    positive_sorted.append((word, positive_concat.count(word)))


negative_sorted.sort(key=lambda x: x[1], reverse=True)
positive_sorted.sort(key=lambda x: x[1], reverse=True)

print("================== NEGATIVE WORD SET ==================")
for word in negative_sorted:
    print(word[0]+":", word[1], end=" | ")
print()
print("=======================================================")
print()
print("================== POSITIVE WORD SET ==================")
for word in positive_sorted:
    print(word[0]+":", word[1], end=" | ")
print()
print("=======================================================")
print()

# negative_intersection = set(decade_negative_word_set[0])
# positive_intersection = set(decade_positive_word_set[0])


# for i in range(len(decade_positive_word_set)):
#     assert(len(decade_positive_word_set) == len(decade_negative_word_set))
#     if len(decade_negative_word_set[i]) > 0:
#         negative_intersection &= set(decade_negative_word_set[i])
#     if len(decade_positive_word_set[i]) > 0:
#         positive_intersection &= set(decade_positive_word_set[i])

# print("================== NEGATIVE WORD SET ==================")
# print(negative_intersection)
# print("=======================================================")
# print()
# print("================== POSITIVE WORD SET ==================")
# print(positive_intersection)
# print("=======================================================")
