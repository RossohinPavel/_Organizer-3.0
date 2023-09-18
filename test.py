class Test:
    def __init__(self):
        self.attr = '123456'

    def __hash__(self):
        return hash(self.attr)

    def __eq__(self, other):
        return self.attr == other


test1 = Test()
test2 = Test()

print(id(test1), id(test2))

my_set = {test1, test2}
print(my_set)

for obj in my_set:
    print(id(obj))
