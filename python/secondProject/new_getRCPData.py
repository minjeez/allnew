import json, datetime, math
import requests
import os.path
import pandas as pd 
import re
from konlpy.tag import Hannanum

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
    return words

def Regex(RCP_NM):
    words = DataProcess(RCP_NM)
    food_list = []
    for word in words:
        print(word)
        new_str = re.sub(r"[^\uAC00-\uD7A3]", "", word)
        food_list.append(new_str)