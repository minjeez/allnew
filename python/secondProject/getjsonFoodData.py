import pandas as pd
import json

# csv_data = pd.read_csv("aa_FoodData2.csv", sep = ",", low_memory=False, encoding='utf-8')
# csv_data.to_json("aa_FoodData2.json", orient = "records", force_ascii=False)

file_path = "aa_Food.json"

with open(file_path, 'r') as file:
    data = json.load(file)
    df = pd.DataFrame(data["Food"])
    new_Data = df[["type1", "name", "year", "servingsize", "unit", "kcal"]]
    set_food = new_Data.drop_duplicates(["name"], keep = 'last')
    set_food = set_food[set_food["type1"] != "가공식품"].reset_index(drop=True)
set_food = set_food[set_food["kcal"] != "-"].reset_index(drop=True)
for _ in set_food.columns:
    if (_ == 'kcal') or (_ == 'servingsize'):
        set_food = set_food.astype({ _ : 'float'}) 
        print(f'{_} 포맷')
    else:
        print(f"{_} 패스")
cnt = 0
for i in set_food["unit"]:
    if i == "g" or i == "mL":
        score = set_food.loc[cnt, "servingsize"]
        score_change = 100 / score
        kal = set_food.loc[cnt,"kcal"]
        ser = set_food.loc[cnt,"servingsize"]
        
        set_food.loc[cnt,"kcal"] = kal * score_change
        set_food.loc[cnt,"servingsize"] = ser * score_change
    else:
        pass
    cnt += 1
set_food = set_food.round()
set_food = set_food.astype({ "servingsize" : 'int'})
for _ in range(len(set_food.index)):
    set_food["1회제공량"] = str(set_food["servingsize"][_]) + str(set_food["unit"][_])

set_food["1회제공량"]
set_food.drop(["servingsize","unit"], axis= 1, inplace=True)

output_data = {"food": set_food.to_dict(orient="records")}

with open("modified_aa_FoodData.json", 'w') as file:
    json.dump(output_data, file, ensure_ascii=False)

# json-server --watch ./aa_Food.json --host 0.0.0.0 --port 5000
# http://192.168.1.163:5000/Food