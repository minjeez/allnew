import pandas as pd
from pandas import DataFrame as df
from pymongo import MongoClient
import os
import json

foods_csv_data = pd.read_csv("fooddata.csv", sep = ",", low_memory=False, encoding='utf-8')
foods_data_dict = foods_csv_data.to_dict(orient="records")
foods_dict = {"Food" : foods_data_dict}
    
df = pd.DataFrame(foods_dict["Food"])

new_Data = df[["DB군", "식품명", "연도", "1회제공량", "내용량_단위", "에너지(㎉)"]]
new_Data = new_Data.sort_values("연도")
set_food = new_Data.drop_duplicates(["식품명"], keep = 'last')
set_food = set_food[set_food["DB군"] != "가공식품"].reset_index(drop=True)
set_food = set_food[set_food["에너지(㎉)"] != "-"].reset_index(drop=True)

for _ in set_food.columns:
    if (_ == '에너지(㎉)') or (_ == '1회제공량'):
        set_food = set_food.astype({ _ : 'float'}) 
        print(f'{_} 포맷')
    else:
        print(f"{_} 패스")
        
cnt = 0
for i in set_food["내용량_단위"]:
    if i == "g" or i == "mL":
        score = set_food.loc[cnt, "1회제공량"]
        score_change = 100 / score
        kal = set_food.loc[cnt,"에너지(㎉)"]
        ser = set_food.loc[cnt,"1회제공량"]
        
        set_food.loc[cnt,"에너지(㎉)"] = kal * score_change
        set_food.loc[cnt,"1회제공량"] = ser * score_change
    else:
        pass
    cnt += 1
set_food = set_food.round()
set_food = set_food.astype({ "1회제공량" : 'int'})

set_food["1회제공량"]
set_food.drop(["1회제공량","내용량_단위"], axis= 1, inplace=True)

set_food = set_food.rename(columns={"DB군": "종류", "식품명": "식품이름", "연도": "연도", "에너지(㎉)": "열량"})
set_food.drop(["종류", "연도"], axis= 1, inplace=True)
print(set_food)

set_foods = set_food.to_dict(orient="records")
foods_dict = {"Food" : set_foods}
with open('foods.json', 'w') as f:
     json.dump(foods_dict, f, ensure_ascii=False)

# json-server --watch ./modified_aa_FoodData.json --host 0.0.0.0 --port 5000
# http://192.168.1.78:5000/Food
# json-server 에 너무 큰 용량의 파일 띄우지 않기로함. 따라서 foods.json을 mosngodb에 넣기로함.

foods = set_food.to_dict("records")
client = MongoClient('mongodb://192.168.1.163:27017/')

db = client['test']
collection_name = 'FoodData'
collection = db[collection_name]

collection.insert_many(foods)

client.close()