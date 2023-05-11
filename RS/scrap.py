# The code saves the following columns for each article:

# "titles": the title of the article.
# "dates": the date the article was published.
# "brief_articles": a brief summary of the article.
# "links": the link to the article.
# "imgs": the link to the image associated with the article.
# "key_words": a list of key words associated with the article.
# "creators": the name of the author(s) of the article.
# "text": a concatenation of the article's title, author(s), key words, and brief summary.


from bs4 import BeautifulSoup
import requests
import pandas as pd


class Scrap():
    def __init__(self):
        pass
    
    # max_num of pages ---> each page contains 40 articles
    def scrap(self, max_num = 10):  
        pnum = 1  # page-num
        y7_link = "https://www.youm7.com"

        titles = []
        dates = []
        brief_articles = []
        links = []
        imgs = []

        while pnum <= max_num:   #
            result = requests.get(f"https://www.youm7.com/Section/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D8%A9/298/{pnum}")   # page number {pnum}
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            
            # for each page
            for i in range(len(soup.find_all("div", {"class" : "col-xs-12 bigOneSec"}))):  
                try:
                    titles.append(soup.find_all("div", {"class" : "col-xs-12 bigOneSec"})[i].img.attrs["alt"].strip())
                    dates.append(soup.find_all("div", {"class" : "col-xs-12 bigOneSec"})[i].span.text.strip())
                    brief_articles.append(soup.find_all("div", {"class" : "col-xs-12 bigOneSec"})[i].p.text.strip())
                    links.append(y7_link + soup.find_all("div", {"class" : "col-xs-12 bigOneSec"})[i].a.attrs["href"].strip())
                    imgs.append(soup.find_all("div", {"class" : "col-xs-12 bigOneSec"})[i].find("img").attrs['src'])
                    
                except:
                    print(f'page # {i} are failed')
            
            pnum += 1  # end of while loop
        
        dic = {
        'titles' : titles,
        'dates': dates,
        'brief_articles': brief_articles,
        'links': links,
        'imgs': imgs   
        }
        
        df = pd.DataFrame(dic)
        
        creators = []
        key_words = []
        
        # for each atricle in page number {pnum}
        for link in df.links:
            result = requests.get(link)
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            creator = soup.find("span", {"class" : "writeBy"}).text.strip().split()[:]

            for c in ["كتبت" ,"كتب" ,"إعداد"] :
                if c in creator:
                        creator = creator[1:]
            keys = []
            for k in soup.find("div", {"class": "tags"}).find_all("h3"):
                keys.append(k.a.text.strip())

            key_words.append(" ".join(keys))
            creators.append(" ".join(creator))

        df["key_words"] = key_words
        df["creators"] = creators
        df["text"] = df.titles + " " + df.creators + " " + df.key_words + " " + df.brief_articles
        
        df.drop_duplicates(inplace = True)
        if 'Unnamed: 0' in df.columns:
            df.drop('Unnamed: 0', axis=1, inplace=True)
        
        df1 = pd.read_csv('y7.csv')  # old df (pre-scraped articles)
        final_df = pd.concat([df, df1])  # combine old df with new one

        final_df.to_csv('y7.csv')  # re-write(save)