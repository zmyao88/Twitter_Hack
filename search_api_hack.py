import tweepy

consumer_key = "MurYU2jKrMBklyckfWS1pw"
consumer_secrect = "0ZwYrtdoqBKcEuK6IGk1hzpxko0WLyuYN5YVMfOaiKc"
access_token = "2165970216-NmrpEF0nrr6ZMynfSNts5D7dFdl7uFbF7UFVrJx"
access_secrect = "yhd9XYV54e4T0EYZeho1NQylT1nCpTZM9RhQwc9CHPqlv"


auth = tweepy.OAuthHandler(consumer_key, consumer_secrect)
auth.set_access_token(access_token, access_secrect)


api = tweepy.API(auth)
user = api.get_user("twitter")

TWITTER_PAGESIZE = 100
USER_QUERY = "halloween party"
current_page = 200

results = api.search(q=USER_QUERY, count=current_page,
 rpp = TWITTER_PAGESIZE)