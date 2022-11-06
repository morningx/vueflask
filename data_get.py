# -*- coding: utf-8 -*-
# /usr/bin/python3
import pymysql
import urllib,urllib.request,sys
import ssl
import json
import pprint
import pandas as pd
from urllib import parse,request

def con_db(user,db,password):
    user,db,password = user,db,password
    con = pymysql.connect(host="127.0.0.1",
                          user=user,
                          password=password,
                          db=db,
                          autocommit=True)
    return con

def selectQuestionAnswerCode(user,db,password):
    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()
    # 获取表头
    sql1 = "SHOW FIELDS FROM question_answer_code"
    cur.execute(sql1)
    labels = cur.fetchall()
    labels = [l[0] for l in labels][0:2]
    # print(labels) # ['id', 'name', 'reliang', 'danbai', 'zhifang']
    sql2 = "select id,question from question_answer_code limit 30"
    cur.execute(sql2)
    content = cur.fetchall()
    # print(content)
    return [labels,content]

def data_json(user,db,password):
    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()
    cur.execute("select id,name,reliang,danbai,zhifang from yk_yycfb limit 30")
    data = pd.DataFrame(list(cur.fetchall()),
                        columns=["id","name","reliang","danbai","zhifang"])
    datajson = data.to_json(orient="records",force_ascii=False)
    # [{"宠物":"汪星人","年龄":25},{"宠物":"喵星人","年龄":23}]
    # df.to_json(orient="records",force_ascii=False)
    # https://blog.csdn.net/qq_43168299/article/details/115761834
    return datajson

# code-detail获取全部详情页物理表的行
def select_data(user,db,password):
    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()

    # 获取表头
    sql1 = "SHOW FIELDS FROM yk_yycfb"
    cur.execute(sql1)
    labels = cur.fetchall()
    labels = [l[0] for l in labels][0:5]
    # print(labels) # ['id', 'name', 'reliang', 'danbai', 'zhifang']

    sql2 = "select id,name,reliang,danbai,zhifang from yk_yycfb limit 30"
    cur.execute(sql2)
    content = cur.fetchall()
    # print(content)
    # ((1, '小麦', 317, 12, 1), (2, '五谷香', 377, 10, 3), (3, '小麦粉(标准粉)', 344, 11, 2), (

    return [labels,content]

def selectCodeDetaiWithlParam(user,db,password,id):
    # 通过con_db函数对应的user-db-password来ping连接mysql数据库
    # 生成对应游标进行数据查询准备
    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()
    # 通过游标执行sql语句操作，获取相应物理表表头
    param_id = id
    # print("param_id:::",param_id)
    sql_column_id = "select * from question_answer_code where id = " + str(param_id).strip()
    cur.execute(sql_column_id)
    res = list(cur.fetchone())
        # .append(param_id)
    # print("根据输入参数id来获取qac物理表对应的所有字段值：\n",sql_column_id,"\n id:::\n",id,"\n res:::\n ",res)
    connect_res.close()
    return res
