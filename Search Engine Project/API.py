from flask import Flask, render_template, request
from search import search
from time import time
from Filter import Filter

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')

@app.route('/result')
def result():
    query = request.args['query']
    tic = time()
    res_df = search(query)  # searching the API or DB
    toc = time()

    fl = Filter(res_df)
    res_df = fl.filter_count()

    res_df = res_df[['title', 'snippet', 'link', 'created']]
    return render_template('result.html', table=res_df, search_time=toc - tic, query=query)
# run
app.run()