from pandas import Series

myindex = ['강감찬', '이순신', '김유신', '광해군', '연산군', '을지문덕']
mylist = [50, 60, 40, 80, 70, 20]
myseries = Series(data=mylist, index=myindex)
print(myseries)

myseries[1] = 100
myseries[2:4] = 999
myseries [['강감찬', '을지문덕']] = 30
print(myseries)

