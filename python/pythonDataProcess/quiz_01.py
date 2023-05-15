import numpy as np
from pandas import Series, DataFrame
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

html = open("ex5-10.html", "r", encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

result = []
tbody = soup.find('tbody')
tds = tbody.findAll('td')
for data in tds:
    result.append(data.text)
print(result)
print(type(result))
print('-' * 50)

myframe = DataFrame(np.reshape(result, (4, 3)), columns=['이름', '국어', '영어'])
df = myframe.set_index(keys=['이름'])
print(type(df.astype(float)))

plt.rcParams['font.family'] = 'Malgun Gothic'
df.astype(float).plot(title='시험 점수', kind='line')

filename = 'quiz_01-Graph.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + 'Saved...')
plt.show()