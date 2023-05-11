import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from farasa.stemmer import FarasaStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class TextClassification:
    def __init__(self):
        self.df = pd.read_csv('y7.csv')
        self.tokenizer = RegexpTokenizer(r'\w+')  # return alphanumerics only
        self.fst = FarasaStemmer(interactive = True)  # farasa stemmer
        self.tf_idf =  TfidfVectorizer()
        self.nn =  NearestNeighbors()
        
        self.apply_clean()
        self.train()
    
    # Pre-Processing
    def clean(self, text):
        cleaned = []
        for w in self.tokenizer.tokenize(text):
            if w in stopwords.words('Arabic') or len(w) == 1:
                continue
            w = self.fst.stem(w)
            cleaned.append(w)
        return ' '.join(cleaned)
    
    # utility function
    def apply_clean(self):
        self.df['clean_text'] = self.df['text'].apply(self.clean)
    
    # train 
    def train(self):
        x = self.tf_idf.fit_transform(self.df.clean_text).toarray()  # text representation
        self.nn.fit(x)
        # get closest five elements
        self.indices = self.nn.kneighbors(x, return_distance=False)  # return indices for closest 5 neighbors
        self.urls = pd.DataFrame(self.indices)  # indices is (len(links) * 5) vector
        self.urls = self.urls.applymap(lambda x: self.df.iloc[x].links)
    
    # predict (take one of the urls in y7.csv and return closest neighbors)
    def predict(self, url):
        # self.urls[0] --> contains all the links
        # link matches
        if self.urls[0].str.contains(url).any():
            res = self.urls[self.urls[0] == url].values[0]  # return 5 links matched (closest neighbors)
            dic = {
            'imgs': [],
            'links': [],
            'creators': [],
             'dates': [],
             'brief_articles': [],
              'text': []
            }

            for url in res:
                temp_df = self.df[['imgs', 'links', 'creators', 'dates', 'brief_articles', 'text']][self.df.links == url]
                dic['imgs'].append(temp_df['imgs'].values[0])
                dic['links'].append(temp_df['links'].values[0])
                dic['creators'].append(temp_df['creators'].values[0])
                dic['dates'].append(temp_df['dates'].values[0])
                dic['brief_articles'].append(temp_df['brief_articles'].values[0])
                dic['text'].append(temp_df['text'].values[0])

            temp_df = pd.DataFrame(dic)
            return temp_df
        # link dose not match 
        else:
            return []
