import pandas as pd

myColumns = ('이름', '나이')
myencoding = 'utf-8'
mydata = [('김철수', 10), ('박영희', 20)]

myframe = pd.DataFrame(mydata, columns=myColumns)
print(myframe)

filename = 'csv_02_01.csv'
myframe.to_csv(filename, encoding=myencoding, mode='w', index=False, sep=' ')

filename = 'csv_02_02.csv'
myframe.to_csv(filename, encoding=myencoding, mode='w', index=False, sep='#')