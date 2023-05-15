class SmartPhone(Object):
    def __init__(self, brand, maker, price):
        self.brand = brand
        self.maker = maker
        self.price = price
    def __str__(self):
        return f'str: {self.brand} - {self.maker} - {self.price}'

    class Galaxy(SmartPhone):
        def __init__(self, brand, maker, price, country):
            self.brand = brand
            self.maker = maker
            self.price = price
            self.country = country
        def __str__(self):
            return f'str : {self.__clas__.__name__} ' \
            f'스마트폰은 {self.maker} 에서 출시되었고 ' \
            f'가격은 {self.price} 입니다. '

        iphone = SmartPhone('IPhone', 'Apple', 10000)
        print(iphone)
        galaxy = Galaxy('Galaxy', 'Samsung', 8000, 'South Korea')
        print(galaxy)



