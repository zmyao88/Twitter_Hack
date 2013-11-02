
from textwrap import TextWrapper
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
    
    
consumer_key="lGVfc9ALaWkeY55VwGvpQA"
consumer_secret="RHEWdk7wA6l3lJ8AhItHWBXaYguGMLVrPY1LwlOo"
  
access_token="2165970216-GKF2JmKsvI7Q7VmNJxyRxXQw3aGaoQDDbgrxIvm"
access_token_secret="20QVGgYKKskM2VlPYyJTxTNIanxIFc8gFBlVRSF3lAicw"


class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''
 
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
 
    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening


listener = StdOutListener()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
stream = Stream(auth, listener)
stream.filter(track=['party','#party'])







