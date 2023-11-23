def test_func(pos_arg, name_arg='test', **kwargs):
    print(test_func.__type_params__)
    print(kwargs)


t = test_func(1, 'name', test='test')
