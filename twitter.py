from tweepy import *
import simplejson as json

ACCESS_TOKEN = '745585523364814848-IHVzTunccCuHXmFlcrtEd61Xs8wPyG1'
ACCESS_SECRET = 'Jyi2LqbMluaW5k1q2yOTIb3jT28fXlU22fNkF2bBLG5UM'
CONSUMER_KEY = 'RC10RuLHntJNmjTG73h71q4T6'
CONSUMER_SECRET = 'G1uopnA6VNqpA1mx4C8qtPRFah2CKri4EIBNqUBjlFoJDT4zy8'


def takename(keywords, since, cnt=200):
  # S = SListener()
  complete_dict = {}
oauth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = API(oauth)
tweets = api.search(q=keywords, lang='en', count=cnt, since_id = since)
tweet_list = []
for tweet in tweets:
  tweet_dict = {}
  tweet_dict["timestamp"] = tweet.created_at
  tweet_dict["text"] = tweet.text
  tweet_dict["retweet_count"] = tweet.retweet_count
  tweet_list.append(tweet_dict)
  complete_dict["keyword"] = keywords




    file1.write((str)(tweet))
    file1.write("\n")
