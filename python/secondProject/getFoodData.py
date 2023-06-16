import json, datetime, math
import requests
import os.path
import pandas as pd 

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

def getFoodData(pageNo, numOfRows):
    end_point = 'https://apis.data.go.kr/1471000/FoodNtrIrdntInfoService1/getFoodNtrItdntList1'

    parameters = ''
    parameters += "?serviceKey=" + get_secret("data_apiKey")
    parameters += "&pageNo=" + str(pageNo)
    parameters += "&numOfRows=" + str(numOfRows)
    parameters += "&type=json" 
    url = end_point + parameters
    
    res = getRequestUrl(url)
    if (res == None):
        return None
    else:
        dict_json = json.loads(res.text) 
        return dict_json

def NewData():
    jsonResult = []
    pageNo = 1
    numOfRows = 100
    nPage = 0
    while(True):
        print('pageNo : %d, nPage : %d' % (pageNo, nPage))
        jsonData = getFoodData(pageNo, numOfRows)
        print(jsonData)

        if (jsonData['header']['resultCode'] == '00'):
            totalCount = jsonData['body']['totalCount']
            print('데이터 총 개수 : ', totalCount)  

            for item in jsonData['body']['items']:
                jsonResult.append(item)

            if totalCount == 0:
                break
            nPage = math.ceil(totalCount / numOfRows)
            if (pageNo == nPage):
                break

            pageNo += 1
        else :
            break
    return jsonResult