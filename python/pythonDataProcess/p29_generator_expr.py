numbers = [0, 1, 2, 3, 4]
evens = (2 * i for i in numbers)

print(evens)
print(evens.__next__())
print(evens.__next__())
print(sum(evens))

print(numbers)
numbers.reverse()
print(numbers)
evens = (2 * i for i in numbers)

print(evens)
print(evens.__next__())
print(evens.__next__())