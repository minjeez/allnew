import json 
import pandas as pd
from pandas import DataFrame as df
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://192.168.1.163:27017/')
# DB 연결
db = client['test']
collection_name = 'FoodData'
collection = db[collection_name]
myframe = collection.find({})

# df = pd.DataFrame(list(myframe))
# print(df)

def first_process(myframe):
    df = pd.DataFrame(list(myframe))
    newdf = df.drop(['_id', 'ANIMAL_PLANT'], axis=1)

    mycolumn = ['식품이름','1회제공량','열량','탄수화물','단백질','지방','당류','나트륨','콜레스테롤','포화지방산','트랜스지방산','연도']
    newdf.columns = mycolumn

    food_update = newdf[(newdf["1회제공량"] != "0")]
    reset_food = food_update.reset_index(drop=True)

    set_food = reset_food.drop_duplicates(["식품이름"], keep = 'last')
    new_set_food = set_food.reset_index(drop=True)
    new_set_food = new_set_food.replace('N/A', 0)
    return new_set_food
    

    
def format_process(format_data):
    for _ in format_data.columns:
      if (_ == '연도') or (_ == '식품이름'): 
          print(f'{_}는 포맷을 안합니다')
      else:
        format_data = format_data.astype({ _ : 'float'})
        print(f'{_} 포맷')


    cnt = 0
    for i in format_data["1회제공량"]:
      if i == 100.0:
        cnt += 1
      else:
        change = 100 / i

        kal = format_data.loc[cnt,"열량"] 
        carbohy = format_data.loc[cnt,"탄수화물"]
        protein = format_data.loc[cnt,"단백질"] 
        fat = format_data.loc[cnt,"지방"] 
        suars = format_data.loc[cnt,"당류"] 
        na = format_data.loc[cnt,"나트륨"] 
        col = format_data.loc[cnt,"콜레스테롤"] 
        poh = format_data.loc[cnt,"포화지방산"] 
        trans = format_data.loc[cnt,"트랜스지방산"] 

        format_data.loc[cnt,"열량"] = kal * change
        format_data.loc[cnt,"탄수화물"] = carbohy * change
        format_data.loc[cnt,"단백질"] = protein * change
        format_data.loc[cnt,"지방"] = fat * change
        format_data.loc[cnt,"당류"] = suars * change
        format_data.loc[cnt,"나트륨"] = na * change
        format_data.loc[cnt,"콜레스테롤"] = col * change
        format_data.loc[cnt,"포화지방산"] = poh * change
        format_data.loc[cnt,"트랜스지방산"] = trans * change
        format_data.loc[cnt,"1회제공량"] = i * change
        
        cnt += 1
    new_set_food1 = format_data.round()
    return new_set_food1


def final_process(final_data):
    sample_data = final_data.copy()
    sample_data["횟수"] = [len(str(sample_data["식품이름"].iloc[i]).split(",")) for i in range(len(sample_data))]
    sample_data["식품이름"] = [str(sample_data["식품이름"].iloc[i]).split(",") for i in range(len(sample_data))]
    sample_data_1 = sample_data[sample_data["횟수"] == 1].reset_index(drop=True)
    sample_data_2 = sample_data[sample_data["횟수"] == 2].reset_index(drop=True)
    sample_data_3 = sample_data[sample_data["횟수"] == 3].reset_index(drop=True)

    cnt = 0 
    for _ in sample_data_1["식품이름"]:
        sample_data_1.loc[cnt, "식품이름"] = _[0]
        cnt += 1

    sample_list = []
    sample_set = []
    for i in sample_data_2["식품이름"]:
        if i[1] in sample_list:
          sample_set.append(i[1])
        else:
          sample_list.append(i[1])
    
    ## 중복 확인
    set_list = list(set(sample_set))

    cnt = 0 
    for i in sample_data_2["식품이름"]:
      if i[1] in set_list:
        sample_data_2.loc[cnt, "식품이름"] = i[0]
        sample_data_2.loc[cnt, "종류"] = i[1]
        cnt += 1
      else:
        sample_data_2.loc[cnt, "식품이름"] = i[1]
        sample_data_2.loc[cnt, "종류"] = i[0]
        cnt += 1

  ## 보류

    drop_list = ["통곡물로든든한아침을만들면", "1", "베지밀칼슘가득두유검은깨", "미스터칩스치즈맛콘칩(옥수수66.49%", '허니앤아몬드쇼트브레드(꿀4%', "노리마끼치즈(김2.06%", "켄돈2컬러(오렌지, 탕고와퍼렌야초콜릿(코코아분말5%", "크롤리푸드버터크림초콜릿크레커(코코아분말3%", "피쉬크래커카라멜(실꼬리돔40%", "피쉬크래커커틀피쉬(실꼬리돔40%"]
    revers_list = ["도우넛", "된장", "곤약", "딸기맛요구르트", "삼각김밥", "너구리", "스파게티"]

    cnt = 0
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

    sample_data_1["종류"] = ""
    new_data = pd.concat([sample_data_1, sample_data_2, sample_data_3], axis = 0).reset_index(drop=True)
    return new_data

# format_data = first_process(myframe)
# final_data = format_process(format_data)
# final_data = final_process(final_data)
# print(final_data)