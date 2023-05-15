import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'

filename = 'mpg.csv'
myframe = pd.read_csv(filename, encoding='utf-8')
print(myframe)

frame01 = myframe.loc[myframe['drv'] == 'f', 'hwy']
frame01.index.name = 'f'

frame02 = myframe.loc[myframe['drv'] == '4', 'hwy']
frame02.index.name = '4'

frame03 = myframe.loc[myframe['drv'] == 'r', 'hwy']
frame03.index.name = 'r'

totalframe = pd.concat([frame01, frame02, frame03], axis=1, ignore_index=True)
totalframe.columns = ['f', '4', 'r']
print(totalframe)

totalframe.plot(kind='box')

plt.xlabel("구동 방식")
plt.ylabel("주행 마일수")
plt.grid(False)
plt.title("고속도로 주행 마일수의 상자수염")

filename = 'boxPlot02_image.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + ' Saved...')
plt.show()