import pandas as pd
import re
import string
import nltk
import random
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import contractions
from ast import literal_eval

def criticalword(keyword_lists):
    article_count = len(keyword_lists)
    keyword_dict = {}
    for list in keyword_lists:
        list = literal_eval(list)
        for word in list:
            if word in keyword_dict:
                keyword_dict[word] += 1
            else:
                keyword_dict[word] = 1
    criticals = {}
    for word in keyword_dict:
        if keyword_dict[word] <= 0.7*article_count:
            criticals[word] = keyword_dict[word]
    if (len(criticals) == 0):
        return '-'
    max_value = max(criticals.values())
    criticalwords = []
    for k, v in criticals.items():
        if v == max_value:
            criticalwords.append(k)
    print('possbile choice: ' + str(criticalwords))
    criticalword = random.choice(criticalwords)
    print('critical word: ' + criticalword)
    criticalrate = criticals[criticalword] / article_count
    print('critical rate: ' + str(round(criticalrate, 2)))
    print('articles possible: ' + str(len(keyword_lists)))
    return criticalword

def divide(model, guess, hits):
    if hits >= 30:
        for index, row in model.iterrows():
            keywords = literal_eval(row['keywords'])
            if guess not in keywords:
                model = model.drop(index)
            elif keywords[guess] < 30:
                model = model.drop(index)
    elif hits >= 15:
        for index, row in model.iterrows():
            keywords = literal_eval(row['keywords'])
            if guess not in keywords:
                model = model.drop(index)
            elif keywords[guess] < 15:
                model = model.drop(index)
            elif keywords[guess] >= 30:
                model = model.drop(index)
    elif hits >= keyword_basefreq: 
        for index, row in model.iterrows():
            keywords = literal_eval(row['keywords'])
            if guess not in keywords:
                model = model.drop(index)
            elif keywords[guess] >= 15:
                model = model.drop(index)
    else:
        for index, row in model.iterrows():
            keywords = literal_eval(row['keywords'])
            if guess in keywords:
                model = model.drop(index)
    return model

data_path = './key_5_5.csv'
keyword_basefreq = 5
key_table = pd.read_csv(data_path)[['title', 'keywords']]
next_guess = criticalword(key_table['keywords'])

print('First guess: ' + next_guess)
print('How many hits? (int)')
hit_count = input()
if hit_count.isdigit():
    hit_count = int(hit_count)
else:
    print('Error input. Exit.')
    exit()

while len(key_table['keywords']) > 1:
    key_table = divide(key_table, next_guess, hit_count)
    next_guess = criticalword(key_table['keywords'])
    if next_guess == '-':
        break
    print('Next guess: ' + next_guess)
    print('How many hits? (int)')
    hit_count = input()
    if hit_count.isdigit():
        hit_count = int(hit_count)
    else:
        print('Error input. Exit.')
        exit()

print('The title: ' + str(key_table['title'].tolist()))