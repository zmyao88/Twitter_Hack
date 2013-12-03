import nltk
from pymongo import MongoClient
import re
import time
import codecs

client = MongoClient('localhost', 27017)                                       
db = client['twitter-hack']                                                    
collection = db['nyc']  


def get_mongo_data(collection):
    my_data = [rec['text'] for rec in collection.find()]
    return my_data

def processor(data):
    try:
        tokenized = nltk.word_tokenize(data)
        tagged = nltk.pos_tag(tokenized)
        name_ent = nltk.ne_chunk(tagged, binary=True)
        
        #entities = re.findall(r'NE')
        print name_ent

    except Exception, e:
        print 'Failed in the try of processor'
        print str(e)




twi_data = get_mongo_data(collection)

for twt in twi_data:
#    text = twt.encode
    print type(twt)    
    processor(twt)
    time.sleep(1)
