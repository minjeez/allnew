import pandas as pd
from pandas import DataFrame as df
from pymongo import MongoClient
import getRCPData as gF
import os
import json

df  = gF.NewData()
print(len(df))

client = MongoClient('mongodb://192.168.1.163:27017/')

db = client['test']
collection_name = 'RCPData'
collection = db[collection_name]

collection.insert_many(df)

client.close()