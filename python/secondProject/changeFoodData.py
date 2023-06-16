import json 
import pandas as pd
from pandas import DataFrame as df
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.163:27017/')
# 디비 연결
db = client['test']
collection_name = 'FoodData'
collection = db[collection_name]
myframe = collection.find({})

df = pd.DataFrame(list(myframe))
# print(df)

newdf = df.drop(['_id', 'ANIMAL_PLANT'], axis=1)
# print(newdf)

mycolumn = ['식품이름','1회제공량','열량','탄수화물','단백질','지방','당류','나트륨','콜레스테롤','포화지방산','트랜스지방산','연도']
newdf.columns = mycolumn
# print(newdf)

food_update = newdf[(newdf["1회제공량"] != "0")]
# print(food_update)
reset_food = food_update.reset_index(drop=True)
# print(reset_food)

set_food = reset_food.drop_duplicates(["식품이름"], keep = 'last')
new_set_food = set_food.reset_index(drop=True)
new_set_food = new_set_food.replace('N/A', 0)
# print(len(food_update))
# print(len(reset_food))
# print(len(set_food))
# print(new_set_food.info())

for _ in new_set_food.columns:
  if (_ == '연도') or (_ == '식품이름'): 
      print(f'{_}는 포맷을 안합니다')
  else:
    new_set_food = new_set_food.astype({ _ : 'float'})
    print(f'{_} 포맷')
# print(new_set_food.info())

cnt = 0
for i in new_set_food["1회제공량"]:
  if i == 100.0:
    cnt += 1
  else:
    change = 100 / i

    kal = new_set_food.loc[cnt,"열량"] 
    carbohy = new_set_food.loc[cnt,"탄수화물"]
    protein = new_set_food.loc[cnt,"단백질"] 
    fat = new_set_food.loc[cnt,"지방"] 
    suars = new_set_food.loc[cnt,"당류"] 
    na = new_set_food.loc[cnt,"나트륨"] 
    col = new_set_food.loc[cnt,"콜레스테롤"] 
    poh = new_set_food.loc[cnt,"포화지방산"] 
    trans = new_set_food.loc[cnt,"트랜스지방산"] 

    new_set_food.loc[cnt,"열량"] = kal * change
    new_set_food.loc[cnt,"탄수화물"] = carbohy * change
    new_set_food.loc[cnt,"단백질"] = protein * change
    new_set_food.loc[cnt,"지방"] = fat * change
    new_set_food.loc[cnt,"당류"] = suars * change
    new_set_food.loc[cnt,"나트륨"] = na * change
    new_set_food.loc[cnt,"콜레스테롤"] = col * change
    new_set_food.loc[cnt,"포화지방산"] = poh * change
    new_set_food.loc[cnt,"트랜스지방산"] = trans * change
    new_set_food.loc[cnt,"1회제공량"] = i * change
    
    print(f'{cnt} 완료')
    cnt += 1
new_set_food1 = new_set_food.round()
print(new_set_food1)

sample_data = new_set_food1.copy()
sample_data["횟수"] = [len(str(sample_data["식품이름"].iloc[i]).split(",")) for i in range(len(sample_data))]
sample_data["식품이름"] = [str(sample_data["식품이름"].iloc[i]).split(",") for i in range(len(sample_data))]
sample_data_1 = sample_data[sample_data["횟수"] == 1].reset_index(drop=True)
sample_data_2 = sample_data[sample_data["횟수"] == 2].reset_index(drop=True)
sample_data_3 = sample_data[sample_data["횟수"] == 3].reset_index(drop=True)

cnt = 0 
for _ in sample_data_1["식품이름"]:
    print(_[0])
    sample_data_1.loc[cnt, "식품이름"] = _[0]
    cnt += 1
sample_data_1

sample_list = []
sample_set = []
for i in sample_data_2["식품이름"]:
    if i[1] in sample_list:
      # print(i[1])
      sample_set.append(i[1])
    else:
      sample_list.append(i[1])

print(set(sample_set))

sample_list = []
sample_set = []
for i in sample_data_2["식품이름"]:
    if i[1] in sample_list:
      # print(i[1])
      sample_set.append(i[1])
    else:
      sample_list.append(i[1])

print(set(sample_set))

set_list = list(set(sample_set))

sample_1 = []
sample_3 = []
sample_2 = []
cnt1 = 0
cnt2 = 0
for i in sample_data_2["식품이름"]:
    if i[1] in set_list:
      sample_1.append(i[1])
      sample_3.append(i[0])
      cnt1 += 1
    else:
      sample_2.append(i[1])
      cnt2 += 1

cnt = 0 
for i in sample_data_2["식품이름"]:
  # print(i[1])
  if i[1] in set_list:
    # print(i[1])
    sample_data_2.loc[cnt, "식품이름"] = i[0]
    sample_data_2.loc[cnt, "종류"] = i[1]
    cnt += 1
  else:
    sample_data_2.loc[cnt, "식품이름"] = i[1]
    sample_data_2.loc[cnt, "종류"] = i[0]
    cnt += 1
print(sample_data_2)

# 식품의 [1] 번째 애들의 전처리 과정이다 

a = sample_data_2.drop_duplicates(["종류"], keep = 'last')
for _ in a["종류"].values:
  print(_)

drop_list = ["통곡물로든든한아침을만들면", "1", "베지밀칼슘가득두유검은깨", "미스터칩스치즈맛콘칩(옥수수66.49%", '허니앤아몬드쇼트브레드(꿀4%', "노리마끼치즈(김2.06%", "켄돈2컬러(오렌지, 탕고와퍼렌야초콜릿(코코아분말5%", "크롤리푸드버터크림초콜릿크레커(코코아분말3%", "피쉬크래커카라멜(실꼬리돔40%", "피쉬크래커커틀피쉬(실꼬리돔40%"]
revers_list = ["도우넛", "된장", "곤약", "딸기맛요구르트", "삼각김밥", "너구리", "스파게티"]

cnt = 0
bin_list = ""
for _ in sample_data_2["종류"]:
  if _ in drop_list:
    sample_data_2 = sample_data_2[sample_data_2["종류"] != _]
    cnt += 1
  elif _ in revers_list:
    sample_data_2.loc[cnt, "종류"] = sample_data_2.loc[cnt, "식품이름"]
    sample_data_2.loc[cnt, "식품이름"] = _
    cnt += 1
  else:
    cnt += 1
    
print(sample_data_2)
# 식품의 [1] 번째 애들의 전처리 보완

# sample_list = []
# sample_set = []
# for i in sample_data_3["식품이름"]:
#     if i[0] in sample_list:
#       sample_set.append(i[0])
#     else:
#       sample_list.append(i[0])
      
# sample_list = []
# sample_set = []
# for i in sample_data_3["식품이름"]:
#     if i[1] in sample_list:
#       sample_set.append(i[1])
#     else:
#       sample_list.append(i[1])
      
# sample_list = []
# sample_set = []
# for i in sample_data_3["식품이름"]:
#     if i[2] in sample_list:
#       sample_set.append(i[2])
#     else:
#       sample_list.append(i[2])
      
# print(set(sample_set))

f_list = ['피자', '샌드위치']
cnt = 0
for i in sample_data_3["식품이름"]:
  if i in f_list:
    sample_data_3 = sample_data_3[sample_data_3["식품이름"] != _]
    cnt += 1
  else:
    sample_data_3.loc[cnt, "종류"] = i[1]
    sample_data_3.loc[cnt, "식품이름"] = i[0]
    cnt += 1
print(sample_data_3)

sample_data_1["종류"] = ""
new_data = pd.concat([sample_data_1, sample_data_2, sample_data_3], axis = 0)
print(new_data)