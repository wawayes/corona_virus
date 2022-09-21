# 导入模块
import re
import requests
import json
from bs4 import BeautifulSoup


class CoronaVirusSpider(object):
    def __init__(self):
        self.home_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'

    def get_content_from_url(self, url):
        """
        根据URL，获取响内容的字符串数据
        :param url:请求的url
        :return
        """
        # 发送请求，获取响应数据
        response = requests.get(url)
        return response.content.decode()

    def parse_home_page(self, home_page):
        """
        解析首页内容，获取python数据
        :param home_page: 首页的内容
        :return: python类型数据
        """
        # print(home_page)
        # 用BeautifulSoup提取疫情数据
        soup = BeautifulSoup(home_page, 'lxml')
        script = soup.find(id='getAreaStat')
        text = script.text
        # print(text)
        # 使用正则表达式，提取json
        json_str = re.findall(r'\[.+\]', text)[0]
        # 将json转为python类型存储
        data = json.loads(json_str)
        return data

    def save(self,data, path):
        # 以json格式保存数据
        with open(path, 'w') as fp:
            json.dump(data, fp, ensure_ascii=False)

    def craw_last_corona_virus(self):
        """
        采集最近一天的各国疫情信息
        :return:
        """
        home_page = self.get_content_from_url(self.home_url)
        last_day_corona_virus = self.parse_home_page(home_page)
        # 保存数据
        self.save(last_day_corona_virus, './data/corona_virus_spider.json')

    def run(self):
        self.craw_last_corona_virus()


if __name__ == '__main__':
    spider = CoronaVirusSpider()
    spider.run()
