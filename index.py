#!/usr/bin/python3
#coding=utf-8
from flask import Flask, render_template, jsonify, url_for, request
from flask_jsglue import JSGlue
import random
import requests
from uuid import uuid1
import json
# flask+vue前后端分离项目，后端服务
from random import *
from flask_cors import CORS
import urllib.request

app = Flask(__name__)
app.debug = False
app.config['DEBUG']=False
jsglue = JSGlue()
jsglue.init_app(app)
#解决跨域问题 CORS(app, resources=r’/*’) 是解决跨域问题的
CORS(app)

user = "root"
password = "123456789"
db_name = "todo_list"

@app.route('/')
def index():
    import data_get
    global user,password,db_name
    res = data_get.select_category(user=user,db=db_name,password=password)
    # print(res[0])
    # print(res[1],[i[1] for i in res[1]])
    # print(res[2])
    # ['回溯', '排序', '查找', '贪心']
    # [('回溯', 1), ('排序', 1), ('查找', 1), ('贪心', 2)]
    # ['中等', '困难', '简单']

    return render_template('main-src.html',category=res[0],total=[i[1] for i in res[1]],level=res[2])

@app.route('/wordcloud', methods=["GET"])
def wordcloud():
    # import ml
    # resml = ml.jieba_example()
    # print("resml",resml)
    import data_get
    word_cloud_data = data_get.worldCloudDataGet(user=user,db=db_name,password=password)
    # print("word_cloud_data:::",type(word_cloud_data),word_cloud_data)
    # word_cloud_data::: <class 'str'> (('样例1',), ('5</br>95&nbsp;88&nbsp;83&nbsp;64&nbsp;100</br>2</br>输出：342</br>说明：最大2个
    import data_visual
    data_visual.WorldCloud(word_cloud_data)
    # hist = data_visual.Histogram() user=user,db=db_name,password=password
    # print(hist) {'回溯': 4, '排序': 1, '查找': 4, '贪心': 4}
    return render_template("index-part-page/wordcloud.html")


@app.route('/blogs')
def blogs_main():
    res = "test blogs-main page message!"
    return render_template("/blogs/blogs.html", result = res)

@app.route('/blogs/pdnp')
def pandas_numpy():
    import JupyterToHtml
    from JupyterToHtml import style_config
    JupyterToHtml.jupyterHtmlGet(
        file = "/Users/hellox/Documents/Code/Vue-flask-master/jupyter/pandas_numpy.ipynb",
        target= "/Users/hellox/Documents/Code/Vue-flask-master/templates/jupyter-html/pandas-numpy",
        config = style_config)
    # print("pandas numpy jupyter html re-start okk!")
    return render_template("/blogs/pdnp.html")

@app.route('/blogs/pandas-numpy')
def pandas_Numpy():
    # res = "test pandasNumpy page message!"
    return render_template("/jupyter-html/pandas-numpy.html")

@app.route("/stackbarpercent")
def stackbarpercent():
    import data_get
    global user,password,db_name
    res = data_get.select_stackbarpercent3(user=user,db=db_name,password=password)
    # print("res-level:",res[0],"\n")
    # res-level: ['简单', '中等', '困难']
    # print("res-list_select:",res[1],"\n")
    # res-level: [{'value': 0, 'percent': 0}, {'value': 1, 'percent': Decimal('0.5000')}, {'value': 1, 'percent': Decimal('0.5000')}]
    import data_visual
    #     return [level,res_level_select_value,res_level_sort_value,res_level_back_value,res_level_heart_value]
    data_visual.stackBarPercent3(levelx=res[0],select=res[1],sort=res[2],back=res[3],heart=res[4])
    # data_visual.stackBarPercent(levelx=res[0],list_simple=res[1],list_medium=res[2],list_hard=res[3])
    return render_template("index-part-page/stackbarpercent.html")

# scatter3d数据图生成
@app.route("/echartsBar")
def echartsBar():
    import data_visual
    data_visual.echartsBar()
    return render_template("index-part-page/echartsBar.html")

@app.route('/histogram', methods=["GET"])
def histogram():
    import data_visual
    hist = data_visual.select_category(user=user,db=db_name,password=password)
    # hist = data_visual.Histogram()
    # print(hist) {'回溯': 4, '排序': 1, '查找': 4, '贪心': 4}
    return render_template("histogram.html", Types=json.dumps(hist))

# 实现代码题目从页面新增功能
# https://blog.csdn.net/w2909526/article/details/107605670 使用flask实现提交表单至后台
@app.route('/code-add-new',methods=['POST','GET'])
def code_add_new():
    if request.method == 'POST':
        question=request.form.get('content_question')
        example=request.form.get('content_example')
        think=request.form.get('content_think')
        code=request.form.get('content_code')
        result=request.form.get('content_result')
        # print ("前端取数为：",question,example,think,code,result)
        import data_get
        global user,password,db_name
        data_get.insertDataToDB(user=user,db=db_name,password=password,q=question,e=example,t=think,c=code,r=result)

    return render_template('code-add-new.html')

@app.route('/code-add',methods=['POST','GET'])
def code_add():
    if request.method == 'POST':
        level=request.form.get('select_level')
        category=request.form.get('select_category')
        question=request.form.get('content_question')
        example=request.form.get('content_example')
        think=request.form.get('content_think')
        code=request.form.get('content_code')
        result=request.form.get('content_result')
        # print ("前端取下拉框数据为：",level,category)
        # print ("前端取数为：",question,example,think,code,result)
        import data_get
        global user,password,db_name
        data_get.insertDataToDB(user=user,db=db_name,password=password,
                                l = level,ca = category,
                                q=question,e=example,t=think,co=code,r=result)

    return render_template('code-add.html')

# https://blog.csdn.net/weixin_36380516/article/details/80008496
# 列表页不同参数id进入不同结果detail页面
# http://127.0.0.1:5000/code-detail-param/id=2
@app.route('/code-detail-param/id=<id>',methods=['GET'])
def code_detail_param(id):
    import data_get
    global user,password,db_name
    param_id = id
    res = data_get.selectCodeDetaiWithlParam(user=user,db=db_name,password=password,id=param_id)
    # print("res paran:::",res,type(res),res[0])
    # res paran::: [3, '题目3', '思路3', '代码3', '样例3', '结果3'] <class 'list'> 3
    return render_template('/code-detail-param.html', result = res)

# https://www.layoutit.com/build
@app.route('/code-list')
def code_list():
    global user,password,db_name
    import data_get
    resDbData = data_get.selectQuestionAnswerCode(user=user,db=db_name,password=password)
    labels=resDbData[0]
    content=resDbData[1]
    content_id = [ i[0] for i in content]
    content_level = [ i[1] for i in content]
    content_category = [ i[2] for i in content]
    print("labels,content_level:::",labels,content_level)
    # content_id::: [1, 2, 3]
    return render_template('code-list.html', labels=labels, content=content,id=content_id,category=content_category,level=content_level)

@app.route('/upload-code')
def upload_code():
    res = "test upload code page message!"
    return render_template("upload-code.html", result = res)

# http://www.ibootstrap.cn/#
@app.route('/code-detail')
def code_detail():
    import question_answer
    # from flask_jsglue import JSGlue
    numsN = 5
    listnums = [95,88,83,64,100]
    maxminN = 2
    res =  question_answer.maxNumMinNumGetSum(numsN=numsN,listnums=listnums,maxminN=maxminN)
    # print(res)

    # 测试输入带有br和nasp换行空格的代码字符串
    # thinkingstr = '</br>#&nbsp;length&nbsp;=&nbsp;int(input().strip())</br>#&nbsp;lis&nbsp;=&nbsp;list(map(int,input().strip()))</br>#&nbsp;frontEndN&nbsp;=&nbsp;int(intput().strip())</br>length&nbsp;=&nbsp;int(numsN)</br>lis&nbsp;=&nbsp;list(map(int,listnums))</br>maxminN&nbsp;=&nbsp;int(maxminN)</br>res&nbsp;=&nbsp;[]</br>if&nbsp;len(set(lis))&nbsp;<=&nbsp;maxminN&nbsp;:</br>&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;"error,return&nbsp;value&nbsp;is:&nbsp;-1&nbsp;"</br>else:</br>&nbsp;&nbsp;&nbsp;&nbsp;sorlis&nbsp;=&nbsp;sorted(set(lis),reverse=False)</br>&nbsp;&nbsp;&nbsp;&nbsp;res.append(sum(sorlis[0:maxminN]))</br>&nbsp;&nbsp;&nbsp;&nbsp;res.append(sum(sorlis[-2:]))</br>&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;"nice,return&nbsp;max&nbsp;N&nbsp;and&nbsp;min&nbsp;N&nbsp;value&nbsp;is&nbsp;:"&nbsp;+&nbsp;str(sum(res))</br></br>if&nbsp;__name__&nbsp;==&nbsp;"__main__":</br>&nbsp;&nbsp;&nbsp;&nbsp;numsN&nbsp;=&nbsp;5</br>&nbsp;&nbsp;&nbsp;&nbsp;listnums&nbsp;=&nbsp;[95,88,83,64,100]</br>&nbsp;&nbsp;&nbsp;&nbsp;maxminN&nbsp;=&nbsp;2</br>&nbsp;&nbsp;&nbsp;&nbsp;res&nbsp;=&nbsp;maxNumMinNumGetSum(numsN=numsN,listnums=listnums,maxminN=maxminN)</br>&nbsp;&nbsp;&nbsp;&nbsp;print(res)</br>'
    # thinkingstr = """
    # 1 初始化：input-strip-int-length数量，input-strip-split空格-map-int-list-inlis数字列表，input-strip-int-n取个数；判断去重复后的inlis是否大于等于【N*2】，否则return-1；</br> !!!!
    # 2 else输入inlis长度大于等于N*2：inlis列表去重复set后转list，排序sorted默认字典排序从小到大，取排序后的前N位置inlis[0:N]求和sum和后N位inlis[-2:]求和sum，加入到res列表中再求和，最终打印输出结果； """
    # res[1] = thinkingstr
    return render_template("code-detail.html", result = res)

@app.route("/condb")
def condb():
    global user,password,db_name
    import data_get
    resDbData = data_get.select_tab(user=user,
                    db=db_name,
                    password=password)
    return str(resDbData)

# https://blog.csdn.net/a19990412/article/details/84955802
@app.route('/data-get')
def data_get():
    global user,password,db_name
    import data_get
    resDbData = data_get.select_data(user=user,
                                db=db_name,
                                password=password)
    labels=resDbData[0]
    content=resDbData[1]
    # print(resDbData)
    return render_template('data-get.html', labels=labels, content=content)

@app.route("/inputkv")
def inputkv():
    key = request.args.get("key")
    value = request.args.get("value")
    return "input key value is : %s,%s" % (key,value)

# https://blog.csdn.net/EchoooZhang/article/details/104640241
WORDTL=[{
    'words': '',
    'tl': []
}]

@app.route('/tl', methods=['GET', 'POST'])
def tl():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        WORDTL.append({
            'words': post_data.get('words'),
            'tl': queryWords(post_data.get('words'))
        })
    else:
        response_object['data'] = WORDTL[-1]
    return jsonify(response_object)

# 定义路由Vue，打印默认的内容
@app.route('/vue', methods=['GET', 'POST'])
def vue():
    return 'Hello vue page message get！'

# 路由定义：调用niuke.py内的函数来页面显示函数返回的内容
@app.route("/question-answer")
def question_answer():
    import question_answer
    # from flask_jsglue import JSGlue
    numsN = 5
    listnums = [95,88,83,64,100]
    maxminN = 2
    res =  question_answer.maxNumMinNumGetSum(numsN=numsN,listnums=listnums,maxminN=maxminN)
    # print(reslis,len(reslis))
    # 让js文件中可以使用url_for方法
    # results = []
    # for i in range(len(reslis)):
    #    results.append(reslis[i])

    result_dict = []
    for i in range(len(res)):
        temp_dict = {} #临时dict
        temp_dict[ 'name' ] = i #键
        temp_dict[ 'result' ] = res[i] #值
        result_dict.append(temp_dict)
    # print(result_dict)
    return render_template("question-answer.html", result = result_dict)


@app.route("/businfo/<station>")
def businfo(station):
    import bus
    info = bus.get_bus_info(station)
    return {
"msg": "success",
"data": info
}

# 让js文件中可以使用url_for方法
results = []
# chars = 'ABCDEFGHIJKLMNOPQRSTUVWSYZ'
results.append({'name': '1 最大N个数与最小N个数的和', 'flag': 'true', 'url': 'http://127.0.0.1:5000/questionanswer'})
"""
results.append({'name': 'vue.js+flask+element-ui简易Demo', 'flag': 'true'})
results.append({'name': '代码请戳github', 'flag': 'true', 'url': 'https://github.com/qianbin01/Vue-flask'})
for i in range(3):
results.append({'name': random.choice(chars), 'index': str(uuid1())})
"""
# @app.route('/')
# def index():
#    return render_template('index.html')


@app.route('/ping')
def getbasedata():
    return jsonify({'results': results})


@app.route('/add', methods=['POST'])
def add():
    name = request.json.get('name')
    results.append({'name': name, 'index': str(uuid1())})  # uuid让index不唯一，实际开发中可以通过数据库的id来代替
    return jsonify({'message': '添加成功！'}), 200


@app.route('/update', methods=['PUT'])
def update():
    name = request.json.get('name')
    index = request.json.get('index')
    for item in results:
        if item['index'] == index:
            item['name'] = name
            break
    return jsonify({'message': '编辑成功！'}), 200


@app.route('/delete', methods=['DELETE'])
def delete():
    name = request.args.get('name')
    index = request.args.get('index')
    results.remove({'name': name, 'index': index})
    return jsonify({'message': '删除成功！'}), 200


if __name__ == '__main__':
    app.run(debug=True)
