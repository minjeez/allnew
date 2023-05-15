import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
filename = 'tips.csv'

myframe = pd.read_csv(filename, encoding='utf-8')
print(myframe)

mycolors = ['r', 'g', 'b']
labels = ['Female', 'Male']
print(labels)

cnt = 0
for finditem in labels:
    xdata = myframe.loc[myframe['sex'] == finditem, 'total_bill']
    ydata = myframe.loc[myframe['sex'] == finditem, 'tip']
    plt.plot(xdata, ydata, color=mycolors[cnt], marker='o', linestyle='None', label=finditem)
    cnt += 1

plt.legend(loc=4)
plt.xlabel("결제 총액")
plt.ylabel("팁 비용")
plt.title("결재 총액과 팁 비용의 산정도")
plt.grid(True)

plt.show()