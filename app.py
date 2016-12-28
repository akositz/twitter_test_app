from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from users import User
from database import Database
import requests


app = Flask(__name__)
app.secret_key = '1234'

Database.initialise(database="learning", host="localhost", user="postgres", password="andi")

@app.before_request
def load_user():
    if 'screen_name' in session:
        #g is globally available! does not die off; we load it before the request
        # and is available during the entire request
        g.user = User.load_from_db_by_screen_name(session['screen_name'])

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    request_token = get_request_token()
    session['request_token']= request_token

    return redirect(get_oauth_verifier_url(request_token))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))

#how did this got activated??? --> apps.twitter.com callback url
@app.route('/auth/twitter') #http://127.0.0.1:4995/auth/twitter?oauth_verifier=123456
def twitter_auth():
    # this extracts the oauth verifier
    oauth_verifier = request.args.get('oauth_verifier') #args are the query string parameters
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_from_db_by_screen_name(access_token['screen_name'])
    if not user:
        user = User(access_token['screen_name'],access_token['oauth_token'],
                    access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile'))

@app.route('/profile') #this endpoint is associated with the profile method
def profile():
    return render_template('profile.html', user = g.user)

@app.route('/twitter-search')
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    #tweets_text =  [tweet['text'] for tweet in tweets['statuses']]
    tweets_text = [{'tweet' : tweet['text'], 'label':'neutral'} for tweet in tweets['statuses']]

    for tweet in tweets_text:
        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        request_json = r.json()
        label = request_json['label']
        tweet['label'] = label

    return render_template('search.html', content = tweets_text)

app.run(port=4995, debug=True)

