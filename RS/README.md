# 👋 Welcome to Arabic-Aricles Recommender System (ARS)!

__ARS is a Python-based web application that uses natural language processing techniques to recommend (ARABIC) news articles based on their semantic similarity.__\
With ARS, you can easily discover related news articles, explore different topics, and stay up-to-date with the latest news.

## 🚀 Getting Started
To get started with NewsCluster, you need to install the required Python packages using pip:
```
pip install -r requirements.txt
```
Once you have installed the required packages, you can start the web application by running the following command:
```
py API.py
```
__The web application will be available at http://localhost:5000/.__

## 📖 How it works
ARS uses a combination of natural language processing techniques and recommendations algorithms to group similar news articles together.
When you provide a URL to a news article, ARS fetches the article, extracts its text and relevant features. The model assigns each article to one or more similarity 
score based on its semantic similarity to other articles in the dataset.

## 🌐 Technologies Used
1. Python 3.7+
2. Flask
3. Pandas
4. Scikit-learn
5. Beautiful Soup
