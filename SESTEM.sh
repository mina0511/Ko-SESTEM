#!/bin/bash

for year in {2010..2021}
do
    python3 -u model/NormalToFrequent.py ./data/wordDicAt${year}.pickle  
    python3 -u model/split_final.py ./data/sentimentalWord${year}.pickle 
    python3 -u model/ArticleToRate.py ./data/sentimentalWord${year}.pickle
    python3 -u model/SESTEM.py ./data/O_${year}.pickle
    python3 -u model/dd.py
done
