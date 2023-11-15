import timeit
import sys


class Test:
    def __init__(self, name) -> None:
        self.name = name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Test):
            __value = __value.name
        return self.name == __value
    

test_lst = [Test(f'test{i}') for i in range(1000)]

def test_list():
    if 'test' not in test_lst:
        test_lst.append(Test('test'))
    if 'test1' not in test_lst:
        test_lst.append(Test('test'))

print(timeit.timeit(test_list, number=1000))
print(sys.getsizeof(test_lst) + sum(sys.getsizeof(x) for x in test_lst))

test_st = {Test(f'test{i}' for i in range(1000))}

def test_set():
    if 'test' not in test_lst:
        test_st.add(Test('test'))
    if 'test1' not in test_lst:
        test_lst.append(Test('test'))

print(timeit.timeit(test_set, number=1000))
print(sys.getsizeof(test_st) + sum(sys.getsizeof(x) for x in test_st))
