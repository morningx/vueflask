
### 2022.10~2022.11更新说明：
1 初始化：flask框架、vue框架构建前后端项目；
2.1 templates模板文件夹实现功能：
code-list.html：实现查询数据库物理表题目列表页，加载到表单内；
code-detail-param.html：实现查询数据库物理表题目详情页内容进行格式化展示；
question-answer.html：代码题目列表页，实现从数据库读取代码题目内容；
upload_code.html：代码题目解答新建页面，解决问题-说明-答案-思路-结果-分类登内容提交；
main-src.html：路由页面，实现后端SQL取数函数跟前端页面模板生成功能；
2.2 templates/index-part-page文件夹：
echarts-bar.html：柱状图，实现透视SQL取数及调用pyecharts生成可视化图；
stackbarpercent.html：实现不同维度透视取数SQL构建列表字典类型变量可视化展示；
wordcloud.html：采用结巴分词库对数据库表代码说明内容进行提取关键词后可视化展示；

### 小工具
1 豆瓣镜像：
pip install tensorflow -i "https://pypi.doubanio.com/simple/"

### 构建思路

1 前端html/js/css页面生成工具：
1.1 结合自动化生成前端页面工具打包生成的html/js/css文件，对html文件展示数据和路由后端页面进行绑定；
1.2 前端页面生成工具：https://www.layoutit.com/build
1.3 工具生成的css/js文件放入文件夹static/内，格式为code-XXX-src；

2 data_get.py：
2.1 主要为跟数据库交互类函数功能实现；
2.2 con_db函数：实现连接mysq数据库；
2.3 selectCodeDetaiWithlParam函数：实现根据id参数获取单个物理表单条数据行，比如详情页面；
2.4 select_data函数：实现获取单个物理表所有数据行，比如列表页面；

3 common_bus.py：
3.1 主要为逻辑处理业务过程类函数实现；
3.2 get_bus_inf函数：随机取100以内的数字，构建公交X分钟到达的信息流；

4 maxNumMinNumGetSum.py：
4.1 主要为子功能查看QA类编程题目列表list页面、详情detail页面业务交互逻辑类函数实现；
4.2 maxNumMinNumGetSum函数：函数内定义内容，将换行和空格替换为html格式（<br>/&nbsp;）处理，便于路由页面调用；

5 index.py：
5.1 主要为flask路由执行入口页面，实现@route路由调用函数生成页面；
5.2 /code-detail-param/id=<id>：代码详情页，生成问题/思路/样例/代码/结果栏页面内容；
5.3 /code-list：代码题目列表页面，从数据库提取到的代码题目后生成到表格内，点击查看详情可进入代码详情页；

6 templates文件夹：
6.1 包含前端展示页面html，html内代码js/css实现从static文件夹读取；
6.1 code-list.html：展示代码题目列表页面；
6.2 code-detail-param：带id参数展示数据库内不同id对应的查询结果内容；

### vueflask项目初始化步骤

pip install flask
pip install flask_jsglue
virtuanenv flask
cd flask
source bin/activate
cd ..
export FLASK_APP=index.py
flask run
-------------------
(flask) (base) helloxdeMacBook-Pro:Vue-flask-master hellox$ flask run
* Serving Flask app 'index.py'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
-------------------
