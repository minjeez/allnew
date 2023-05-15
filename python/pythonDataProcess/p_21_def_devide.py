# def div(a, b):
#     i = a//b
#     v = a%b
#     return [i, v]
#
# arr = div(6, 4)
#
# print(arr[0])
# print(arr[1])

def divide(a, b):
    return (a / b, a % b)

a = input("Input first number : ")
b = input("Input second number : ")

q, r = divide(int(a), int(b))
print(f'The share is {int(q)} and remainder is {r}')
