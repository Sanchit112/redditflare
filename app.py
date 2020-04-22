import pandas as pd
import flask
import pickle
import praw
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# load model
model = pickle.load(open('model.pkl','rb'))
reddit = praw.Reddit(client_id='mc9lbLzZ-4Il6Q',
                     client_secret='H4PTkK1nNC6RCqzLp8gvfvgWLCI',
                     user_agent='reddit_scraper',
                     username= "sanchit112",
                     password= "Death112")


r1 = re.compile('[/(){}\[\]\|@,;]')
r2 = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def clean_text(text):
    text = BeautifulSoup(text, "lxml").text # HTML decoding
    text = text.lower() # lowercase text
    text = r1.sub(' ', text) # replace certain symbols by space in text
    text = r2.sub('', text) # delete symbols from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove STOPWORDS from text
    return text



def prediction(url):
    submission = reddit.submission(url = url)
    data = {}
    data["title"] = clean_text(str(submission.title))
    data["url"] = clean_text(str(submission.url))
    data["body"] = clean_text(str(submission.selftext))

    submission.comments.replace_more(limit=None)
    comment = ''
    count = 0
    for top_level_comment in submission.comments:
        comment = comment + ' ' + top_level_comment.body
        count+=1
        if(count > 10):
             break    
    data["comment"] = clean_text(str(comment))
    combined_features = data["title"] +" "+ data["comment"] +" "+ data["url"] +" "+ data["body"]
    return model.predict([combined_features])

# app
app = flask.Flask(__name__)

# routes
@app.route('/', methods=['GET', 'POST'])
def main():  
    if flask.request.method == 'POST':
        # Extract the input
        text = flask.request.form['url']
        
        # Get the model's prediction
        flair = prediction(str(text))
    
        # Render the form again, but add in the prediction and remind user
        # of the values they input before
        return flask.jsonify(flair[0])



if __name__ == '__main__':
    app.run(port = 5000, debug=True)