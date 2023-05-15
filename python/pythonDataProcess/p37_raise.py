list = []

try:
    while True:
        print('Item amount : ', len(list))
        print('Iventory : ', list)

        if len(list) >= 4:
            raise Exception('Inventory lack')
        item = 'item' + str(len(list))
        list.append(item)

## e = cause of exception
except Exception as e:
    print('Inventory Full')
    print(e)