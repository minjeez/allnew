class minjee:

    def __init__(self, a, b):
        self.a = a
        self.b = b
    def gcd(self):
        while self.b != 0:
            self.a, self.b = self.b, self.a % self.b
        return self.a

a = int(input("Input First number : "))
b = int(input("Input Second number : "))

m = minjee(a, b)

print(f'gcd({a}, {b}) of {a}, {b} : {m.gcd()}')
