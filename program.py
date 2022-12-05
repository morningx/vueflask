# # -*- coding: utf-8 -*-
#!/usr/bin/python3
# import pandas as pd

def paTest():
    ins = ((1, '小麦', 317, 12, 1, 64, 11, 0, 2, 10, 0, 0, 4, 0, 2, 0, 289, 7, 34, 4, 5, 3, 2, 0, 325, 4), (2, '五谷香', 377, 10, 3, 78, 0, 0, 3, 6, 0, 0, 0, 0, 2, 0, 7, 1, 2, 0, 0, 0, 0, 0, 13, 1), (3, '小麦粉(标准粉)', 344, 11, 2, 72, 2, 0, 1, 13, 0, 0, 2, 0, 2, 0, 190, 3, 31, 50, 4, 2, 2, 0, 188, 5), (4, '小麦粉(富强粉，特一粉)', 350, 10, 1, 75, 1, 0, 1, 13, 0, 0, 2, 0, 1, 0, 128, 3, 27, 32, 3, 1, 1, 0, 114, 7), (5, '小麦粉(特二粉)', 349, 10, 1, 74, 2, 0, 1, 12, 0, 0, 2, 0, 1, 0, 124, 2, 30, 48, 3, 1, 1, 1, 120, 6), (6, '小麦胚粉', 392, 36, 10, 39, 6, 0, 5, 4, 4, 1, 4, 0, 23, 0, 1523, 5, 85, 198, 1, 17, 23, 1, 1168, 65), (7, '麸皮', 220, 16, 4, 30, 31, 20, 4, 14, 0, 0, 12, 0, 4, 0, 862, 12, 206, 382, 10, 11, 6, 2, 682, 7), (8, '挂面(均值)', 346, 10, 1, 75, 1, 0, 1, 12, 0, 0, 2, 0, 1, 0, 129, 184, 17, 49, 3, 1, 1, 0, 134, 12), (9, '挂面(标准粉)', 344, 10, 1, 74, 2, 0, 1, 12, 0, 0, 2, 0, 1, 0, 157, 150, 14, 51, 4, 1, 1, 0, 153, 10), (10, '挂面(富强粉)', 347, 10, 1, 76, 0, 0, 1, 13, 0, 0, 2, 0, 1, 0, 122, 111, 21, 48, 3, 1, 1, 0, 112, 11))
    print(type(ins),ins[0])
    # <class 'tuple'> (1, '小麦', 317, 12, 1, 64, 11, 0, 2, 10, 0, 0, 4, 0, 2, 0, 289, 7, 34, 4, 5, 3, 2, 0, 325, 4)
    res = pd.DataFrame(list(ins))
    print(res)

# args 是 arguments 的缩写，表示位置参数；
# kwargs 是 keyword arguments 的缩写，表示关键字参数;
# 可变参数的两种形式，并且 *args 必须放在 **kwargs 的前面，因为位置参数在关键字参数的前面。
def enumerateArgsTest(*args):
    for cnt,strv in enumerate(args):
        print("enumerateArgsTest:::",cnt,strv)
def enumerateKwargsTest(**kwargs):
    # TypeError: 'dict' object cannot be interpreted as an integer
    for name,value in kwargs.items():
        print("enumerateKwargsTest::: {0} is {1}".format(name,value))
def enumerateArgsKwargsTest(*args,**kwargs):
    for cnt,strv in enumerate(args):
        print("enumerateArgsKwargsTest:::",cnt,strv)
    for name,value in kwargs.items():
        print("enumerateArgsKwargsTest:::{0},{1}".format(name,value))

if __name__ == '__main__':
    enumerateArgsTest('a','b','c')
    enumerateArgsTest('a','b')
    enumerateKwargsTest(footname='apple',tdvalue = 'nice')
    enumerateKwargsTest(footname='pei',xdvalue = 'no')
    enumerateArgsKwargsTest('a',footname='apple',tdvalue = 'nice')