import pandas as pd
from pandas import DataFrame as df
from pymongo import MongoClient
import def_changeFoodData as cF
import os
import json

def secondStep():
    client = MongoClient('mongodb://192.168.1.163:27017/')
    db = client['test']
    collection_name = 'FoodData'
    collection = db[collection_name]
    myframe = collection.find({})

    format_data = cF.first_process(myframe)
    final_data = cF.format_process(format_data)
    new_final_data = cF.final_process(final_data)

    new_final_data.reset_index(inplace=True)
    data_dict = new_final_data.to_dict("records")
    collection_name = 'procFoodData'
    collection = db[collection_name]
    collection.insert_many(data_dict)

    client.close()
    print('completed again')