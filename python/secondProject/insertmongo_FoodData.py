import pandas as pd
from pymongo import MongoClient
import getFoodData as gF
import os
import json

def firstStep():
    df = gF.NewData()
    client = MongoClient('mongodb://192.168.1.163:27017/')
    db = client['test']
    collection_name = 'FoodData'
    collection = db[collection_name]
    collection.insert_many(df)
    client.close()
    print('completed')

firstStep()