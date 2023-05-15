# Hi This is Recurseive machanism Good bye
result = 0
for i in range(1, 11):
    result += i

print(result)



def summary(n):
    inner = 0
    for i in range(n, 0, -1):
        inner += i
    return inner

print(summary(10))



def summary_rec(n):
    print('나 불렀냐')
    if n == 1:
        return 1
    return n + summary_rec(n-1)

# sr(1) : 1
# sr(2) : 2 + 1

print(summary_rec(10))