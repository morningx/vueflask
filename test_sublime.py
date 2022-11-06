# # -*- coding: utf-8 -*-
#!/usr/bin/python3


import pandas as pd

ins = ((1, '小麦', 317, 12, 1, 64, 11, 0, 2, 10, 0, 0, 4, 0, 2, 0, 289, 7, 34, 4, 5, 3, 2, 0, 325, 4), (2, '五谷香', 377, 10, 3, 78, 0, 0, 3, 6, 0, 0, 0, 0, 2, 0, 7, 1, 2, 0, 0, 0, 0, 0, 13, 1), (3, '小麦粉(标准粉)', 344, 11, 2, 72, 2, 0, 1, 13, 0, 0, 2, 0, 2, 0, 190, 3, 31, 50, 4, 2, 2, 0, 188, 5), (4, '小麦粉(富强粉，特一粉)', 350, 10, 1, 75, 1, 0, 1, 13, 0, 0, 2, 0, 1, 0, 128, 3, 27, 32, 3, 1, 1, 0, 114, 7), (5, '小麦粉(特二粉)', 349, 10, 1, 74, 2, 0, 1, 12, 0, 0, 2, 0, 1, 0, 124, 2, 30, 48, 3, 1, 1, 1, 120, 6), (6, '小麦胚粉', 392, 36, 10, 39, 6, 0, 5, 4, 4, 1, 4, 0, 23, 0, 1523, 5, 85, 198, 1, 17, 23, 1, 1168, 65), (7, '麸皮', 220, 16, 4, 30, 31, 20, 4, 14, 0, 0, 12, 0, 4, 0, 862, 12, 206, 382, 10, 11, 6, 2, 682, 7), (8, '挂面(均值)', 346, 10, 1, 75, 1, 0, 1, 12, 0, 0, 2, 0, 1, 0, 129, 184, 17, 49, 3, 1, 1, 0, 134, 12), (9, '挂面(标准粉)', 344, 10, 1, 74, 2, 0, 1, 12, 0, 0, 2, 0, 1, 0, 157, 150, 14, 51, 4, 1, 1, 0, 153, 10), (10, '挂面(富强粉)', 347, 10, 1, 76, 0, 0, 1, 13, 0, 0, 2, 0, 1, 0, 122, 111, 21, 48, 3, 1, 1, 0, 112, 11))
print(type(ins),ins[0])
# <class 'tuple'> (1, '小麦', 317, 12, 1, 64, 11, 0, 2, 10, 0, 0, 4, 0, 2, 0, 289, 7, 34, 4, 5, 3, 2, 0, 325, 4)

res = pd.DataFrame(list(ins))
print(res)