import p25_timer as ti

timer = ti.counter2()

cnt = 0

while True:
    n = timer()
    if n > 100:
        break
    if n % 7 == 0:
        print(n)
        cnt += 1

print(cnt)

