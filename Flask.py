from flask import Flask, render_template, url_for, request, redirect,request, send_from_directory,make_response,jsonify,send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import tweepy as tw
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    image_link = db.Column(db.String(200), nullable=False)

    def __init__(self, username, image_link):
        self.username = username
        self.image_link = image_link

    def __repr__(self):
        return '<Task %r>' % self.id
# Create the table in the database
db.create_all()

@app.route('/previous_searches', methods=['GET'])
def previous_searches():
    usernames = set()
    tweets = Tweets.query.all()
    for tweet in tweets:
        usernames.add(tweet.username)
    return render_template("previous_searches.html", usernames=usernames)

@app.route('/view_images', methods=['POST'])
def view_images():
    username = request.form.get('usernames')
    images = []
    tweets = Tweets.query.filter_by(username=username)
    for tweet in tweets:
        images.append(tweet.image_link)
    return render_template("view_images.html", images=images, username=username)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user = request.form['username']
        tweets_count = request.form['tweets_count']
        tweepy(user, tweets_count)
        return render_template("image.html")
    else:
        return render_template("index.html")

@app.route('/get_image_links', methods=['GET'])
def get_image_links():
    username = request.args.get('username')
    tweets = Tweets.query.filter_by(username=username).all()
    image_links = [tweet.image_link for tweet in tweets]
    return jsonify(image_links)

def tweepy(user,tweets_count):
    tweets_count = int(tweets_count)
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

    tweets = api.user_timeline(screen_name=username, count=tweets_count,exclude_replies=True,include_rts=False)
    with open("static/images/images.txt", "w") as f:
        for i, tweet in enumerate(tweets):
            media = tweet.entities.get('media', [])
            if(len(media) > 0):
                f.write(media[0]['media_url'])
                new_tweet = Tweets(username, media[0]['media_url'])
                db.session.add(new_tweet)
                db.session.commit()
                if(i != len(tweets) - 1):
                    f.write("\n")


if __name__ == "__main__":
    app.run(debug=True)
