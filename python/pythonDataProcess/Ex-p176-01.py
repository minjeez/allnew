from pandas import Series
import numpy as np

mylist = [200, 300, 400, 100]
myindex = ['손오공', '저팔계', '사오정', '삼장법사']

print('\n실적 현황')
print('\n직원 실적')
myseries = Series(data=mylist, index=myindex)

for idx in myseries.index:
    print('Index : ' + idx + ', values : ' + str(myseries[idx]))