numbers = (i for i in range(1, 101))

# print(list(numbers))
syk = ("3", "6", "9")

for i in list(numbers):
    st = str(i)
    if 10 > i:
        if st[0] in syk:
            print("짝")
        else:
            print(i)
    else:
        if st[0] in syk and st[1] in syk:
            print("짝짝")
        elif st[0] in syk or st[1] in syk:
            print("짝")
        else:
            print(i)


# st = str(10) ## st = 10인데 10은 string 10. 스트링 10은 10
# print(st[0])
# print(st[1])
#
# st = str(33)
# if st[0] == "3" and st[1] == "3":
#     print('짝짝')