import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'

filename = 'ex802.csv'
myframe = pd.read_csv(filename, index_col='type')
print(myframe)

myframe.plot(kind='line', rot=0, title='지역별 차종 교통량', figsize=(10, 6), legend=True)

filename = 'dataframeGraph02.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' Saved...')
plt.show()