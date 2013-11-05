import os
from pymongo import MongoClient
import sys
import settings
from textwrap import TextWrapper
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import socket
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

sock_loc = "/tmp/twitter_socket"
if os.path.exists(sock_loc):
    os.remove(sock_loc)
s = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
s.bind(sock_loc)
print "connected to %s" % sock_loc
ne = {'lat' : 40.92285206859968, 'lon' : -73.66264343261719}
sw = {'lat' : 40.558156335842106, 'lon' : -74.27444458007812}

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
                print "inserted: %s" % text
                send_data = json.dumps(data_insert)
                send_to_socket(send_data)
                print "message sent!"
                collection.insert(data_insert)
                # send data to a tcp server interfacing with node

            
        except BaseException, e:
            print 'failed on_data: %s' % str(e)

def _check_bounds(coordinates, ne, sw):
    lon, lat = coordinates['coordinates']
    if sw[1] < lon < ne[1]:
        if sw[0] < lat < ne[0]:
            return True
    return False

def send_to_socket(data):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    client.connect(sock_loc)
    client.send(data)
    client.close()



def run(track_list):
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
     
    stream = Stream(auth, listener)
    bounding_box = [sw['lon'], sw['lat'], ne['lon'], ne['lat']]
    stream.filter(locations=bounding_box, track=track_list)

    #stream.filter(track=track_list)

if __name__ == '__main__':
    try:
        track_list = sys.argv[1:]
        run(track_list)
    except KeyboardInterrupt:
        print '\nciao for now'
        sys.exit(0)
