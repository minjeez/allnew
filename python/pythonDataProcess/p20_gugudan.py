while True:
    n = input("Input the number(q : Quit) : ")

    if n == 'q':
        print("Exit")
        break;

    if int(n) < 2 or int(n) > 9:
        print("input number range 2~9!!")
        continue;

    for i in range(1,10):
        print(f'{n}*{i} = {int(n)*i}')