from flask import Flask, request, render_template
from matplotlib.pyplot import flag
import pandas as pd
from app import TextClassification
from scrap import Scrap
import os

# global need_update   # to indicate if df is updated or not
# need_update = False

tc = TextClassification()
sc = Scrap()
images = os.path.join('static', 'images')
                      
app = Flask(__name__)  # create flask object
app.config['UPLOAD_FOLDER'] = images

@app.route("/")
def main():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'rs.jpg')
    return render_template("main.html", user_image = full_filename)

@app.route("/scrap")
def scraping():  # to take # pages to scrap
    return render_template("scrap.html")  

@app.route("/get_scrap")
def get_scrap():
    num_pages = request.args["num_pages"]
    try:
        sc.scrap(int(num_pages))
        return render_template("main.html")  # go back to main page after scraping done
    except:
        return render_template("fresult.html", result = "Failure! Un-able To Scrap")

@app.route("/predict")
def predict():  # to take url to predict
    return render_template("predict.html")

@app.route("/get_predict")
def get_predict():
    url = request.args["url"]  
    temp_df = tc.predict(url)
    if len(temp_df) == 0:  # link not found
        return render_template("fresult.html", result = "Failure! Link not found :(")
    else:
        return render_template('result.html', tables=[temp_df], titles=temp_df.columns.values)


# run app
app.run(debug=True)