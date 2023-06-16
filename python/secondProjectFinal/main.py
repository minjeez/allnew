import pandas as pd
import json
from fastapi import FastAPI, APIRouter
import new_getFoodData as nF 
import new_getRCPData as nR
import os
import requests

# from pydantic import BaseModel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')

app = FastAPI()
router = APIRouter()

RCP_NM = ""
sing_list = []

@app.get('/first_search_RCP')
async def first_search_RCP(first_RCP_NM):
    foods = nR.first_search_RCP(first_RCP_NM)
    new_foods = foods
    return new_foods

@app.get('/search_RCP')
async def searchRCP(RCP_NM_name):
    global RCP_NM
    food = nR.search_RCP(RCP_NM_name)
    RCP_NM = RCP_NM_name
    return food

@app.get('/Psearch_RCP_process')
async def searchRCPProcess():
    global RCP_NM
    processedfoods = nR.DataProcess(RCP_NM)
    return processedfoods

@app.get('/Regex')
async def Regex():
    global RCP_NM
    regexfoods = nR.Regex(RCP_NM)
    return regexfoods

@app.get('/firstmatch')
async def firstmatch():
    global RCP_NM
    firstmatch = nR.BinMatch(RCP_NM)
    return firstmatch

@app.get('/secondmatch')
async def secondmatch():
    global RCP_NM
    secondmatch= nR.FoodDBMatchFood(RCP_NM)
    return secondmatch

@app.get('/lastmatch')
async def lastmatch():
    global RCP_NM
    lastmatch= nR.trashMatch(RCP_NM)
    return lastmatch

@app.get('/singo')
async def singo(args):
    if "," in args:
        args_list = args.split(",")
    else:
        args_list = args.split(" ")
    cnt = 0
    for _ in args_list:
        args_list[cnt] = _.replace(" ", "")
        cnt += 1
    global RCP_NM, sing_list
    single = nR.singo(RCP_NM, args_list)
    sing_list = single["신고구분"][0]["신고완료후값"]
    return single 

@app.get('/foodListCkeck')
async def foodListCkeck(args):
    if "," in args:
        args_list = args.split(",")
    else:
        args_list = args.split(" ")
    print(args_list)
    cnt = 0
    for _ in args_list:
        args_list[cnt] = _.replace(" ", "")
        cnt += 1
    global RCP_NM, sing_list
    foodListCkeck= nR.foodListCkeck(RCP_NM,sing_list, args_list)
    sing_list = []
    return foodListCkeck

@app.get('/showRCP')
async def showRCP():
    global RCP_NM
    showRCP= nR.showRCP(RCP_NM)
    return showRCP

@app.get('/search_all')
async def search_all(RCP_NM_name):
    search_all = nR.search_all(RCP_NM_name)
    global RCP_NM
    RCP_NM = RCP_NM_name
    return search_all

# 원천소스 샘플

# @app.get('/getFoodData')
# async def getFoodData(pageNo, numOfRows):
#     foods = nF.getFoodData(pageNo, numOfRows)
#     pageNo = 1
#     numOfRows = 3
#     new_foods = foods
#     return new_foods

# @app.get('/foodDBget')
# async def foodDBget():
#     foodDBget = nF.NewData()
#     return foodDBget[0]

# @app.get('/arrangeCode')
# async def arrangeCode():
#     arrangeCode = nF.arrange_code()
#     return arrangeCode[0]

# request 받아서 동작 진행

# @app.get('/Psearch_RCP_process')
# async def Psearch_RCP_process():
#     global RCP_NM
#     print(RCP_NM)
#     baseurl='http://192.168.1.78:3000' 
#     try:
#         response = requests.get(baseurl + '/'+'search_RCP?RCP_NM_name="'+ RCP_NM)
#         processedfoods = nR.DataProcess(response)
#         return processedfoods.json()
    
#     except requests.exceptions.RequestException as e:
#         return {"ok": e}