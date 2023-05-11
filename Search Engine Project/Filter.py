# to filter(rank) our result pages

from bs4 import BeautifulSoup
from settings import *
import re
from nltk.corpus import stopwords


en_stopwords = stopwords.words('English')

def scrape(row):
    soup = BeautifulSoup(row['html'], 'lxml')
    page_content = soup.get_text()
    # pre-process the text
    page_content = page_content.lower()
    page_content = re.sub("[^a-z1-9 ]", "", page_content)  # remove special chars
    return page_content.strip()


# get the freq of query's keywords from each page content
def query_freq(row):
    content = scrape(row)
    query_words = row['query'].strip().split()
    # remove stopword from query if any
    for word in query_words:
        if word in en_stopwords:
            querey_words.remove(word)

    counts = [content.count(word.lower()) for word in query_words]  # freq of each wrod
    result = sum(counts)
    return result
    
    
class Filter():
    def __init__(self, res_df):
        self.results = res_df.copy()  # results
        
    def filter_count(self):  
        # num_words_filter 
        contents = self.results.apply(scrape, axis=1)  # returns series of contents
        word_counts = contents.apply(lambda x: len(x.split()))  # count # words
        
        # query's keywords freq filter
        word_freq = self.results.apply(query_freq, axis=1)
            
        # divide all by median so less than 1 --> less than median #_words
        word_counts /= word_counts.median()  # as median get bigger as it gets more better
        
        self.results['rank'] += word_counts  # commit 1st filter
        self.results['rank'] += word_freq  # commit 2nd filter
        self.results = self.results.sort_values(by='rank', ascending=False)  # desc sort
        
        # rest the index and re-rank the pages
        self.results.reset_index(drop=True, inplace=True)
        self.results['rank'] = list(range(1, self.results.shape[0] + 1))
        return self.results
    
    
        