from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['twitter-hack']
my_collection = db.nyc

#try find one record
my_collection.find_one()

for rec in my_collection.find():
    print rec
