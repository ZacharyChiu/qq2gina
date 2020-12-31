# 参考：https://blog.csdn.net/sl01224318/article/details/110264107

import re
import os
import requests
import time
import random
from bs4 import BeautifulSoup as bs


class Huaban():
    def __init__(self):
        self.PhotoNum = 0
        self.head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        self.TimeOut = 30
        self.buff = '?iqkxaeyv&limit=200&wfl=1&max='
        self.url_image = "http://hbimg.b0.upaiyun.com/"
        self.result = []
        

    def get_source(self,a):
        with open('picSpace.xml','r',encoding='utf-8') as f:
            xml = bs(f.read(),'html.parser')
        beauty = eval(xml.fresh.string)['beauty']
        myfeed = eval(xml.fresh.string)['myfeed']
        uiti = eval(xml.mypin.string)['uiti']  #list
        try:
            return eval(a)
        except Exception as e:
            print(e)  # 关键词错误
            return 'https://huaban.com/discovery/beauty/'

    def requestUrl(self,url,lenth=1000):
        Page = requests.session().get(url, headers=self.head, timeout=self.TimeOut)
        Page.encoding = "utf-8"
        text = Page.text
        pattern = re.compile('{"pin_id":(\d*?),.*?"key":"(.*?)",.*?"like_count":(\d*?),.*?"repin_count":(\d*?),.*?}', re.S)
        items = re.findall(pattern, text)
        # print(items)
        max_pin_id = 0
        for item in items:
            max_pin_id = item[0]
            x_key = item[1]
            x_like_count = int(item[2])
            x_repin_count = int(item[3])
           
            url_item = self.url_image + x_key  # 图片链接地址
            # print(url_item)
            if len(self.result) < lenth:
                self.result.append(url_item)
            else:
                max_pin_id = 0
                break
            self.PhotoNum += 1
        if max_pin_id != 0:
            self.requestUrl(self.urlNext + str(max_pin_id))
        else:
            print('')
    def run(self,ask,lenth=1000):
        self.result = []
        self.url = self.get_source(ask)
        if type(self.url) == list:
            for u in self.url:
                self.urlNext = u + self.buff
                self.requestUrl(u,lenth=lenth)
        else:
            self.urlNext = self.url + self.buff
            self.requestUrl(self.url,lenth=lenth)
        return self.result

class Moji():
    def __init__(self):
        self.url = "https://tianqi.moji.com/forecast15/china/jiangsu/yixing"
        self.wea15 = self.get15wea()
        
    def get15wea(self):
        head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        TimeOut = 30
        ans = []
        Page = requests.session().get(self.url, headers=head, timeout=TimeOut)
        Page.encoding = "utf-8"
        self.html = bs(Page.text,'html.parser')
        weather_block = self.html.find_all('div',class_='wea_list clearfix')[0]
        weather_bar = weather_block.ul.find_all('li')
        for i in weather_bar:
            day = i.find_all('span',class_='week')  #[星期, 日期]
            week = day[0].string
            date = day[1].string
            weather = i.find_all('span',class_='wea')  # [0] 转 [1]
            wen = i.find_all('div',class_='tree clearfix')[0].p
            wen_1 = wen.b.string  # 最高温
            wen_0 = wen.strong.string  # 最低温
            if len(set(weather)) == len(weather):
                wea = weather[0].string + '转' + weather[1].string
            else:
                wea = weather[0].string
            
            info = [date,week,wea,wen_1,wen_0]
            
            ans.append(info)
            # print(info)
            # print('='*20)
        return ans

class City():
    def __init__(self):
        self.url = 'http://xzqh.mca.gov.cn/map'
    def get_citys(self):
        head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        TimeOut = 30
        ans = []
        Page = requests.get(self.url, headers=head, timeout=TimeOut)
        Page.encoding = "GBK"  # 注意网页源代码header中的编码方式。这里用utf-8显示不出中文
        self.html = bs(Page.text,'html.parser')
        aa = self.html.find_all('table',class_='select_table')[1]
        bb = aa.find_all('input',id="pyArr")[0].attrs
        citys = eval(bb['value'])  # list
        cc = []
        for i in citys:
            cc.append(i['cName'])
        return cc
    def province(self,p):
        citys = self.get_citys()
        for i in citys:
            if p in i['cName']:
                p_0 = citys.index(i)
                # print('start:%d'%p_0)
                for j in citys[p_0+1:]:
                    if '省' in j['cName']:
                        p_1 = citys.index(j)
                        # print('end:%d'%p_1)
                        break
        return citys[p_0:p_1]

def web_order():
    url = 'https://huaban.com/boards/66843722/'
    head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    TimeOut = 30
    ans = []
    Page = requests.session().get(url, headers=head, timeout=TimeOut)
    Page.encoding = "utf-8"
    html = bs(Page.text,'html.parser')
    title = html.head.title.string
    order = title.split('_')[0].split('(')[0]
    return order


if __name__ == '__main__':
    city = City().get_citys()
    
    print(city)
   