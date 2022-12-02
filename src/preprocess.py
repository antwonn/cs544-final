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
from nltk.stem.snowball import SnowballStemmer


filter_words = ['also', 'would', 'should', 'could', 'one', 'two', 'three', 'four',
    'five', 'six', 'seven', 'eight', 'nine', 'ten', 'zero', 'used', 'good', 'bad',
    'terrible', 'awesome', 'like', 'dislike', 'become', 'became', 'called', 'often',
    'always', 'rarely', 'however', 'nonetheless', 'but', 'later', 'include', 'known',
    'another', 'around', 'along']

def preprocess(content):
    # data cleaning, lemmerization...
    # Change the following code with the data cleaning and preprocessing code you used
    content = content.lower()
    #content = re.split('https:\/\/.*', str(content))[0]
    #content = content.replace('\d+', '')
    content = content.strip()
    #content = contractions.fix(content)
    content = content.split()
    #content = [x.translate(str.maketrans('', '', string.punctuation)) for x in content] 
    #content = [x.replace('[^a-zA-Z]', '') for x in content]
    stop = stopwords.words('english')
    content = ['' if x in stop else x for x in content]
    content = ['' if x in filter_words else x for x in content]
    #stemmer = SnowballStemmer('english')
    #content = [stemmer.stem(x) for x in content]
    content = ' '.join(content)
    tokens = word_tokenize(content)
    # Change the code above with the data cleaning and preprocessing code you used
    return tokens

data_path = './articles_dataset.csv'
articles = pd.read_csv(data_path)[['title', 'content']]
articles['tokens'] = articles['content'].apply(lambda x: preprocess(str(x)))
articles = articles[['title', 'tokens']]
articles.to_csv('preprocessed.csv')