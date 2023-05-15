import prime_func

a = int(input("input number : "))

if prime_func.prime(a) == 1:
    print(f'{a} is a prime number')

else:
    print(f'{a} is not a prime number')
