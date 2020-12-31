# -*- coding = utf-8 -*-
# Author: Zachary
# @Time: 2020/10/4 16:43

import os
import psutil
# import pygame
# from mutagen.mp3 import MP3
import time
import datetime
import jieba.posseg as psg
import requests
from bs4 import BeautifulSoup as bs
import random
import re
import json

import chatme
import ghuman
import spider
import gtime


# jieba去除提示内容：
# 到jieba目录下：C:\Users\111\Anaconda3\Lib\site-packages\jieba
# 把jieba的__init__.py中约28行处【default_logger.setLevel(logging.DEBUG)】改为【default_logger.setLevel(logging.INFO)】


# def play_music(path,f=16000):
    # pygame.mixer.init(frequency=f)
    # pygame.mixer.music.load(path)
    # pygame.mixer.music.play()

def whatrun():
    pids = psutil.pids()
    names = []
    for pid in pids:
        p = psutil.Process(pid)
        names.append(p.name())
    return set(names)

def find_cq(text):
    form = re.compile(r'(\[CQ:(\S)+=(\S)+\])')
    r = re.findall(form,text)
    
    result = []
    for i in r:
        result.append(i[0])
    return (result)
    

class QQ():
    def __init__(self):
        self.api = 'http://127.0.0.1:7700/'
        self.sdpapi = self.api + 'send_private_msg'
        self.sdgapi = self.api + 'send_group_msg'
    def sd_p_msg(self,qq,msg):
        params = {
            "user_id": qq,
            "message": msg}
        response = requests.post(self.sdpapi, data=json.dumps(params), headers={'Content-Type': 'application/json'})
        print(response.text)
        return response
    def sd_g_msg(qq,msg):
        params = {
            "group_id": qq,
            "message": msg}
        response = requests.post(self.sdgapi, data=json.dumps(params), headers={'Content-Type': 'application/json'})
        print(response.text)
        return response


class Readed():
    def __init__(self):
        try:
            with open('readed.temp','r',encoding='utf-8') as f:
                text = f.read()
                self.dic = eval(text)
        except:
            with open('readed.temp','w',encoding='utf-8') as f:
                text = f.write("{'status':'sleep','readed':''}")
                self.dic = {'readed':''}
    def readed(self,s):
        if self.dic['readed'] == s:
            return 1
        else:
            return 0
    def update(self):
        try:
            with open('readed.temp','r',encoding='utf-8') as f:
                text = f.read()
                self.dic = eval(text)
        except:
            with open('readed.temp','w',encoding='utf-8') as f:
                text = f.write("{'status':'empty','readed':''}")
                self.dic = {'readed':''}
    def write(self,text='',status='0'):
        if text == '':
            text = self.dic['readed']
        if status == '0':
            status = self.dic['status']
        d = {'status':status,'readed':text}
        with open('readed.temp','w',encoding='utf-8') as f:
            text = f.write(str(d))
            
            
class MsgID():
    def __init__(self,msgid='0'):
        self.id = msgid
        self.msg = ''
        logs = os.listdir('logs')
        today_log = str(datetime.datetime.now()).split(' ')[0]+'.log'
        if today_log in logs:
            with open('logs\\'+today_log,'r',encoding='utf-8') as f:
                ls = f.readlines()
        else:
            ls = []
        self.logs = []  
        for i in ls:
            try:
                if i.strip()[-1] == ')':
                    self.logs.append(i)  # 获取今天的日志中所有消息行（列表形式）
            except:
                pass
        if self.logs == []:
            self.nologs = 1
        else:
            self.nologs = 0
        self.rcv = []
        self.send = []
        for i in self.logs:
            try:
                if i.split('[INFO]:')[1].strip()[:2] == '收到':
                    self.rcv.append(i)
                elif i.split('[INFO]:')[1].strip()[:2] == '发送':
                    self.send.append(i)
            except:
                pass
        if self.id == '0':
            try:
                self.id = self.logs[-1].split('(')[-1].strip()[:-1]
            except:
                pass
        # print('id:%s'%self.id)
        for line in self.logs:
            msg_id = line.split('(')[-1][:-3].strip()
            if self.id == msg_id:
                self.msg = line  # 该id对应的消息（完整信息）
                    
        self.time = self.msg.split(']')[0][1:]  #消息时间
        self.msgtype = self.msg.split('[INFO]:')[-1].strip()[2:].split(' ')[0]  # 私聊还是群聊
        if self.msgtype == '好友':
            self.sduser = self.msg.split('[INFO]:')[-1].strip().split(' ')[1]  # QQ昵称(QQ号)
            self.sdname = self.sduser.split('(')[0]
            self.sdid = self.sduser.split('(')[-1][:-1]
            self.text = ':'.join(self.msg.split(':')[4:]).split('('+self.id+')')[0][1:-1]
        elif self.msgtype == '群':
            self.sdqun = self.msg.split('[INFO]:')[-1].strip().split(' ')[1]  # WON(1039564640)
            self.sdqunname = self.sdqun.split('(')[0]
            self.sdqunid = self.sdqun.split('(')[-1][:-1]
            
            self.sduser = self.msg.split('[INFO]:')[-1].strip().split(' ')[3]  # QQ昵称(QQ号)
            self.sdname = self.sduser.split('(')[0]
            self.sdid = self.sduser.split('(')[-1][:-1]
            
            self.text = ':'.join(self.msg.split(':')[4:]).split('('+self.id+')')[0][1:-1]
            # print('TEXT##%s##'%self.text)
        else:
            self.text = ''
        # 消息分类
        cqcodes = find_cq(self.text)
        self.cq = 0
        if self.text[:3] == 'gg$':
            self.texttype = '命令'
            self.order = ''.join(self.text.split('gg$')[1:])
        elif cqcodes:  # 消息中有CQ码
            self.cq = 1
            if len(cqcodes) == 1:
                self.cqtype = cqcodes[0].split(' ')[0].split(',')[0][4:]
                self.cqfile = cqcodes[0].split(' ')[0].split(',')[1][:-1]
                if cqcodes[0] == self.text:  # 单纯CQ码
                    if self.cqtype == 'image':
                        self.texttype = '图片消息'
                    elif self.cqtype == 'at':
                        self.cqtype == 'atsb'  # just at somebody
                        atit = self.cqfile.split('=')[-1]
                        if atit == '2140911591':
                            it = '姬娜'
                        elif atit == '1563382991':
                            it = '超哥'
                        else:
                            it = '('+atit+')'
                        self.texttype = '@ ' + it
                    elif self.cqtype == 'face':
                        self.texttype = 'QQ表情'
                    elif self.cqtype == 'record':
                        self.texttype = '语音消息'
                    elif self.cqtype == 'redbag':
                        self.texttype = '红包'
                    elif self.cqtype == 'redbag':
                        self.texttype = '红包'
                    elif self.cqtype == 'video':
                        self.texttype = '视频消息'
                else:
                    if self.cqtype == 'at':
                        atit = self.cqfile.split('=')[-1]
                        if atit == '2140911591':
                            it = '姬娜'
                        elif atit == '1563382991':
                            it = '超哥'
                        else:
                            it = '('+atit+')'
                        self.texttype = '@' + it
                        self.text = ''.join(self.text.split(cqcodes[0]+' '))
                    else:
                        self.texttype = '复合消息'
                    
        else:
            self.texttype = '普通对话'
    def get_id(self,one_line):
        return one_line.split('(')[-1].strip()[:-1]
    
    def update(self,newid='0'):
        self.__init__(newid)
        return self.logs

def do(ask):
    asks = ask.split(' ')
    try:
        if asks[0] == 'kill':
            return 'taskkill /f /t /im ' + 'go-cqhttp.exe'
        else:
            return '听不懂你在说什么...'
    except Exception as e:
        print(e.args)

class Require():
    def __init__(self,sentence):
        self.require = []
        self.s = sentence.strip()
    
    def showpic(self):
        freshpic = ['骚图','靓图']
        uitipic = ['实体','美女','妹子','来点妹子','给点颜色','来点颜色','给点颜色我瞧瞧','给我点颜色瞧瞧']
        tu = 0
        if '图' in self.s:
            tu = 1
        if self.s in freshpic:
            return [1,'fresh']
        elif self.s in uitipic:
            return [1,'uiti']
        else:
            return [0,'']
    
    def whois(self):
        seg = dict(psg.cut(self.s.strip()))
        ren = 0
        wen = 0
        man = []
        element = ['吗','谁','哪','几','什么']
        # print(seg)
        for k,v in seg.items():
            if 'nr' in str(v):
                # print(self.s,end='')
                man.append(k)
                ren = 1
        for i in element:
            if i in self.s:
                wen = 1
        return [ren and wen,''.join(man)]
    def weather(self):
        seg = dict(psg.cut(self.s.strip()))
        t = []
        w = ['天气','温度','气温','几度']
        tt = ['大后天']  # 未识别时间名词补充
        shi = 0
        tian = 0
        for k,v in seg.items():
            if 't' in str(v):
                # print(self.s,end='')
                t.append(k)
                shi = 1  # 出现时间名词
            else:
                for i in tt:
                    if i in self.s:
                        shi = 1
                        t = [i]
        for i in w:
            if i in self.s:
                tian = 1
        if tian:
            if shi:
                return [1,1,t]
            else:
                return [1,0,t]
        else:
            return [0,0,[]]
    
    def run(self):
        # 判断意图
        if self.s == '鸡汤':
            print('【诉求判断器】想喝鸡汤...')
            return 'jith'
        elif self.showpic()[0] == 1:
            print('【诉求判断器】索要图片...')
            return ['showpic',self.showpic()[1]]
        elif self.whois()[0] == 1:
            return ['whois',self.whois()[1]]
            print('【诉求判断器】询问人物...')
        elif self.weather()[0] == 1:
            print('【诉求判断器】询问天气...')
            return ['weather',self.weather()[1],self.weather()[2]]
        else:
            print('【诉求判断器】瞎叽霸聊...')
def gfun(ask):
    # 输入文本和诉求,输出回复
    require = Require(ask).run()
    print('Require: %s'%require)
    if require == 'jith':
        # 毒鸡汤
        url = 'http://www.nows.fun'
        head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        TimeOut = 30
        Page = requests.session().get(url, headers=head, timeout=TimeOut)
        Page.encoding = "utf-8"
        text = Page.text
        html = bs(text,"html.parser")
        res = html.find_all(id='sentence')[0].string
        return res
    
        
    elif type(require) == type([]):
        if require[0] == 'whois':
            name = require[1]  # 想要认识的人的名字
            users = ghuman.People()  # 导入人物库
            who = users.find(name)  # 根据名字找到Ta的资料
            res = users.produce(name)
            return res
        elif require[0] == 'showpic':
            # 发点图片
            hua = spider.Huaban()  # 导入花瓣网爬取工具
            if require[1] == 'fresh':
                urls = hua.run('beauty')  # 选择使用哪一个主题的图片集
            elif require[1] == 'uiti':
                urls = hua.run('uiti')
            index = random.randint(0,len(urls)-1)  # 从图库中随机抽取一张
            res = '[CQ:image,file='+urls[index]+']'  # 封装CQ码
            return res
        elif require[0] == 'weather':
            clk = gtime.Gtime()  # 导入姬娜的生物钟
            wea15 = spider.Moji().wea15  # 获取墨迹15天天气
            # 数据结构为 [日期，星期，天气，最高温，最低温]
            date = clk.date(clk.now)  # 今天日期'12/25'
            
            if require[1] == 1:  # 询问某天天气
                time_dic = {'今天':1,'现在':1,'明天':2,'后天':3,'大后天':4}
                fes_list = fes = ['元旦','情人节','妇女节','植树节','愚人节','劳动节',
                '儿童节','建党节','建军节','教师节','国庆','万圣节','光棍节',
                    '平安夜','圣诞']
                
                clk = gtime.Gtime()
                
                
                if require[2]:
                    t = require[2][0]  # 询问的时间
                    print('时间：',t)
                    if t in time_dic:  # 今明后
                        now_wea = wea15[time_dic[t]]
                        info = '%s是%s月%s日，%s，%s，最低温度%s，最高温度%s。'%(t,now_wea[0].split('/')[0],now_wea[0].split('/')[1],now_wea[1],now_wea[2],now_wea[4],now_wea[3])
                        print(now_wea)
                        return info
                    elif t in fes_list:  # 节日
                        index = clk.when_fes(t)
                        now_wea = wea15[index+1]
                        info = '%s是%s月%s日，%s，%s，最低温度%s，最高温度%s。'%(t,now_wea[0].split('/')[0],now_wea[0].split('/')[1],now_wea[1],now_wea[2],now_wea[4],now_wea[3])
                        print(now_wea)
                        return info
                
            elif require[1] == 0:  # 询问天气
                isdate = clk.isdate(ask)
                print(isdate)
                if isdate[0] == 1:
                    t = isdate[1]
                    index = clk.when_date(t[0]+'.'+t[1])
                    now_wea = wea15[index+1]
                    info = '%s月%s日，%s，%s，最低温度%s，最高温度%s。'%(t[0],t[1],now_wea[1],now_wea[2],now_wea[4],now_wea[3])
                    print(now_wea)
                    return info
                else:    
                    now_wea = wea15[1]
                    info = '今天是%s月%s日，%s，%s，最低温度%s，最高温度%s。'%(now_wea[0].split('/')[0],now_wea[0].split('/')[1],now_wea[1],now_wea[2],now_wea[4],now_wea[3])
                    print(now_wea)
                    return info
    
    else:
        return chatme.chat(ask)  # 排除所有功能诉求后,剩下闲聊

if __name__ == '__main__':
    # test_list = ['元旦的天气',
        # '天气',
        # '元旦是几月几号',
        # '距离元旦还有几天',
        # '中秋的天气怎么样',
        # '元旦是什么时候']
    # for i in test_list:
        # # ans = Require(i).run()
        # ans = gfun(i)
        # print(ans)
        # print('\n')
    print('\n'.join(whatrun()))
