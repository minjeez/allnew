mynum = [1, 2, 3, 4, 5]

## generator
def square_number(nums):
    for num in nums:
        yield num * num

for result in square_number(mynum):
    print(result)
