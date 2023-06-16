import pandas as pd
import urllib.request
import json
from bs4 import BeautifulSoup
from urllib.parse import quote

url_name = quote("두루치기")
url = 'https://www.10000recipe.com/recipe/list.html?q=' + url_name
# print(url)
sourcecode = urllib.request.urlopen(url).read()
soup = BeautifulSoup(sourcecode, "html.parser")
links = soup.find('a', class_='common_sp_link')["href"]
new_ulr = 'https://www.10000recipe.com' + links 
new_sourcecode = urllib.request.urlopen(new_ulr).read()
soup = BeautifulSoup(new_sourcecode, "html.parser")
div = soup.find('div', attrs={'class': "ready_ingre3"})
food = div.text
food = food.split(" ")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
food = food
# col = "재료"
df = pd.DataFrame(food , columns = ["재료"])
df = df[df["재료"] != ""]

print(df)

try:
  cnt = 0
  stepdescr_list = []
  while True:
            div = soup.find('div', attrs={'id': f"stepdescr{cnt+1}"}).text
            stepdescr_list.append(div)
            cnt += 1
except:
  print("완료되었습니다.")
print(stepdescr_list)