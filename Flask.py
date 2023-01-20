from flask import Flask, render_template, url_for, request, redirect,request, send_from_directory,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tweepy as tw
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user = request.form['username']
        tweepy(user)
        return render_template("image.html")
    else:
        return render_template("index.html")

def tweepy(user):

    with open('config.json', 'r') as f:
        config = json.load(f)
    consumer_key = config['consumer_key']
    consumer_secret = config['consumer_secret']
    access_token = config['access_token']
    access_token_secret = config['access_token_secret']

    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth)

    # Get tweets from a user
    username = user

    tweets = api.user_timeline(screen_name=username, count=500,exclude_replies=True,include_rts=False)
    with open("static/images/images.txt", "w") as f:
        for i, tweet in enumerate(tweets):
            media = tweet.entities.get('media', [])
            if(len(media) > 0):
                f.write(media[0]['media_url'])
                if(i != len(tweets) - 1):
                    f.write("\n")


if __name__ == "__main__":
    app.run(debug=True)
