from konlpy.tag import Hannanum
from konlpy.utils import pprint
import def_changeRCPData as dCRCP
import def_changeFoodData as dCFOOD
import re
import json 
import pandas as pd
import pymongo
from pymongo import MongoClient

# DB Connect
client = MongoClient('mongodb://192.168.1.163:27017/')
db = client['test']
collection_name = 'RCPData'
collection = db[collection_name]
myframe = collection.find({})
# all words of RCP Data
have_n, no_n = dCRCP.have_n_non(myframe)
content1 = dCRCP.regular_repeat_remove(have_n)

collection_name = 'FoodData'
collection = db[collection_name]
myframe = collection.find({})
# all words of Food Data
format_data = dCFOOD.first_process(myframe)
final_data = dCFOOD.format_process(format_data)
content2 = dCFOOD.final_process(final_data)
food_list = []
for i in content2["식품이름"]:
    food_list.append(i)

# Extract ingredients from RCP Data and compare with Food Data
hannanum = Hannanum()
words1 = hannanum.nouns(content1[0])
print(words1)
a = []
b = []
for i in words1:
    if i in food_list:
        a.append(i)
    else:
        b.append(i)

print(f"매칭 되는 재료 : {a}")
print(f"매칭 안되는 재료 : {b}")

# Putting matched ingredients in bin_FoodData.json
df = pd.DataFrame(a , columns = ["재료"])
print(df)
df = df.to_dict("records")

with open('bin_FoodData.json', 'w') as f:
    json.dump(df, f, ensure_ascii=False) 