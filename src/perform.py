import pandas as pd
import random
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
    #print('possbile choice: ' + str(criticalwords))
    criticalword = random.choice(criticalwords)
    #print('critical word: ' + criticalword)
    criticalrate = criticals[criticalword] / article_count
    #print('critical rate: ' + str(round(criticalrate, 2)))
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

def count(guess, content):
    occur = 0
    for token in content:
        if guess == token:
            occur += 1
    return occur

data_path = './key_5_5.csv'
keyword_basefreq = 5
og_key_table = pd.read_csv(data_path)[['title', 'keywords']]

data_path = './preprocessed.csv'
articles = pd.read_csv(data_path)[['title', 'tokens']]
articles = articles.sample(n=20, random_state=1)

correct = 0
wrong = 0
guess_count = 0
article_count = 0
hit = 0
critical_hit = 0
for index, row in articles.iterrows():
    article_count += 1
    key_table = og_key_table
    content = literal_eval(row['tokens'])
    while len(key_table['keywords']) > 1:
        next_guess = criticalword(key_table['keywords'])
        #print(next_guess)
        if next_guess == '-':
            break
        hit_count = count(next_guess, content)
        if hit_count > 0:
            hit += 1
        if hit_count > 5:
            critical_hit += 1
        #print(hit_count)
        key_table = divide(key_table, next_guess, hit_count)
        guess_count += 1
    for title in key_table['title'].tolist():
        if title == row['title']:
            correct += 1
            #print('correct')
            break
        else:
            wrong += 1
            #print('wrong')
average_guess = guess_count / article_count
hit_ratio = hit / guess_count
critical_hit_ratio = critical_hit / guess_count
accuracy = correct / (correct + wrong)
print('average guess for random article: ' + str(round(average_guess, 2)))
print('guess hit ratio: ' + str(round(hit_ratio, 2)))
print('guess critical hit ratio: ' + str(round(critical_hit_ratio, 2)))
print('title accuracy overall: ' + str(round(accuracy)))