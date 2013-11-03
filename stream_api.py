from pymongo import MongoClient
import settings
from textwrap import TextWrapper
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
try:
    import simplejson as json
except:
    import json
    
    
consumer_key = settings.CONSUMER_KEY
consumer_secret = settings.CONSUMER_SECRET
access_token = settings.ACCESS_TOKEN
access_token_secret = settings.ACCESS_TOKEN_SECRET

client = MongoClient('localhost', 27017)
db = client['twitter-hack']
col = db['nyc']


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
 
    '''
    def on_status(self, status):
        # Prints the text of the tweet
        #print('Tweet text: ' + status.text)
        if status.user.geo_enabled:
            if status.coordinates:
                print 'Coordinates: ', status.coordinates
                print ('User id: ' + status.user.id_str)

        #print('ID_str: ' + status.id_str)
        #print('Tweet text: ' + status.text)
        
 
        # There are many options in the status object,
        # hashtags can be very easily accessed.
        
        for hashtag in status.entities['hashtags']:
            print(hashtag['text'])
        return True
    '''
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening

    def on_data(self, data):
        try:
            data = json.loads(data)
            text = data['text']
            print text
            col.insert(data)
            print 'load onto database'
            
        except BaseException, e:
            print 'failed on_data: %s' % str(e)


listener = StdOutListener()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
stream = Stream(auth, listener)
stream.filter(track=['nyc'])


