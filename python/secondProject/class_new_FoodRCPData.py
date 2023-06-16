import json, datetime, math
import requests
import os.path
import pandas as pd 
import re
import new_getFoodData as gF
from konlpy.tag import Hannanum
from pymongo import MongoClient

hannanum = Hannanum()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())
    
class RCPMatching(object):
    def __init__(self):
        self.RCP_NM = None

    def get_secret(self, setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            errorMsg = "Set the {} environment variable.".format(setting)
            return errorMsg

    def getRequestUrl(self, url):
        res = requests.get(url)
        try:
            if res.status_code == 200:
                return res
        except Exception as e:
            print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
            return None

    def getRCPData(self, startIdx, endIdx, RCP_NM):
        end_point = 'http://openapi.foodsafetykorea.go.kr'
        parameters = ''
        parameters += "/api/" + self.get_secret("data_apiKey2") + "/COOKRCP01/json"
        parameters += "/" + str(startIdx)
        parameters += "/" + str(endIdx)
        parameters += "/RCP_NM=" + str(RCP_NM)
        self.RCP_NM = RCP_NM
        url = end_point + parameters
        res = self.getRequestUrl(url)
        if (res == None):
            return None
        else:
            dict_json = json.loads(res.text) 
            return dict_json

    def searchRCP(self, RCP_NM):
        cnt = 0
        jsonResult = []
        startIdx = 1
        endIdx = 10
        RCP_Information = self.getRCPData(startIdx, endIdx, RCP_NM)
        if RCP_Information["COOKRCP01"]["RESULT"]["MSG"] == "해당하는 데이터가 없습니다.":
            cnt = 0
            print("관련데이터가 없습니다.")
        else:
            jsonResult.append(RCP_Information['COOKRCP01']['row'])
            cnt = 1   
            
        df = pd.DataFrame.from_dict(jsonResult[0]).T
        
        return df


    def DataProcess(self):
        df = self.searchRCP()
        RCP_vale = df.loc["RCP_PARTS_DTLS"].values
        words = hannanum.nouns(RCP_vale[0])
        return words

    def Regex(self):
        words = self.DataProcess()
        food_list = []
        for word in words:
            new_str = re.sub(r"[^\uAC00-\uD7A3]", "", word)
            food_list.append(new_str)
            
        return food_list

    def BinMatch(self):
        with open('bin_FoodData.json', 'r') as f:
            son_data = json.load(f)
        try:
            food_list = []
            cnt = 0
            while True:
                food_list.append(son_data[cnt]['재료'])
                cnt +=1
        except:
            print("완료되었습니다.")
        regex_list = self.Regex()
        
        show_list = []
        nomtach_list  = []
        for i in regex_list:
            if i in food_list: 
                show_list.append(i)
            else:
                nomtach_list.append(i)
        
        return [show_list, nomtach_list]     
            
    def FoodDBMatchFood(self):
        client = MongoClient('mongodb://192.168.0.254:27017/')
        db = client['test']
        collection_name = 'FoodData'
        collection = db[collection_name]
        myframe = collection.find({},{"식품이름"})
        myframe_list = []
        for _ in myframe:
            myframe_list.append(_["식품이름"])

        matchlist = self.BinMatch()
        
        show_list = []
        nomtach_list  = []
        for i in matchlist[1]:
            if i in myframe_list: 
                show_list.append(i)
            else:
                nomtach_list.append(i)
        
        # Putting matched ingredients in bin_FoodData.json
        df = pd.DataFrame(show_list , columns = ["재료"])
        df = df.to_dict("records")
        with open('bin_FoodData.json', 'w') as f:
            json.dump(df, f, ensure_ascii=False)
        
        return [show_list, nomtach_list]
    
    
    
# match = RCPMatching()
# a = match.searchRCP("닭고기김치찌개")
# print(a)
# print(a)
# b = match.DataProcess()
# print(b)

# print(a)