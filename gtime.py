import datetime
import time
import re

# datetime与str转化：https://zhidao.baidu.com/question/1836089390684292660.html

class Gtime():
    def __init__(self):
        self.now = datetime.datetime.now()
        self.today = str(self.now).split(' ')[0]
        
    def addd(self,num):
        # 天数加减
        r = datetime.datetime.now()+datetime.timedelta(days=num)
        return r
    def addm(self,num):
        r = datetime.datetime.now()+datetime.timedelta(minutes=num)
        return r
    def addh(self,num):
        r = datetime.datetime.now()+datetime.timedelta(hours=num)
        return r
    def addy(self,num):
        r = datetime.datetime.now()+datetime.timedelta(years=num)
        return r
    
    def date(self,i):
        # 截取日期。输入的i为datetime对象
        return '.'.join(str(i).split(' ')[0].split('-')[1:])
    
    def clock(self):
        self.now = datetime.datetime.now()
        return self.now
        
    def festival(self,ask):
        # 获取节日的日期
        fes = {'元旦':'1.1','情人节':'2.14','妇女节':'3.8','植树节':'3.12',
            '愚人节':'4.1','劳动节':'5.1','儿童节':'6.1','建党节':'7.1',
            '建军节':'8.1','教师节':'9.10','国庆':'10.1','万圣节':'11.1',
            '光棍节':'11.11','平安夜':'12.24','圣诞':'12.25'}
        if ask in fes:
            return fes[ask]
    def when_fes(self,ask):
        # 某节日距离今天几天
        fes_date = self.festival(ask)
        if fes_date != None:
            yue = self.today.split('-')[1]
            if int(yue) <= int(fes_date.split('.')[0]):  # 下一个节日在今年
                fes = self.today.split('-')[0] + '-' + fes_date.replace('.','-')
            else:
                fes = str(int(self.today.split('-')[0])+1) + '-' + fes_date.replace('.','-')
        # t = str(self.clock()).split(' ')[1].split('.')[0]
        t = '00:00:00'
        fes_datetime = datetime.datetime.strptime(fes+' '+t,'%Y-%m-%d %H:%M:%S')
        cha = fes_datetime - self.clock()
        chaday = int(str(cha).split(' ')[0])
        chahour = str(cha).split(' ')[2].split(':')
        
        print(chahour)
        return int(str(cha).split(' ')[0]) + 1
    
    def when_date(self,ask):
        # 12.25距离今天几天
        fes_date = ask
        yue = self.today.split('-')[1]
        if int(yue) <= int(ask.split('.')[0]):  # 下一个节日在今年
            fes = self.today.split('-')[0] + '-' + ask.replace('.','-')
        else:
            fes = str(int(self.today.split('-')[0])+1) + '-' + ask.replace('.','-')
        # t = str(self.clock()).split(' ')[1].split('.')[0]
        t = '00:00:00'
        fes_datetime = datetime.datetime.strptime(fes+' '+t,'%Y-%m-%d %H:%M:%S')
        cha = fes_datetime - self.clock()
        chaday = int(str(cha).split(' ')[0])
        chahour = str(cha).split(' ')[2].split(':')
        
        print(chahour)
        return int(str(cha).split(' ')[0]) + 1
    
    def isdate(self,text):
        # 判断字符串中有无日期，若有则返回日期
        r = [0]
        form_list = [r"(\d{4}-\d{1,2}-\d{1,2})",  #2012-12-12
            r"(\d{4}/\d{1,2}/\d{1,2})",  #2012/12/12
            r"(\d{4}\.\d{1,2}\.\d{1,2})",
            r"(\d{4}年\d{1,2}月\d{1,2}日)",
            r"(\d{4}年\d{1,2}月\d{1,2}号)",
            r"(\d{4}年\d{1,2}月\d{1,2})",
            r"(\d{1,2}-\d{1,2})",
            r"(\d{1,2}/\d{1,2})",
            r"(\d{1,2}\.\d{1,2})",
            r"(\d{1,2}月\d{1,2}日)",
            r"(\d{1,2}月\d{1,2}号)",
            r"(\d{1,2}月\d{1,2})",
            ]
        for form in form_list:
            f = re.compile(form)
            num_f = re.compile(r"(\d{1,2})")
            find = re.findall(f,text)
            
            # print(f)
            if find:
                # print(find)
                nums = re.findall(num_f,find[0])
                # print(nums)
                r = [1,nums]  # list
                break
            
        return r
    
if __name__ == '__main__':
    clk = Gtime()  # Clock
    # ask = input('>>>')
    test = ['你的生日是2月29号吗',
        '1月2号的天气'
        ]
    for t in test:
        date = clk.isdate(t)
        print(date)

    # print(clk.when_date('1.2'))