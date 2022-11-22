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
    con = pymysql.connect(host="localhost",
                          port=3306,
                          user=user,
                          password=password,
                          db=db,
                          charset='utf8',
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
    labels = [l[0] for l in labels][0:4]
    # print(labels) # ['id', 'name', 'reliang', 'danbai', 'zhifang']
    sql2 = "select id,level,category,question from question_answer_code limit 30"
    cur.execute(sql2)
    content = cur.fetchall()
    # print("content:::",content)
    # content::: ((1, '题目18888888888888888'), (2, '求最大N个数与最小N个数的和'), (3, '题目3'), (4, '求最大N个数与最小N个数的和new'), (5, '题目4'), (6, '题目5'),9'), (10, '题目10'), (11, '题目11'), (12, '题目12'), (21, '222'))

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
# 写入前端代码题目数据页面数据到数据库
def insertDataToDB(user,db,password,l,ca,q,e,t,co,r):
    levelStr = l
    categoryStr = ca
    questionStr = str(q.replace("\n","</br>").replace(" ","&nbsp;"))
    exampleStr = str(e.replace("\n","</br>").replace(" ","&nbsp;"))
    thinkStr = str(t.replace("\n","</br>").replace(" ","&nbsp;"))
    codeStr = str(co.replace("\n","</br>").replace(" ","&nbsp;"))
    resultStr = str(r.replace("\n","</br>").replace(" ","&nbsp;"))
    # 通过con_db函数对应的user-db-password来ping连接mysql数据库
    # 生成对应游标进行数据查询准备
    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()
    # 通过游标执行sql语句操作，获取相应物理表表头
    sql_insert = "insert into question_answer_code(level,category,question,think,code,example,result) values (" "'"+levelStr+"'," + "'"+categoryStr +"'," + "'"+questionStr+"'," +  "'"+thinkStr+"',"+"'"+codeStr+"',"+"'"+exampleStr+"',"+"'"+resultStr+"'"+")"
    print(sql_insert)
    try:
        cur.execute(sql_insert)
        connect_res.commit() # 提交到数据库执行
        print("插入数据成功")
    except Exception as e:
        print('插入失败', str(e))
    finally:
        cur.close()
    return "ok"

# 获取分类数据及对应分类的总个数
def select_category(user,db,password):

    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()

    sql1 = "select distinct category from question_answer_code order by category asc"
    cur.execute(sql1)
    category = cur.fetchall()
    category = [ i[0] for i in category]
    # print(category,[ i[0] for i in category])
    # (('回溯',), ('排序',), ('查找',), ('贪心',)) ['回溯', '排序', '查找', '贪心']

    sql2 = "select category,count(category) as total from question_answer_code group by category order by category asc"
    cur.execute(sql2)
    total = cur.fetchall()
    total = [ i for i in total]
    # print(total)
    # [('回溯', 1), ('排序', 1), ('查找', 1), ('贪心', 2)]

    # sql3 = "select distinct level from question_answer_code order by level asc"
    sql3 = "select DISTINCT level,case when level='简单' then 1 when level='中等' then 2 when level='困难' then 3 else 'others' end as level_id from question_answer_code order by level_id"
    cur.execute(sql3)
    level = cur.fetchall()
    level = [ i[0] for i in level]
    # print(category,[ i[0] for i in category])

    return [category,total,level]

# 根据level级别查category类别数据
def select_stackbarpercent(user,db,password):

    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()

    # X轴查询题目等级：简单，中等，困难
    sql1 = "select DISTINCT level,case when level='简单' then 1 when level='中等' then 2 when level='困难' then 3 else 'others' end as level_id from question_answer_code order by level_id"
    cur.execute(sql1)
    level = cur.fetchall()
    level = [ i[0] for i in level]

    # X轴查询题目等级：简单，中等，困难
    sql2 = '''select
tempa.level_id,tempa.category_id,tempb.total_level,
tempa.level,
tempa.category,
tempa.total_level_category,
tempa.total_level_category / tempb.total_level as percent
from
(select level_id,level,category_id,category,total_level_category
from (
select
case
when level='简单' then 1
when level='中等' then 2
when level='困难' then 3
else 'others' end as level_id,
level,
case
when category='查找' then 1
when category='排序' then 2
when category='回溯' then 3
when category='贪心' then 4
else 'others' end as category_id,
category,
count(level) as total_level_category
from
question_answer_code
group by level,category
)temp where 1=1
order by level_id,category_id asc
) tempa
left join
(
select
case
when level='简单' then 1
when level='中等' then 2
when level='困难' then 3
else 'others' end as level_id,
level,
count(level) as total_level
from
question_answer_code
group by level
order by level_id
)tempb
on tempa.level_id = tempb.level_id
where 1=1
order by level_id,category_id asc
'''
    cur.execute(sql2)
    level_simple = []
    total_level_categor = cur.fetchall()
    # total_level_categor:  (('1', '简单', '4', '贪心', 2, 2, Decimal('1.0000')), ('2', '中等', '1', '查找', 1, 1, Decimal('1.0000')), ('3', '困难', '1', '查找', l('0.3333')), ('3', '困难', '2', '排序', 1, 3, Decimal('0.3333')), ('3', '困难', '3', '回溯', 1, 3, Decimal('0.3333')))
    # print("total_level_categor: ",total_level_categor)

    for i in range(len(total_level_categor)):
        if total_level_categor[i][0] == '1':
            level_simple.append(total_level_categor[i])
    # print("level_simple：",level_simple)
    # level_simple： [('1', '4', 2, '简单', '贪心', 2, Decimal('1.0000'))]
    level_simple = level_simple[0][3:]
    # print(level_simple)
    # ('简单', '贪心', 2, Decimal('1.0000'))
    res_level_simple_key = ["查找","排序","贪心","回溯"]
    res_level_simple_value = []
    if level_simple[1] != '查找':
        # res_level_simple_value.append((0,0))\
        res_level_simple_value.append({"value":0,"percent":0})
    else:
        # res_level_simple_value.append((level_simple[2],level_simple[3]))
        res_level_simple_value.append({"value":level_simple[2],"percent":level_simple[3]})
    if level_simple[1] != '排序':
        res_level_simple_value.append({"value":0,"percent":0})
    else:
        res_level_simple_value.append({"value":level_simple[2],"percent":level_simple[3]})
    if level_simple[1] != '贪心':
        res_level_simple_value.append({"value":0,"percent":0})
    else:
        res_level_simple_value.append({"value":level_simple[2],"percent":level_simple[3]})
    if level_simple[1] != '回溯':
        res_level_simple_value.append({"value":0,"percent":0})
    else:
        res_level_simple_value.append({"value":level_simple[2],"percent":level_simple[3]})

    # print("res_level_simple_value: ",res_level_simple_value)
    # res_level_simple_value:  [{'value': 0, 'percent': 0}, {'value': 0, 'percent': 0}, {'value': 2, 'percent': Decimal('1.0000')}, {'value': 0, 'percent': 0}]

    return [level,res_level_simple_value]


'''
level_id level category_id category total_level_category total_level percent
1	简单	4	贪心	2	2	1.0000
2	中等	1	查找	1	1	1.0000
3	困难	1	查找	1	3	0.3333
3	困难	2	排序	1	3	0.3333
3	困难	3	回溯	1	3	0.3333
'''

# 根据category类别查level级别数据
def select_stackbarpercent2(user,db,password):

    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()

    # X轴查询题目等级：简单，中等，困难
    sql1 = "select DISTINCT level,case when level='简单' then 1 when level='中等' then 2 when level='困难' then 3 else 'others' end as level_id from question_answer_code order by level_id"
    cur.execute(sql1)
    level = cur.fetchall()
    level = [ i[0] for i in level]

    # X轴查询题目等级：简单，中等，困难
    sql2 = '''select
    tempa.category_id,tempa.level_id,tempb.total_category,
    tempa.category,
    tempa.level,
    tempa.total_category_level,
    tempa.total_category_level / tempb.total_category as percent
    from
    (
    select DISTINCT
    case
    when category='查找' then 1
    when category='排序' then 2
    when category='回溯' then 3
    when category='贪心' then 4
    else 'others' end as category_id,
    category,
    case
    when level='简单' then 1
    when level='中等' then 2
    when level='困难' then 3
    else 'others' end as level_id,
    level,
    count(category) as total_category_level
    from
    question_answer_code
    group by category_id,category,level_id,level
    order by category_id asc
    )tempa

    left join

    (select DISTINCT
    case
    when category='查找' then 1
    when category='排序' then 2
    when category='贪心' then 3
    when category='回溯' then 4
    else 'others' end as category_id,
    category,
    count(category) as total_category
    from
    question_answer_code
    group by category
    order by category_id
    )tempb

    on tempa.category_id = tempb.category_id
    where 1=1
    order by category_id,level_id asc
    '''
    cur.execute(sql2)
    level_simple = []
    level_medium = []
    level_hard = []
    total_category_level = cur.fetchall()
    # print("total_level_categor: ",total_category_level)
    # total_level_categor:  (('1', '2', 2, '查找', '中等', 1, Decimal('0.5000')), ('1', '3', 2, '查找', '困难', 1, Decimal('0.5000')), ('2', '3', 1, '排序', '困难l('1.0000')), ('3', '3', 2, '回溯', '困难', 1, Decimal('0.5000')), ('4', '1', 1, '贪心', '简单', 2, Decimal('2.0000')))

    for i in range(len(total_category_level)):
        if total_category_level[i][1] == '1':
            level_simple.append(total_category_level[i])
        if total_category_level[i][1] == '2':
            level_medium.append(total_category_level[i])
        if total_category_level[i][1] == '3':
            level_hard.append(total_category_level[i])

    # print("level_simple：",level_simple)
    # level_simple： [('1', '2', 2, '查找', '中等', 1, Decimal('0.5000')), ('1', '3', 2, '查找', '困难', 1, Decimal('0.5000'))]
    level_simple = [level_simple[i][3:] for i in range(len(level_simple))]
    # print("level_simple: ",level_simple)
    # level_select:  [('贪心', '简单', 2, Decimal('2.0000'))]
    # ["简单","中等","困难"]
    res_level_simple_value = [{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0}]
    for i in range(len(level_simple)):
        if level_simple[i][0] == '查找':
            res_level_simple_value[0] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
        elif level_simple[i][0] == '排序':
            res_level_simple_value[1] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
        elif level_simple[i][0] == '回溯':
            res_level_simple_value[2] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
        elif level_simple[i][0] == '贪心':
            res_level_simple_value[3] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
    # print("res_level_simple_value: ",res_level_simple_value)
    # res_level_select_value:  [{'value': 0, 'percent': 0}, {'value': 1, 'percent': Decimal('0.5000')}, {'value': 1, 'percent': Decimal('0.5000')}]
    # levelx=res[0],list_select=res[1],list_sort=res[2],list_heart=res[3],list_back=res[4]

    level_medium = [level_medium[i][3:] for i in range(len(level_medium))]
    # print("level_medium: ",level_medium)
    res_level_medium_value = [{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0}]
    for i in range(len(level_medium)):
        if level_medium[i][0] == '查找':
            res_level_medium_value[0] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
        elif level_medium[i][0] == '排序':
            res_level_medium_value[1] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
        elif level_medium[i][0] == '回溯':
            res_level_medium_value[2] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
        elif level_medium[i][0] == '贪心':
            res_level_medium_value[3] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
    # print("res_level_medium_value: ",res_level_medium_value)

    # print("level_hard:\n",level_hard)
    level_hard = [level_hard[i][3:] for i in range(len(level_hard))]
    # print("level_hard: ",level_hard)
    res_level_hard_value = [{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0}]
    for i in range(len(level_hard)):
        if level_hard[i][0] == '查找':
            res_level_hard_value[0] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
        elif level_hard[i][0] == '排序':
            res_level_hard_value[1] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
        elif level_hard[i][0] == '回溯':
            res_level_hard_value[2] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
        elif level_hard[i][0] == '贪心':
            res_level_hard_value[3] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
    # print("res_level_hard_value: ",res_level_hard_value)
    # res_level_hard_value:  [{'value': 0, 'percent': 0}, {'value': 0, 'percent': 0}, {'value': 0, 'percent': 0}, {'value': 4, 'percent': Decimal('1.3333')}]

    return [level,
                res_level_simple_value,
                res_level_medium_value,
                res_level_hard_value
            ]

# 根据category类别查level级别数据
def select_stackbarpercent3(user,db,password):

    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()

    # X轴查询题目等级：简单，中等，困难
    sql1 = "select DISTINCT level,case when level='简单' then 1 when level='中等' then 2 when level='困难' then 3 else 'others' end as level_id from question_answer_code order by level_id"
    cur.execute(sql1)
    level = cur.fetchall()
    level = [ i[0] for i in level]

    # X轴查询题目等级：简单，中等，困难
    sql2 = '''select
    tempa.category_id,tempa.level_id,tempb.total_category,
    tempa.category,
    tempa.level,
    tempa.total_category_level,
    tempa.total_category_level / tempb.total_category as percent
    from
    (
    select DISTINCT
    case
    when category='查找' then 1
    when category='排序' then 2
    when category='回溯' then 3
    when category='贪心' then 4
    else 'others' end as category_id,
    category,
    case
    when level='简单' then 1
    when level='中等' then 2
    when level='困难' then 3
    else 'others' end as level_id,
    level,
    count(category) as total_category_level
    from
    question_answer_code
    group by category_id,category,level_id,level
    order by category_id asc
    )tempa

    left join

    (select DISTINCT
    case
    when category='查找' then 1
    when category='排序' then 2
    when category='贪心' then 3
    when category='回溯' then 4
    else 'others' end as category_id,
    category,
    count(category) as total_category
    from
    question_answer_code
    group by category
    order by category_id
    )tempb

    on tempa.category_id = tempb.category_id
    where 1=1
    order by category_id,level_id asc
    '''
    cur.execute(sql2)
    level_simple = []
    level_medium = []
    level_hard = []
    total_category_level = cur.fetchall()
    # print("total_level_categor: ",total_category_level)
    # total_level_categor:  (('1', '2', 2, '查找', '中等', 1, Decimal('0.5000')), ('1', '3', 2, '查找', '困难', 1, Decimal('0.5000')), ('2', '3', 1, '排序', '困难l('1.0000')), ('3', '3', 2, '回溯', '困难', 1, Decimal('0.5000')), ('4', '1', 1, '贪心', '简单', 2, Decimal('2.0000')))

    for i in range(len(total_category_level)):
        if total_category_level[i][1] == '1':
            level_simple.append(total_category_level[i])
        if total_category_level[i][1] == '2':
            level_medium.append(total_category_level[i])
        if total_category_level[i][1] == '3':
            level_hard.append(total_category_level[i])

    # print("level_simple：",level_simple)
    # level_simple： [('1', '2', 2, '查找', '中等', 1, Decimal('0.5000')), ('1', '3', 2, '查找', '困难', 1, Decimal('0.5000'))]
    level_simple = [level_simple[i][3:] for i in range(len(level_simple))]
    # print("level_simple: ",level_simple)
    level_medium = [level_medium[i][3:] for i in range(len(level_medium))]
    level_hard = [level_hard[i][3:] for i in range(len(level_hard))]

    # level_select:  [('贪心', '简单', 2, Decimal('2.0000'))]
    # ["简单","中等","困难"]
    res_level_select_value = [{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0}]
    res_level_sort_value = [{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0}]
    res_level_back_value = [{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0}]
    res_level_heart_value = [{"value":0,"percent":0},{"value":0,"percent":0},{"value":0,"percent":0}]
    for i in range(len(level_simple)):
        if level_simple[i][0] == '查找':
            res_level_select_value[0] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
        elif level_simple[i][0] == '排序':
            res_level_sort_value[0] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
        elif level_simple[i][0] == '回溯':
            res_level_back_value[0] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
        elif level_simple[i][0] == '贪心':
            res_level_heart_value[0] = {"value":level_simple[i][2],"percent":level_simple[i][3]}
    # print("level_simple:::res_level_select_value: ",res_level_select_value,"/n")
    # print("level_simple:::res_level_sort_value: ",res_level_sort_value,"/n")
    # print("level_simple:::res_level_back_value: ",res_level_back_value,"/n")
    # print("level_simple:::res_level_heart_value: ",res_level_heart_value,"/n")

    for i in range(len(level_medium)):
        if level_medium[i][0] == '查找':
            res_level_select_value[1] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
        elif level_medium[i][0] == '排序':
            res_level_sort_value[1] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
        elif level_medium[i][0] == '回溯':
            res_level_back_value[1] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
        elif level_medium[i][0] == '贪心':
            res_level_heart_value[1] = {"value":level_medium[i][2],"percent":level_medium[i][3]}
    # print("level_medium:::res_level_select_value: ",res_level_select_value,"/n")
    # print("level_medium:::res_level_sort_value: ",res_level_sort_value,"/n")
    # print("level_medium:::res_level_back_value: ",res_level_back_value,"/n")
    # print("level_medium:::res_level_heart_value: ",res_level_heart_value,"/n")

    for i in range(len(level_hard)):
        if level_hard[i][0] == '查找':
            res_level_select_value[2] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
        elif level_hard[i][0] == '排序':
            res_level_sort_value[2] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
        elif level_hard[i][0] == '回溯':
            res_level_back_value[2] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
        elif level_hard[i][0] == '贪心':
            res_level_heart_value[2] = {"value":level_hard[i][2],"percent":level_hard[i][3]}
    # print("level_hard:::res_level_select_value: ",res_level_select_value,"/n")
    # print("level_hard:::res_level_sort_value: ",res_level_sort_value,"/n")
    # print("level_hard:::res_level_back_value: ",res_level_back_value,"/n")
    # print("level_hard:::res_level_heart_value: ",res_level_heart_value,"/n")

    return [level,res_level_select_value,res_level_sort_value,res_level_back_value,res_level_heart_value]


def worldCloudDataGet(user,db,password):

    connect_res = con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()

    # X轴查询题目等级：简单，中等，困难
    sql = "select example from question_answer_code"
    cur.execute(sql)
    word_cloud_data = cur.fetchall()
    # print("word_cloud_data str :::",type(str(word_cloud_data)))
    # word_cloud_data::: <class 'str'> (('样例1',), ('5</br>95&nbsp;88&nbsp;83&nbsp;64&nbsp;100</br>2</br>输出：342</br>说明：最大2个
    # exam = [ i[0] for i in word_cloud_data]
    return str(word_cloud_data)

if __name__ == "__main__":

    user = "root"
    password = "123456789"
    db_name = "todo_list"
    res_wc = worldCloudDataGet(user=user,db=db_name,password=password)
    print("resworldCloudDataGet()",res_wc)