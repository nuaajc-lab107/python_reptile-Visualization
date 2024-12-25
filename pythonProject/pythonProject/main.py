from flask import Flask, render_template_string
import base64
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import requests
from bs4 import BeautifulSoup
import csv
import json
from pyecharts import options as opts
from pyecharts.charts import Bar,Gauge,Pie,Page,Funnel,Geo,Scatter3D
import random
import matplotlib
matplotlib.use('Agg')
app = Flask(__name__)

def getHTMLtext(url):
    """请求获得网页内容"""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问")
        return r.text
    except:
        print("访问错误")
        return " "

def get_content(html):
    """处理得到有用信息保存数据文件"""
    final = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '7d'})
    # 获取当天的数据
    data2 = body.find_all('div', {'class': 'left-div'})
    text = data2[2].find('script').string
    text = text[text.index('=') + 1:-2]
    jd = json.loads(text)
    dayone = jd['od']['od2']
    final_day = []
    count = 0
    for i in dayone:
        temp = []
        if count <= 23:
            temp.append(i['od21'])
            temp.append(i['od22'])
            temp.append(i['od24'])
            temp.append(i['od25'])
            temp.append(i['od26'])
            temp.append(i['od27'])
            temp.append(i['od28'])
            final_day.append(temp)
        count += 1
    # 获取7天的数据
    ul = data.find('ul')
    li = ul.find_all('li')
    i = 0
    for day in li:
        if i < 7 and i > 0:
            temp = []
            date = day.find('h1').string
            date = date[0:date.index('日')]
            temp.append(date)
            inf = day.find_all('p')
            temp.append(inf[0].string)
            tem_low = inf[1].find('i').string
            if inf[1].find('span') is None:
                tem_high = None
            else:
                tem_high = inf[1].find('span').string
            temp.append(tem_low[:-1])
            if tem_high[-1] == '℃':
                temp.append(tem_high[:-1])
            else:
                temp.append(tem_high)
            wind = inf[2].find_all('span')
            for j in wind:
                temp.append(j['title'])
            wind_scale = inf[2].find('i').string
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1 - 1:index1]))
            final.append(temp)
        i += 1
    return final_day, final

def get_content2(html):
    """处理得到有用信息保存数据文件"""
    final = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '15d'})
    ul = data.find('ul')
    li = ul.find_all('li')
    i = 0
    for day in li:
        if i < 8:
            temp = []
            date = day.find('span', {'class': 'time'}).string
            date = date[date.index('（') + 1:-2]
            temp.append(date)
            weather = day.find('span', {'class': 'wea'}).string
            temp.append(weather)
            tem = day.find('span', {'class': 'tem'}).text
            temp.append(tem[tem.index('/') + 1:-1])
            temp.append(tem[:tem.index('/') - 1])
            wind = day.find('span', {'class': 'wind'}).string
            if '转' in wind:
                temp.append(wind[:wind.index('转')])
                temp.append(wind[wind.index('转') + 1:])
            else:
                temp.append(wind)
                temp.append(wind)
            wind_scale = day.find('span', {'class': 'wind1'}).string
            index1 = wind_scale.index('级')
            temp.append(int(wind_scale[index1 - 1:index1]))
            final.append(temp)
        i += 1
    return final

def write_to_csv(file_name, data, day=14):
    """保存为csv文件"""
    with open(file_name, 'a', errors='ignore', newline='') as f:
        if day == 14:
            header = ['日期', '天气', '最低气温', '最高气温', '风向1', '风向2', '风级']
        else:
            header = ['小时', '温度', '风力方向', '风级', '降水量', '相对湿度', '空气质量']
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(data)

from flask import Flask, render_template_string
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import base64
import io

app = Flask(__name__)


def tem_curve_14(data):
    """温度曲线绘制"""
    date = list(data['日期'])
    tem_low = list(data['最低气温'])
    tem_high = list(data['最高气温'])
    for i in range(0, 14):
        if math.isnan(tem_low[i]) == True:
            tem_low[i] = tem_low[i - 1]
        if math.isnan(tem_high[i]) == True:
            tem_high[i] = tem_high[i - 1]

    tem_high_ave = sum(tem_high) / 14  # 求平均高温
    tem_low_ave = sum(tem_low) / 14  # 求平均低温

    tem_max = max(tem_high)
    tem_max_date = tem_high.index(tem_max)  # 求最高温度
    tem_min = min(tem_low)
    tem_min_date = tem_low.index(tem_min)  # 求最低温度

    x = range(1, 15)
    plt.figure(1)
    plt.plot(x, tem_high, color='red', label='高温')  # 画出高温度曲线
    plt.scatter(x, tem_high, color='red')  # 点出每个时刻的温度点
    plt.plot(x, tem_low, color='blue', label='低温')  # 画出低温度曲线
    plt.scatter(x, tem_low, color='blue')  # 点出每个时刻的温度点

    plt.plot([1, 15], [tem_high_ave, tem_high_ave], c='black', linestyle='--')  # 画出平均温度虚线
    plt.plot([1, 15], [tem_low_ave, tem_low_ave], c='black', linestyle='--')  # 画出平均温度虚线
    plt.legend()
    plt.text(tem_max_date + 0.15, tem_max + 0.15, str(tem_max), ha='center', va='bottom', fontsize=10.5)  # 标出最高温度
    plt.text(tem_min_date + 0.15, tem_min + 0.15, str(tem_min), ha='center', va='bottom', fontsize=10.5)  # 标出最低温度
    plt.xticks(x)
    plt.title('未来14天高温低温变化曲线图')
    plt.xlabel('未来天数/天')
    plt.ylabel('摄氏度/℃')
    # 将图像转换为Base64编码
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data

# 未来14天风向改变函数（来自data14_analysis.py）
def change_wind_14(wind):
    """改变风向"""
    for i in range(0, 14):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
            wind[i] = 45
        elif wind[i] == "西北风":
            wind[i] = 135
        elif wind[i] == "西南风":
            wind[i] = 225
        elif wind[i] == "东南风":
            wind[i] = 315
    return wind

# 未来14天风向雷达图函数（来自data14_analysis.py）
def wind_radar_14(data):
    """风向雷达图"""
    wind1 = list(data['风向1'])
    wind2 = list(data['风向2'])
    wind_speed = list(data['风级'])
    wind1 = change_wind_14(wind1)
    wind2 = change_wind_14(wind2)

    degs = np.arange(45, 361, 45)
    temp = []
    for deg in degs:
        speed = []
        # 获取 wind_deg 在指定范围的风速平均值数据
        for i in range(0, 14):
            if wind1[i] == deg:
                speed.append(wind_speed[i])
            if wind2[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed) / len(speed))
    print(temp)
    N = 8
    theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
    # 数据极径
    radii = np.array(temp)
    # 绘制极区图坐标系
    plt.axes(polar=True)
    # 定义每个扇区的RGB值（R,G,B），x越大，对应的颜色越接近蓝色
    colors = [(1 - x / max(temp), 1 - x / max(temp), 0.6) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
    plt.title('未来14天风级图', x=0.2, fontsize=20)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data

# 未来14天天气饼图函数（来自data14_analysis.py）
def weather_pie_14(data):
    """绘制天气饼图"""
    weather = list(data['天气'])
    dic_wea = {}
    for i in range(0, 14):
        if weather[i] in dic_wea.keys():
            dic_wea[weather[i]] += 1
        else:
            dic_wea[weather[i]] = 1
    print(dic_wea)
    explode = [0.01] * len(dic_wea.keys())
    color = ['lightskyblue', 'silver', 'yellow', 'salmon', 'grey', 'lime', 'gold', 'red', 'green', 'pink']
    plt.pie(dic_wea.values(), explode=explode, labels=dic_wea.keys(), autopct='%1.1f%%', colors=color)
    plt.title('未来14天气候分布饼图')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data

# 一天温度曲线绘制函数（来自data1_analysis.py）
def tem_curve_1(data):
    """温度曲线绘制"""
    hour = list(data['小时'])
    tem = list(data['温度'])
    for i in range(0, 24):
        if math.isnan(tem[i]) == True:
            tem[i] = tem[i - 1]
    tem_ave = sum(tem) / 24  # 求平均温度
    tem_max = max(tem)
    tem_max_hour = hour[tem.index(tem_max)]  # 求最高温度
    tem_min = min(tem)
    tem_min_hour = hour[tem.index(tem_min)]  # 求最低温度
    x = []
    y = []
    for i in range(0, 24):
        x.append(i)
        y.append(tem[hour.index(i)])
    plt.figure(1)
    plt.plot(x, y, color='red', label='温度')  # 画出温度曲线
    plt.scatter(x, y, color='red')  # 点出每个时刻的温度点
    plt.plot([0, 24], [tem_ave, tem_ave], c='blue', linestyle='--', label='平均温度')  # 画出平均温度虚线
    plt.text(tem_max_hour + 0.15, tem_max + 0.15, str(tem_max), ha='center', va='bottom', fontsize=10.5)  # 标出最高温度
    plt.text(tem_min_hour + 0.15, tem_min + 0.15, str(tem_min), ha='center', va='bottom', fontsize=10.5)  # 标出最低温度
    plt.xticks(x)
    plt.legend()
    plt.title('一天温度变化曲线图')
    plt.xlabel('时间/h')
    plt.ylabel('摄氏度/℃')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data

# 一天相对湿度曲线绘制函数（来自data1_analysis.py）
def hum_curve_1(data):
    """相对湿度曲线绘制"""
    hour = list(data['小时'])
    hum = list(data['相对湿度'])
    for i in range(0, 24):
        if math.isnan(hum[i]) == True:
            hum[i] = hum[i - 1]
    hum_ave = sum(hum) / 24  # 求平均相对湿度
    hum_max = max(hum)
    hum_max_hour = hour[hum.index(hum_max)]  # 求最高相对湿度
    hum_min = min(hum)
    hum_min_hour = hour[hum.index(hum_min)]  # 求最低相对湿度
    x = []
    y = []
    for i in range(0, 24):
        x.append(i)
        y.append(hum[hour.index(i)])
    plt.figure(2)
    plt.plot(x, y, color='blue', label='相对湿度')  # 画出相对湿度曲线
    plt.scatter(x, y, color='blue')  # 点出每个时刻的相对湿度
    plt.plot([0, 24], [hum_ave, hum_ave], c='red', linestyle='--', label='平均相对湿度')  # 画出平均相对湿度虚线
    plt.text(hum_max_hour + 0.15, hum_max + 0.15, str(hum_max), ha='center', va='bottom', fontsize=10.5)  # 标出最高相对湿度
    plt.text(hum_min_hour + 0.15, hum_min + 0.15, str(hum_min), ha='center', va='bottom', fontsize=10.5)  # 标出最低相对湿度
    plt.xticks(x)
    plt.legend()
    plt.title('一天相对湿度变化曲线图')
    plt.xlabel('时间/h')
    plt.ylabel('百分比/%')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data

# 一天空气质量曲线绘制函数（来自data1_analysis.py）
def air_curve_1(data):
    """空气质量曲线绘制"""
    hour = list(data['小时'])
    air = list(data['空气质量'])
    for i in range(0, 24):
        if math.isnan(air[i]) == True:
            air[i] = air[i - 1]
    air_ave = sum(air) / 24  # 求平均空气质量
    air_max = max(air)
    air_max_hour = hour[air.index(air_max)]  # 求最高空气质量
    air_min = min(air)
    air_min_hour = hour[air.index(air_min)]  # 求最低空气质量
    x = []
    y = []
    for i in range(0, 24):
        x.append(i)
        y.append(air[hour.index(i)])
    plt.figure(3)
    for i in range(0, 24):
        if y[i] <= 50:
            plt.bar(x[i], y[i], color='lightgreen', width=0.7)  # 1等级
        elif y[i] <= 100:
            plt.bar(x[i], y[i], color='wheat', width=0.7)  # 2等级
        elif y[i] <= 150:
            plt.bar(x[i], y[i], color='orange', width=0.7)  # 3等级
        elif y[i] <= 200:
            plt.bar(x[i], y[i], color='orangered', width=0.7)  # 4等级
        elif y[i] <= 300:
            plt.bar(x[i], y[i], color='darkviolet', width=0.7)  # 5等级
        elif y[i] > 300:
            plt.bar(x[i], y[i], color='maroon', width=0.7)  # 6等级
    plt.plot([0, 24], [air_ave, air_ave], c='black', linestyle='--')  # 画出平均空气质量虚线
    plt.text(air_max_hour + 0.15, air_max + 0.15, str(air_max), ha='center', va='bottom', fontsize=10.5)  # 标出最高空气质量
    plt.text(air_min_hour + 0.15, air_min + 0.15, str(air_min), ha='center', va='bottom', fontsize=10.5)  # 标出最低空气质量
    plt.xticks(x)
    plt.title('一天空气质量变化曲线图')
    plt.xlabel('时间/h')
    plt.ylabel('空气质量指数AQI')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data

# 一天风向雷达图函数（来自data1_analysis.py）
def wind_radar_1(data):
    """风向雷达图"""
    wind = list(data['风力方向'])
    wind_speed = list(data['风级'])
    for i in range(0, 24):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
             wind[i] = 45
        elif wind[i] == "西北风":
            wind[i] = 135
        elif wind[i] == "西南风":
            wind[i] = 225
        elif wind[i] == "东南风":
            wind[i] = 315
    degs = np.arange(45, 361, 45)
    temp = []
    for deg in degs:
        speed = []
        # 获取 wind_deg 在指定范围的风速平均值数据
        for i in range(0, 24):
            if wind[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed) / len(speed))
    print(temp)
    N = 8
    theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
    # 数据极径
    radii = np.array(temp)
    # 绘制极区图坐标系
    plt.axes(polar=True)
    # 定义每个扇区的RGB值（R,G,B），x越大，对应的颜色越接近蓝色
    colors = [(1 - x / max(temp), 1 - x / max(temp), 0.6) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
    plt.title('一天风级图', x=0.2, fontsize=20)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data
def calc_corr(a, b):
    """计算相关系数"""
    a_avg = sum(a) / len(a)
    b_avg = sum(b) / len(b)
    cov_ab = sum([(x - a_avg) * (y - b_avg) for x, y in zip(a, b)])
    sq = math.sqrt(sum([(x - a_avg) ** 2 for x in a]) * sum([(x - b_avg) ** 2 for x in b]))
    corr_factor = cov_ab / sq
    return corr_factor


def corr_tem_hum_1(data):
    """温湿度相关性分析"""
    tem = data['温度']
    hum = data['相对湿度']
    plt.scatter(tem, hum, color='blue')
    plt.title("温湿度相关性分析图")
    plt.xlabel("温度/℃")
    plt.ylabel("相对湿度/%")
    plt.text(20, 40, "相关系数为：" + str(calc_corr(tem, hum)), fontdict={'size': '10', 'color': 'red'})
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    return img_data


@app.route('/')
def index():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 读取未来14天天气数据文件
    data14 = pd.read_csv('weather14.csv', encoding='gb2312')
    tem_img_data_14 = tem_curve_14(data14)
    wind_img_data_14 = wind_radar_14(data14)
    pie_img_data_14 = weather_pie_14(data14)

    # 读取一天天气数据文件
    data1 = pd.read_csv('weather1.csv', encoding='gb2312')
    tem_img_data_1 = tem_curve_1(data1)
    hum_img_data_1 = hum_curve_1(data1)
    air_img_data_1 = air_curve_1(data1)
    wind_img_data_1 = wind_radar_1(data1)
    corr_img_data_1 = corr_tem_hum_1(data1)

    return render_template_string("""
    <html>
    
        <head>
            <title>宿迁学院天气数据可视化</title>
        </head>
        <body>
            <h1>宿迁学院未来14天天气数据可视化</h1>
            <img src="data:image/png;base64,{{ tem_img_data_14 }}" alt="未来14天温度变化曲线">
            <img src="data:image/png;base64,{{ wind_img_data_14 }}" alt="未来14天风向雷达图">
            <img src="data:image/png;base64,{{ pie_img_data_14 }}" alt="未来14天天气饼图">

            <h1>宿迁学院一天天气数据可视化</h1>
            <img src="data:image/png;base64,{{ tem_img_data_1 }}" alt="一天温度变化曲线">
            <img src="data:image/png;base64,{{ hum_img_data_1 }}" alt="一天相对湿度变化曲线">
            <img src="data:image/png;base64,{{ wind_img_data_1 }}" alt="一天风向雷达图">
            <img src="data:image/png;base64,{{ corr_img_data_1 }}" alt="温湿度相关性分析图">
        </body>
    </html>
    """, tem_img_data_14=tem_img_data_14, wind_img_data_14=wind_img_data_14, pie_img_data_14=pie_img_data_14,
           tem_img_data_1=tem_img_data_1, hum_img_data_1=hum_img_data_1, air_img_data_1=air_img_data_1,
           wind_img_data_1=wind_img_data_1, corr_img_data_1=corr_img_data_1)


if __name__ == '__main__':
    app.run(debug=True)

