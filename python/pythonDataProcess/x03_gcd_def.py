def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

a = int(input("Input First number : "))
b = int(input("Input Second number : "))
print(f'gcd({a}, {b}) of {a}, {b} : {gcd(a, b)}')