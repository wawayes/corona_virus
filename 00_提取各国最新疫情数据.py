# 导入相关模块
import json

import requests
from bs4 import BeautifulSoup
import re

# 发送请求，获取疫情首页数据
response = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')

home_page = response.content.decode()

# print(home_page)

# 使用BeautifulSoup提取疫情数据
soup = BeautifulSoup(home_page, 'lxml')

script = soup.find(id='getAreaStat')
text = script.text
# print(text)

# 使用正则表达式，提取json字符串
json_str = re.findall(r'(\[.+\])', text)[0]
# print(json_str)

# 把json字符串转为python类型的数据
last_day_corona_virus = json.loads(json_str)
print(last_day_corona_virus)

