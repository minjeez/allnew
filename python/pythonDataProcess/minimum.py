def min(a, b):
    if a > b:
        return b
    else:
        return a


## p38_module1.py

import minimum

a = input('Input First number : ')
b = input('Input Second number : ')

print(f'Min number is {minimum.min(a, b)}')