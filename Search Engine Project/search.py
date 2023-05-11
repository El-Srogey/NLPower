# The search (Quering) API

from settings import *
import requests
import pandas as pd
from storage import DBStorage
from urllib.parse import quote_plus
from time import time


def search_api(query, pages = (RESULT_COUNT // 10)): # RESULT_COUNT: num_of_pages ---> settings.py
    results = []
    for i in range(pages):
        start = i * 10 + 1  # rank for each first result (in page 1: 1st record = 1, 2nd = 11)
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            query=quote_plus(query),  # to format special chars in query if any (e.g spaces)
            start = start
        )
        # Reminder: SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&num=10&gl=" + COUNTRY
        
        result = requests.get(url)
        data = result.json()  # convert from json to dict
        results += (data['items'])  # concatnate not append
        
    res_df = pd.DataFrame.from_dict(results)
    res_df['rank'] = list(range(1, res_df.shape[0] + 1))
    res_df = res_df[['link', 'title', 'rank', 'snippet']]
    
    return res_df


def scrape(links):
    html = []
    for link in links:
        try:
            result = requests.get(link, timeout=5)
            html.append(result.text)
        except:
            pass
    return html


def search(query):
    columns = ['query', 'rank', 'link','title', 'snippet', 'html', 'created']
    db = DBStorage()
    
    # if the query result is in the DB already
    if db.query_results(query).shape[0] >= 1:  # if the res_df contains any records
        result = db.query_results(query)
        result['created'] = pd.to_datetime(result['created'])  
        return result[columns]   # get from the results table only (column)
    
    # else (query result not in the DB)
    res_df = search_api(query)  # return ('link', 'title', 'rank', 'snippet') columns
    res_df['query'] = query 
    res_df['created'] = time()
    html = scrape(res_df['link'])  # take some time :(  
    res_df['html'] = html
    res_df = res_df[columns]  # make it's in the right order as should be inserted into DB
    
    res_df.apply(lambda x: db.insert_rows(x), axis=1)  # insert into DB
    return res_df