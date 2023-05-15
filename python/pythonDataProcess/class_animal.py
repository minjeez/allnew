class Animals(object):
    def __init__(self, name):
        self.name = name
    def move(self):
        print("move~")
    def speak(self):
        pass

class Dog(Animals):
    def speak(self):
        print("wolf-wolf")

class Duck(Animals):
    def speak(self):
        print("quack-quack")