def fibo(n):
    if n == 1 or n == 2:
        return 1
    return fibo(n-2) + fibo(n-1)


# 1 1 2 3 5 8 13
print(fibo(5))

def fibo_list(n):
    two_prev = 1
    one_prev = 1
    result = 0
    if n < 3:
        return 1
    for i in range(3, n+1):
        result = two_prev + one_prev
        two_prev, one_prev = one_prev, result
    return result


print(fibo_list(5))