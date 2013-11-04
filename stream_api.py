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
collection = db['nyc']


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening

    def on_data(self, data):
        try:
            data = json.loads(data)
            if data['user']['geo_enabled'] and data['coordinates']:
                coor = data['coordinates']
                text = data['text']
                user = data['user']
                data_insert = {
                    'coordinates' : coor,
                    'text' : text,
                    'user' : user
                }
                #check if it's in nyc bound
                ne = [40.92285206859968, -73.66264343261719]
                sw = [40.558156335842106, -74.27444458007812]
                if _check_bounds(coor, ne, sw):
                    collection.insert(data_insert)
                    print "inserted: %s" % text
                    # send data to a tcp server interfacing with node

            
        except BaseException, e:
            print 'failed on_data: %s' % str(e)

def _check_bounds(coordinates, ne, sw):
    lon, lat = coordinates['coordinates']
    if sw[1] < lon < ne[1]:
        if sw[0] < lat < ne[0]:
            return True
    return False
    

listener = StdOutListener()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
stream = Stream(auth, listener)
track_list = ['NYC']        
try:
    stream.filter(track=track_list)
except KeyboardInterrupt:
    print 'Interupted'


