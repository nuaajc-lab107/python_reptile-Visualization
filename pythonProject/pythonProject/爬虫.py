import requests  # 发送请求
from bs4 import BeautifulSoup  # 解析网页
import pandas as pd  # 存取csv
movie_name = []  # 电影名称
movie_url = []  # 电影链接
movie_star = []  # 电影评分
movie_star_people = []  # 评分人数
movie_director = []  # 导演
movie_actor = []  # 主演
movie_year = []  # 上映年份
movie_country = []  # 国家
movie_type = []  # 类型
short_comment = []  # 一句话短评
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
for movie in soup.select('.item'):
	name = movie.select('.hd a')[0].text.replace('\n', '')  # 电影名称
	movie_name.append(name)
	url = movie.select('.hd a')[0]['href']  # 电影链接
	movie_url.append(url)
	star = movie.select('.rating_num')[0].text  # 电影评分
	movie_star.append(star)
	star_people = movie.select('.star span')[3].text  # 评分人数
	star_people = star_people.strip().replace('人评价', '')
	movie_star_people.append(star_people)