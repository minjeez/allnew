import random

class findMax:
    def __init__(self, data):
        self.data = data
    def max(self):
        max = self.data[0]
        for i in self.data:
            if i > max:
                max = i
        return max

data = random.sample(range(1,101), 10)
print(data)

data1 = findMax(data)
print(f'Max value is : {data1.max()}')