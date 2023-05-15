def prime(x):
    for i in range(2, x):
        if x % i == 0:
            return 0
        else:
            return 1
