import json, datetime
import requests
import os.path
import pandas as pd 
import re
import new_getFoodData as gF
from konlpy.tag import Hannanum
from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.request

hannanum = Hannanum()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

def getRequestUrl(url):
    res = requests.get(url)
    try:
        if res.status_code == 200:
            return res
    except Exception as e:
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def getRCPData(startIdx, endIdx, RCP_NM):
    end_point = 'http://openapi.foodsafetykorea.go.kr'
    parameters = ''
    parameters += "/api/" + get_secret("data_apiKey2") + "/COOKRCP01/json"
    parameters += "/" + str(startIdx)
    parameters += "/" + str(endIdx)
    parameters += "/RCP_NM=" + str(RCP_NM)
    url = end_point + parameters
    res = getRequestUrl(url)
    if (res == None):
        return None
    else:
        dict_json = json.loads(res.text)
        return dict_json
    
def first_search_RCP(RCP_NM):
    jsonResult = []
    startIdx = 1
    endIdx = 10
    RCP_Information = getRCPData(startIdx, endIdx, RCP_NM)
    if RCP_Information["COOKRCP01"]["RESULT"]["MSG"] == "해당하는 데이터가 없습니다.":
        food = {f"{RCP_NM} 종류" : [RCP_NM]}
    else:
        jsonResult.append(RCP_Information['COOKRCP01']['row'])
        foods = pd.DataFrame.from_dict(jsonResult[0]).T
        food = foods.loc["RCP_NM", : ]
        food = {f"{RCP_NM} 종류" : list(food)}
    return food

def search_RCP(RCP_NM):
    cnt = 0
    jsonResult = []
    startIdx = 1
    endIdx = 10
    RCP_Information = getRCPData(startIdx, endIdx, RCP_NM)
    if RCP_Information["COOKRCP01"]["RESULT"]["MSG"] == "해당하는 데이터가 없습니다.":
        cnt = 0
        print("관련데이터가 없습니다.")
    else:
        jsonResult.append(RCP_Information['COOKRCP01']['row'])
        cnt = 1   
        
    foods = pd.DataFrame.from_dict(jsonResult[0]).T
    return foods

def DataProcess(RCP_NM):
    df = search_RCP(RCP_NM)
    RCP_vale = df.loc["RCP_PARTS_DTLS"].values
    words = hannanum.nouns(RCP_vale[0])
    # print(type(words))
    food = {"형태소" : words}
    return food

def Regex(RCP_NM):
    words = DataProcess(RCP_NM)
    food_list = []
    for word in words["형태소"]:
        new_str = re.sub(r"[^\uAC00-\uD7A3]", "", word)
        food_list.append(new_str)
    food_list = {"정규화" : food_list}
    return food_list

def BinMatch(RCP_NM):
    with open('bin_FoodData.json', 'r') as f:
        son_data = json.load(f)
    try:
        food_list = []
        cnt = 0
        while True:
            food_list.append(son_data["Food"][cnt]['재료'])
            cnt +=1
    except:
        pass
    ReGex_list = Regex(RCP_NM)

    show_list = []
    nomtach_list  = []
    for i in ReGex_list['정규화']:
        if i in food_list: 
            show_list.append(i)
        else:
            nomtach_list.append(i)
    
    show_list = {"매치완료" : show_list}
    nomtach_list = {"매치실패" : nomtach_list}
    new_list = {"구분" : [show_list, nomtach_list]}
    return new_list    
          
def FoodDBMatchFood(RCP_NM):
    client = MongoClient('mongodb://192.168.1.78:27017/')
    db = client['test']
    collection_name = 'FoodData'
    collection = db[collection_name]
    myframe = collection.find({},{"식품이름"})
    myframe_list = []
    for _ in myframe:
        myframe_list.append(_["식품이름"])
    new_list = BinMatch(RCP_NM)
    show_list = []
    nomtach_list  = []
    for i in new_list['구분'][1]["매치실패"]:
        if i in myframe_list: 
            show_list.append(i)
        else:
            nomtach_list.append(i)
    
    # Putting matched ingredients in bin_FoodData.json
    with open('bin_FoodData.json', 'r') as f:
        existing_data = json.load(f)
        # print(existing_data)
    df = pd.DataFrame(show_list , columns = ["재료"])
    df = df.to_dict("records")
    df += existing_data["Food"]
    new_df = {"Food" : df}
    with open('bin_FoodData.json', 'w') as f:
        json.dump(new_df, f, ensure_ascii=False)
    
    show_list = {"매치완료" : show_list}
    nomtach_list = {"매치실패" : nomtach_list}
    new_lsit = {"구분" : [show_list, nomtach_list]}
    return new_lsit

def trashMatch(RCP_NM):
    with open('Trash.json', 'r') as f:
        son_data = json.load(f)
    try:
        trash_list = []
        cnt = 0
        while True:
            trash_list.append(son_data["trash"][cnt]['값'])
            cnt +=1
    except:
        pass
    new_lsit = FoodDBMatchFood(RCP_NM)
    show_list = []
    nomtach_list  = []
    for i in new_lsit['구분'][1]["매치실패"]:
        if i in trash_list: 
            nomtach_list.append(i)
        else:
            show_list.append(i)
    show_list = {"매치완료" : show_list}
    nomtach_list = {"쓰레기처리" : nomtach_list}
    new_lsit = {"구분" : [show_list, nomtach_list]}
    return new_lsit

def singo(RCP_NM, *args):
    try:
        new_lsit_1 = BinMatch(RCP_NM)
        new_lsit_2 = FoodDBMatchFood(RCP_NM)
        new_lsit_3 = trashMatch(RCP_NM)
        last_list = new_lsit_1['구분'][0]["매치완료"] + new_lsit_2['구분'][0]["매치완료"] + new_lsit_3['구분'][0]["매치완료"]
        args_list = []
        singo_lists = []
        for arg in args:
            args_list.append(arg)
        for last in args_list[0]:
            if last in last_list:
                last_list.remove(last)
                singo_lists.append(last)
            else:
                pass
        with open('Trash.json', 'r') as f:
            existing_data = json.load(f)
        df = pd.DataFrame(args_list[0] , columns = ["값"])
        df = df.to_dict("records")
        df += existing_data["trash"]   
        new_df = {"trash" : df}
        with open('Trash.json', 'w') as f:
            json.dump(new_df, f, ensure_ascii=False)
        
        last_list = {"신고완료후값" : last_list}
        singo_lists = {"신고완료" : singo_lists}
        new_list = {"신고구분" : [last_list, singo_lists]}
        return new_list
    except:
        last_list = clolingDF(RCP_NM)
        args_list = []
        singo_lists = []
        for arg in args:
            args_list.append(arg)
        for last in args_list[0]:
            if last in last_list["재료 리스트"]:
                last_list["재료 리스트"].remove(last)
                singo_lists.append(last)
            else:
                pass
        with open('Trash.json', 'r') as f:
            existing_data = json.load(f)
        df = pd.DataFrame(args_list[0] , columns = ["값"])
        df = df.to_dict("records")
        df += existing_data["trash"]   
        new_df = {"trash" : df}
        with open('Trash.json', 'w') as f:
            json.dump(new_df, f, ensure_ascii=False)
        last_list = {"신고완료후값" : last_list["재료 리스트"]}
        singo_lists = {"신고완료" : singo_lists}
        new_list = {"신고구분" : [last_list, singo_lists]}
        return new_list

def showRCP(RCP_NM):
    foods = search_RCP(RCP_NM)
    foodname = foods[foods.index == "RCP_NM"][0].values
    # print(foodname[0])

    manual_list = []
    for manual in foods.index:
        if "MANUAL" in manual and "IMG" not in manual:
            foodmanual = foods[foods.index == manual].values
            if len(foodmanual[0][0]) > 0:
                manual_list.append(foodmanual[0][0])
            
    manual_list = sorted(manual_list)
    cnt = 0
    for n in manual_list:
        manual_list[cnt] = n.replace('\n', '')
        cnt += 1
    new_list = { "레시피" : [{"음식이름" : foodname[0]} , {"메뉴얼" : manual_list}]}
    return new_list

def foodListCkeck(RCP_NM, sing_list, *args):
    try:
        new_lsit_1 = BinMatch(RCP_NM)
        new_lsit_2 = FoodDBMatchFood(RCP_NM)
        new_lsit_3 = trashMatch(RCP_NM)
        last_list = new_lsit_1['구분'][0]["매치완료"] + new_lsit_2['구분'][0]["매치완료"] + new_lsit_3['구분'][0]["매치완료"] 
            
        guma_list = [] #구매를 해야되는 리스트
        
        args_list = [] #냉장고 물건을 체크를 한애
        
        a_trashmatch_list = []
        
        for arg in args:
            args_list.append(arg)
            
        if len(sing_list) > 0: 
            for lee in new_lsit_3['구분'][0]["매치완료"]:
                if lee in sing_list:
                    a_trashmatch_list.append(lee)
                else:
                    pass
            for sing in sing_list:
                if sing in args_list[0]:
                    pass
                else:
                    guma_list.append(sing)
                    
            with open('bin_FoodData.json', 'r') as f:
                existing_data = json.load(f)

            df = pd.DataFrame(a_trashmatch_list , columns = ["재료"])
            df = df.to_dict("records")
            df += existing_data["Food"]
            new_df = {"Food" : df}
            with open('bin_FoodData.json', 'w') as f:
                json.dump(new_df, f, ensure_ascii=False)        
            
        else:  
            for last in last_list:
                if last in args_list[0]:
                    pass
                else:
                    guma_list.append(last)  
            with open('bin_FoodData.json', 'r') as f:
                existing_data = json.load(f)

            df = pd.DataFrame(new_lsit_3['구분'][0]["매치완료"]  , columns = ["재료"])
            df = df.to_dict("records")
            df += existing_data["Food"]
            new_df = {"Food" : df}
            with open('bin_FoodData.json', 'w') as f:
                json.dump(new_df, f, ensure_ascii=False)        
        
        
        guma_list = {"구매리스트" : guma_list}
        new_list= showRCP(RCP_NM)
        
        all_list = {"종합" :[guma_list, new_list["레시피"][0] , new_list["레시피"][1]]}
        return all_list
    except:
        clo = cloling(RCP_NM)
        last_list = clo["구분"][1]["재료"]
        
        guma_list = [] #구매를 해야되는 리스트
        
        args_list = [] #냉장고 물건을 체크를 한애
        
        a_trashmatch_list = []
        
        for arg in args:
            args_list.append(arg)
        if len(sing_list) > 0: 
            for lee in last_list:
                if lee in sing_list:
                    a_trashmatch_list.append(lee)
                else:
                    pass
            for sing in sing_list:
                if sing in args_list[0]:
                    pass
                else:
                    guma_list.append(sing) 
                    
            with open('bin_FoodData.json', 'r') as f:
                existing_data = json.load(f)

            df = pd.DataFrame(a_trashmatch_list , columns = ["재료"])
            print(1)
            df = df.to_dict("records")
            print(1)
            df += existing_data["Food"]
            print(1)
            new_df = {"Food" : df}
            with open('bin_FoodData.json', 'w') as f:
                json.dump(new_df, f, ensure_ascii=False)  
            
        else:  
            for last in last_list:
                if last in args_list[0]:
                    pass
                else:
                    guma_list.append(last)  
            with open('bin_FoodData.json', 'r') as f:
                existing_data = json.load(f)    
            df = pd.DataFrame(clo["구분"][1]["재료"] , columns = ["재료"])

            df = df.to_dict("records")
            df += existing_data["Food"]
            new_df = {"Food" : df}
            with open('bin_FoodData.json', 'w') as f:
                json.dump(new_df, f, ensure_ascii=False)  
                      
        guma_list = {"구매리스트" : guma_list}
        RCP_list = { '메뉴얼' :  clo["구분"][2]['레시피']}
        RPC_name = {"음식이름" : RCP_NM}
        all_list = {"종합" :[guma_list, RPC_name , RCP_list]}
        return all_list
            
def search_all(RCP_NM):
    try:
        new_lsit_1 = BinMatch(RCP_NM)
        new_lsit_2 = FoodDBMatchFood(RCP_NM)
        new_lsit_3 = trashMatch(RCP_NM)
        last_list = new_lsit_1['구분'][0]["매치완료"] + new_lsit_2['구분'][0]["매치완료"] + new_lsit_3['구분'][0]["매치완료"] 
        
        last_list = {"재료 리스트" : last_list}
        return last_list
    except:
        last_list = clolingDF(RCP_NM)
        return last_list

def clolingDF(RCP_NM):
    url_name = quote(RCP_NM)
    url = 'https://www.10000recipe.com/recipe/list.html?q=' + url_name
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    links = soup.find('a', class_='common_sp_link')["href"]
    new_ulr = 'https://www.10000recipe.com' + links 
    new_sourcecode = urllib.request.urlopen(new_ulr).read()
    soup = BeautifulSoup(new_sourcecode, "html.parser")
    div = soup.find('div', attrs={'class': "ready_ingre3"})
    food = div.text
    food = food.split("\n")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    a_list = []
    for f in food:
        f = f.replace(" ", "")
        if (f == ""):
            pass
        else:
            a_list.append(f)
              
    with open('Trash.json', 'r') as f:
        son_data = json.load(f)
    try:
        trash_list = []
        cnt = 0
        while True:
            trash_list.append(son_data["trash"][cnt]['값'])
            cnt +=1
    except:
        pass
    show_list = []
    non_list = []
    for _ in a_list:
        if (_ in trash_list) or ( _.isalpha() == False):
            non_list.append(_)
        else:
            show_list.append(_)

    cloling_food = {"재료 리스트" : show_list}
    
    return cloling_food

def cloling(RCP_NM):
    url_name = quote(RCP_NM)
    url = 'https://www.10000recipe.com/recipe/list.html?q=' + url_name
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    links = soup.find('a', class_='common_sp_link')["href"]
    new_ulr = 'https://www.10000recipe.com' + links 
    new_sourcecode = urllib.request.urlopen(new_ulr).read()
    soup = BeautifulSoup(new_sourcecode, "html.parser")
    div = soup.find('div', attrs={'class': "ready_ingre3"})
    food = div.text
    food = food.split("\n")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    a_list = []
    for f in food:
        f = f.replace(" ", "")
        if (f == ""):
            pass
        else:
            a_list.append(f)
    try:
        cnt = 0
        stepdescr_list = []
        while True:
            div = soup.find('div', attrs={'id': f"stepdescr{cnt+1}"}).text
            stepdescr_list.append(f"{cnt+1}. {div}")
            cnt += 1
    except:
        pass
    
    with open('Trash.json', 'r') as f:
        son_data = json.load(f)
    try:
        trash_list = []
        cnt = 0
        while True:
            trash_list.append(son_data["trash"][cnt]['값'])
            cnt +=1
    except:
        pass
    show_list = []
    non_list = []
    for _ in a_list:
        if (_ in trash_list) or ( _.isalpha() == False):
            non_list.append(_)
        else:
            show_list.append(_)

    new_stepdescr = []
    for stepdescr in stepdescr_list:
        if "\n" in stepdescr:
            a = stepdescr.replace("\n" , "")
            new_stepdescr.append(a)
        else:
            new_stepdescr.append(stepdescr)

    cloling_food = {"구분" : [{"음식명" : RCP_NM}, {"재료" : show_list} , {"레시피" : new_stepdescr}]}

    return cloling_food

def clolingRCP(RCP_NM):
    url_name = quote(RCP_NM)
    url = 'https://www.10000recipe.com/recipe/list.html?q=' + url_name
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")
    links = soup.find('a', class_='common_sp_link')["href"]
    new_ulr = 'https://www.10000recipe.com' + links 
    new_sourcecode = urllib.request.urlopen(new_ulr).read()
    soup = BeautifulSoup(new_sourcecode, "html.parser")
    div = soup.find('div', attrs={'class': "ready_ingre3"})
    try:
        cnt = 0
        stepdescr_list = []
        while True:
            div = soup.find('div', attrs={'id': f"stepdescr{cnt+1}"}).text
            stepdescr_list.append(f"{cnt+1}. {div}")
            cnt += 1
    except:
        pass
    new_stepdescr = []
    for stepdescr in stepdescr_list:
        if "\n" in stepdescr:
            a = stepdescr.replace("\n" , "")
            new_stepdescr.append(a)
        else:
            new_stepdescr.append(stepdescr)

    cloling_food = {"구분" : [{"음식명" : RCP_NM}, {"레시피" : new_stepdescr}]}

    return cloling_food