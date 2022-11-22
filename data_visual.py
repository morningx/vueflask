from random import randrange
from pyecharts import options as opts
from pyecharts.charts import Bar, Geo, Map
from pyecharts.charts import Bar
from pyecharts.faker import Faker
import data_get
import random
from pyecharts.charts import Bar,Gauge,Pie,Page,Funnel,Geo,Scatter3D
# from pyecharts.constants import DEFAULT_HOST
from flask import Flask, render_template
from pyecharts import options as opts
from pyecharts.charts import WordCloud

# https://gallery.pyecharts.org/#/WordCloud/wordcloud_custom_font_style
def WorldCloud(word_cloud_data):
    word_cloud_data = word_cloud_data
    import ml
    words = ml.jieba_WordCloudData(word_cloud_data)
    # print("res_jieba_cnt_res_jieba_stopwords:::",words)
    # res_jieba_cnt_res_jieba_stopwords::: [('样', 6), ('例', 6), ('输出', 14), ('个数', 8), ('最小', 4
    c = (
        WordCloud()
        .add(
            "",
            words,
            word_size_range=[20, 100],
            textstyle_opts=opts.TextStyleOpts(font_family="cursive"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="QA问答关键词"))
        .render("templates/index-part-page/wordcloud.html")
    )



# https://blog.csdn.net/qq_58738770/article/details/127723556
def Histogram():
    filename = open(f'part-data.txt', 'r', encoding='utf-8')  # 柱状图
    lines = filename.read()
    line_list = lines.split('\n')
    tpe = []
    num = []
    for line in line_list:
        jguo = line.split(",")
        tpe.append(jguo[0])
        num.append(jguo[1])
    list_1 = dict(zip(tpe, num))
    # print(list_1)

    return list_1

# 获取分类数据及对应分类的总个数
def select_category(user,db,password):
    import data_get
    connect_res = data_get.con_db(user,db,password)
    connect_res.ping()
    cur = connect_res.cursor()

    sql = "select category,count(category) as total from question_answer_code group by category order by category asc"
    cur.execute(sql)
    total = cur.fetchall()
    total = [ i for i in total]
    # print(total)
    # [('回溯', 1), ('排序', 1), ('查找', 1), ('贪心', 2)]
    total = dict(total)

    return total

# https://blog.csdn.net/u013421629/article/details/78191967
def scatter3d():
    data = [generate_3d_random_point() for _ in range(80)]
    range_color = [
        '#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
        '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("3D scattering plot demo", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    return scatter3D
def generate_3d_random_point():
    return [random.randint(0, 100),random.randint(0, 100),random.randint(0, 100)]

from pyecharts import options as opts
from pyecharts.charts import Bar,Gauge,Pie,Page,Funnel,Geo,Scatter3D
import random

def scatter3dnew():
    data = [(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)) for _ in range(80)]

    c = (Scatter3D(init_opts=opts.InitOpts(width="1440px", height="720px",bg_color="black"))  #初始化
         .add("Scatter3D",       # 图例名称
              data,               # 包含列表的列表, 数据项，数据中，每一行是一个数据项，每一列属于一个维度
              grid3d_opts=opts.Grid3DOpts(width=100,  # 三维笛卡尔坐标系组件在三维场景中的宽度
                                          height=100,
                                          depth=100,  # 三维笛卡尔坐标系组件在三维场景中的深度。
                                          rotate_speed=500,  # 物体自转的速度。
                                          is_rotate=True,  # 是否开启视角绕物体的自动旋转查看。
                                          )
              )
         .set_global_opts(
             title_opts=opts.TitleOpts(title="Scatter_3D",       #添加标题
                                       title_textstyle_opts=opts.TextStyleOpts(font_size=25,
                                                                               color='#FFFFFF',  # 文字颜色。
                                                                               border_radius=True,  # 文字块的圆角
                                                                               border_color="white"), # 文字块边框颜色
                                       ),
         )
         .render("./templates/index-part-page/scatter3dnew.html"),
         )

from pyecharts import options as opts
from pyecharts.charts import Bar, Grid
from pyecharts.faker import Faker
def echartsBar():
    bar = (
        Bar(init_opts=opts.InitOpts(chart_id="1234"))
        .add_xaxis(Faker.choose())
        .add_yaxis("商家A", Faker.values())
        .add_yaxis("商家B", Faker.values())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="Bar-Graphic Image（旋转功能）组件示例"),
            graphic_opts=[
                opts.GraphicImage(
                    graphic_item=opts.GraphicItem(
                        id_="logo", right=20, top=20, z=-10, bounding="raw", origin=[75, 75]
                    ),
                    graphic_imagestyle_opts=opts.GraphicImageStyleOpts(
                        image="https://www.echartsjs.com/zh/images/favicon.png",
                        width=150,
                        height=150,
                        opacity=0.4,
                    ),
                )
            ],
        )
    )
    c = (
        Grid(init_opts=opts.InitOpts(chart_id="1234"))
        .add(
            chart=bar,
            grid_opts=opts.GridOpts(pos_left="5%", pos_right="4%", pos_bottom="5%"),
        )
        .add_js_funcs(
            """
            var rotation = 0;
            setInterval(function () {
            chart_1234.setOption({
            graphic: {
            id: 'logo',
            rotation: (rotation += Math.PI / 360) % (Math.PI * 2)
            }
            });
            }, 30);
            """
        )
        .render("templates/index-part-page/echartsBar.html")
    )

from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

# https://gallery.pyecharts.org/#/Bar/stack_bar_percent
def stackBarPercent3(levelx,select,sort,back,heart):
# def stackBarPercent(levelx,list_simple,list_medium,list_hard):
    # list_select=res[1],list_sort=res[1],list_heart=res[1],list_back=res[1]
    lvx = levelx
    select = select
    sort = sort
    back = back
    heart = heart
    # print("select: ",select)
    # select:  [{'value': 0, 'percent': 0}, {'value': 3, 'percent': Decimal('0.7500')}, {'value': 1, 'percent': Decimal('0.2500')}]

    # "查找","排序","贪心","回溯"
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(lvx)
        .add_yaxis("查找", select, stack="stack1", category_gap="50%")
        .add_yaxis("排序", sort, stack="stack1", category_gap="50%")
        .add_yaxis("贪心", heart, stack="stack1", category_gap="50%")
        .add_yaxis("回溯", back, stack="stack1", category_gap="50%")
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="left",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
        .render("templates/index-part-page/stackbarpercent.html")
    )
