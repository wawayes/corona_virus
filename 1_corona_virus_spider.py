# 导入模块
import re
import requests
import json
from bs4 import BeautifulSoup
# 发送请求，获取响应数据
response = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')
home_page = response.content.decode()
# print(home_page)
# 用BeautifulSoup提取疫情数据
soup = BeautifulSoup(home_page, 'lxml')

script = soup.find(id='getAreaStat')
text = script.text
# print(text)
# 使用正则表达式，提取json
json_str = re.findall(r'\[.+\]', text)[0]

# 将json转为python类型存储
corona_virus_spider = json.loads(json_str)
print(corona_virus_spider)

# 以json格式保存数据
with open('./data/corona_virus_spider.json', 'w') as fp:
    json.dump(corona_virus_spider, fp, ensure_ascii=False)
