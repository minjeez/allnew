import numpy as np
from pandas import DataFrame

# sdata = {
#     '국어' : [60.00, 'NaN', 40.00],
#     '영어' : ['NaN', 80.00, 50.00],
#     '수학' : [90.00, 50.00, 'NaN']
# }
#
# myindex = ['강감찬', '김유신', '이순신']
# myframe = DataFrame(sdata, index=myindex)
# print(myframe)

mydata = [[60.00, np.nan, 90.00], [np.nan, 80.00, 50.00], [40.00, 50.00, np.nan]]
myindex = ['강감찬', '김유신', '이순신']
mycolumn = ['국어', '영어', '수학']
myframe = DataFrame(data=mydata, index=myindex, columns=mycolumn)
print('\nBefore')
print(myframe)

myframe.loc[myframe['국어'].isnull(), '국어'] = myframe['국어'].mean()
myframe.loc[myframe['영어'].isnull(), '영어'] = myframe['영어'].mean()
myframe.loc[myframe['수학'].isnull(), '수학'] = myframe['수학'].mean()
print('\nAfter')
print(myframe)
print('-' * 50)
print(myframe.describe())

# myframe.loc[['강감찬'], ['영어']] = 65.00
# myframe.loc[['김유신'], ['국어']] = 50.00
# myframe.loc[['이순신'], ['수학']] = 70.00
# print('## after')
# print(myframe)
