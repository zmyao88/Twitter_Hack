import settings
import tweepy

consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
access_token_secret = settings.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(consumer_key, consumer_secrect)
auth.set_access_token(access_token, access_secrect)


api = tweepy.API(auth)
user = api.get_user("twitter")

TWITTER_PAGESIZE = 100
USER_QUERY = "halloween party"
current_page = 200

results = api.search(q=USER_QUERY, count=current_page,
 rpp=TWITTER_PAGESIZE)
