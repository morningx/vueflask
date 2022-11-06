#!/usr/bin/python3
#coding=utf-8

import random
# import pandas as pd
# import numpy as np

def maxNumMinNumGetSum(numsN,listnums,maxminN):
    questionStr = """求最大N个数与最小N个数的和。"""
    thinkingstr = """1 初始化：input-strip-int-length数量，input-strip-split空格-map-int-list-inlis数字列表，input-strip-int-n取个数；判断去重复后的inlis是否大于等于【N*2】，否则return-1；
2 else输入inlis长度大于等于N*2：inlis列表去重复set后转list，排序sorted默认字典排序从小到大，取排序后的前N位置inlis[0:N]求和sum和后N位inlis[-2:]求和sum，加入到res列表中再求和，最终打印输出结果； """
    exampleStr = """5
95 88 83 64 100
2
输出：342
说明：最大2个数[100,95],最小2个数[83,64], 输出为342 """
    codeStr = """# length = int(input().strip())
# lis = list(map(int,input().strip()))
# frontEndN = int(intput().strip())
length = int(numsN)
lis = list(map(int,listnums))
maxminN = int(maxminN)
res = []
if len(set(lis)) <= maxminN :
    return "error,return value is: -1 "
else:
    sorlis = sorted(set(lis),reverse=False)
    res.append(sum(sorlis[0:maxminN]))
    res.append(sum(sorlis[-2:]))
    return "nice,return max N and min N value is :" + str(sum(res))
if __name__ == "__main__":
    numsN = 5
    listnums = [95,88,83,64,100]
    maxminN = 2
    res = maxNumMinNumGetSum(numsN=numsN,listnums=listnums,maxminN=maxminN)
    print(res) """

    questionStr = questionStr.replace("\n","</br>").replace(" ","&nbsp;")
    thinkingstr = thinkingstr.replace("\n","</br>").replace(" ","&nbsp;")
    exampleStr = exampleStr.replace("\n","</br>").replace(" ","&nbsp;")
    codeStr = codeStr.replace("\n","</br>").replace(" ","&nbsp;")

    othersStr = ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

    # length = int(input().strip())
    # lis = list(map(int,input().strip()))
    # frontEndN = int(intput().strip())
    length = int(numsN)
    lis = list(map(int,listnums))
    maxminN = int(maxminN)
    res = []
    value = ""
    if len(set(lis)) <= maxminN :
        value = "error,return value is: -1"
        return [questionStr,thinkingstr,exampleStr,codeStr,othersStr,value]
    else:
        sorlis = sorted(set(lis),reverse=False)
        res.append(sum(sorlis[0:maxminN]))
        res.append(sum(sorlis[-2:]))
        value = "nice,return max N and min N value is :" + str(sum(res))
        return [questionStr,thinkingstr,exampleStr,codeStr,othersStr,value]

if __name__ == "__main__":
    numsN = 5
    listnums = [95,88,83,64,100]
    maxminN = 2
    res = maxNumMinNumGetSum(numsN=numsN,listnums=listnums,maxminN=maxminN)
    print(res)


