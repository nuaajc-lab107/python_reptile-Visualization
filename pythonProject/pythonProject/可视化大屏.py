from pyecharts import options as opts
from pyecharts.charts import Bar, Gauge, Pie, Page, Funnel, Geo, Scatter3D
import random


def bar():  # 柱状图
    cate = ['1月', '2月', '3月', '4月', '5月', '6月']
    c = (
        Bar()
        .add_xaxis(cate)
        .add_yaxis("订单数", [random.randint(100, 200) for _ in cate])
        .add_yaxis("完成数", [random.randint(50, 100) for _ in cate])
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=True, color="#2CB34A")

        )
        .set_global_opts(title_opts=opts.TitleOpts(title="2021年订单推移图",
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#2CB34A"),
                                                   pos_left="5%"),
                         legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#2CB34A")),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#2CB34A")),
                         yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color="#2CB34A"))

                         )
        .set_colors(["blue", "green"])
        # .render("bar_stack0.html")
    )
    return c


def tab0(name, color):  # 标题
    c = (Pie().
    set_global_opts(
        title_opts=opts.TitleOpts(title=name, pos_left='center', pos_top='center',
                                  title_textstyle_opts=opts.TextStyleOpts(color=color, font_size=20))))
    return c


def tab1(name, color):  # 标题
    c = (Pie().
    set_global_opts(
        title_opts=opts.TitleOpts(title=name, pos_left='center', pos_top='center',
                                  title_textstyle_opts=opts.TextStyleOpts(color=color, font_size=25))))
    return c


def gau():  # 仪表图
    c = (
        Gauge(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add(series_name="库位利用率", data_pair=[["", 90]])
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{a} <br/>{b} : {c}%"),

        )
        # .render("gauge.html")
    )
    return c


def radius():
    cate = ['客户A', '客户B', '客户C', '客户D', '客户E', '其他客户']
    data = [153, 124, 107, 99, 89, 46]
    c = Pie()
    c.add('', [list(z) for z in zip(cate, data)],
          radius=["30%", "75%"],
          rosetype="radius")
    c.set_global_opts(title_opts=opts.TitleOpts(title="客户销售额占比", padding=[1, 250],
                                                title_textstyle_opts=opts.TextStyleOpts(color="#FFFFFF")),
                      legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color="#FFFFFF"), type_="scroll",
                                                  orient="vertical", pos_right="5%", pos_top="middle")
                      )
    c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    c.set_colors(['red', "orange", "yellow", "green", "Cyan", "purple"])

    return c


def funnel():
    cate = ['访问', '注册', '加入购物车', '提交订单', '付款成功']
    data = [30398, 15230, 10045, 8109, 5698]
    c = Funnel()
    c.add("用户数", [list(z) for z in zip(cate, data)],
          sort_='ascending',
          label_opts=opts.LabelOpts(position="inside"))
    c.set_global_opts(title_opts=opts.TitleOpts(title=""))

    return c


def geo():
    city_num = [('武汉', 105), ('成都', 70), ('北京', 99),
                ('西安', 80), ('杭州', 60), ('贵阳', 34),
                ('上海', 65), ('深圳', 54), ('乌鲁木齐', 76),
                ('哈尔滨', 47), ('兰州', 56), ('信阳', 85)]
    start_end = [('宁波', '成都'), ('武汉', '北京'), ('武汉', '西安'),
                 ('长沙', '杭州'), ('武汉', '贵阳'), ('武汉', '上海'),
                 ('甘肃', '深圳'), ('北京', '乌鲁木齐'), ('上海', '哈尔滨'),
                 ('武汉', '兰州'), ('西藏', '信阳')]
    c = Geo()
    c.add_schema(maptype='china',
                 itemstyle_opts=opts.ItemStyleOpts(color='#323c48', border_color='white'))
    # 4.添加数据
    c.add('', data_pair=city_num, color='white')
    c.add('', data_pair=start_end, type_="lines", label_opts=opts.LabelOpts(is_show=False),
          effect_opts=opts.EffectOpts(symbol="arrow",
                                      color='gold',
                                      symbol_size=7))
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=""))

    return c


def scatter3D():
    data = [(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)) for _ in range(80)]
    c = (Scatter3D()
    .add("", data)
    .set_global_opts(
        title_opts=opts.TitleOpts(""),
    )
    )
from pyecharts.charts import Page
page = Page()
page.add(
         tab0("OFFICETOUCH","#2CB34A"),
         bar(),
         tab1("数据可视化大屏","#2CB34A"),
         gau(),
         radius(),
         funnel(),
         geo(),
         scatter3D()
         )
page.render("datacenter.html")
