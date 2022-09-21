# 导入模块
import re
import requests
import json
from tqdm import tqdm
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

    def parse_home_page(self, home_page, tag_id):
        """
        解析首页内容，获取python数据
        :param tag_id:
        :param home_page: 首页的内容
        :return: python类型数据
        """
        # print(home_page)
        # 用BeautifulSoup提取疫情数据
        soup = BeautifulSoup(home_page, 'lxml')
        script = soup.find(id=tag_id)
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
        last_day_corona_virus = self.parse_home_page(home_page, tag_id='statisticsData')
        # 保存数据
        self.save(last_day_corona_virus, './data/last_day_corona_virus.json')

    def craw_corona_virus(self):
        """
        采集从1月23日以来的疫情信息
        :return:
        """
        # 加载各国疫情数据
        with open('./data/last_day_corona_virus.json') as fp:
            last_day_corona_virus = json.load(fp)
        corona_virus = []
        # print(last_day_corona_virus)
        for country in tqdm(last_day_corona_virus, '1月23日以来疫情信息'):
        # for country in last_day_corona_virus:
            statistics_data_url = country['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            # print(statistics_data_json_str)
            # 把json数据转换为python数据类型保存到列表中
            statistics_data = json.loads(statistics_data_json_str)['data']
            # print(statistics_data)
            for one_day in statistics_data:
                one_day['provinceName'] = country['provinceName']
                # one_day['countryShortCode'] = country['countryShortCode']
            corona_virus.extend(statistics_data)

        self.save(corona_virus, './data/corona_virus.json')

    def craw_last_day_corona_virus_of_china(self):
        """
        采集最近一日各省疫情信息
        :return:
        """
        home_page = self.get_content_from_url(self.home_url)
        craw_last_day_corona_virus_of_china = self.parse_home_page(home_page, tag_id='getAreaStat')
        self.save(craw_last_day_corona_virus_of_china, './data/craw_last_day_corona_virus_of_china.json')

    def run(self):
        # self.craw_last_corona_virus()
        # self.craw_corona_virus()
        self.craw_last_day_corona_virus_of_china()

if __name__ == '__main__':
    spider = CoronaVirusSpider()
    spider.run()
