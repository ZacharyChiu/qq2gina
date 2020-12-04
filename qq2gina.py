# -*- coding = utf-8 -*-
# Author: Zachary
'''
通过QQ向姬娜发送命令
'''
import os 
import re 
import datetime
import csv
import pygame
import requests
import json
import chatme
import gfun_air
# import Ali_TTS as tts

def play_music(path,f=16000):
    pygame.mixer.init(frequency=f)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    
def kill_biaodian(s):
    # 去掉所有标点
    punc = '~`!#$%^&*()_+-=|\';“”:/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》《{}'
    return re.sub(r"[%s]+" %punc, "",s)

def have_speech(s):
    # 检测日志中是否已经含有此语音文件，如果有，返回文件名编号
    have = []
    name = False
    with open('tts_recoder.csv','r',encoding='utf-8') as f:
        rows = f.readlines()[1:]
    print('rows:',rows)
    for b in rows:
        body = b.split(',')[-1].strip()
        have.append(kill_biaodian(body))
    print('have:',have)
    if kill_biaodian(s) in have:
        index = have.index(kill_biaodian(s))
        name = rows[index].split(',')[0]
    return name

def get_time():
    cur_time = datetime.datetime.now()  # 数据类型为：datetime
    now = str(cur_time).split('.')[0]
    date = ''.join(now.split(' ')[0].split('-'))
    time = ''.join(now.split(' ')[1].split(':'))
    t = date + time
    return t

def get_msg():
    logs = os.listdir('logs')
    today_log = str(datetime.datetime.now()).split(' ')[0]+'.log'
    if today_log in logs:
        with open('logs/'+today_log,'r',encoding='utf-8') as f:
            log = f.read()
        sd = re.findall(r'发送.*的消息.*.*',log)
        rcv = re.findall(r'收到.*的消息.*.*',log)
        return [rcv,sd]
    else:
        print('今天的日志特么没找到...')

def sd_p_msg(qq,msg):
	url = 'http://127.0.0.1:5700/send_private_msg'
	params = {
		"user_id": qq,
		"message": msg}
	response = requests.post(url, data=json.dumps(params), headers={'Content-Type': 'application/json'})
	print(response.text)
	return response
def sd_g_msg(qq,msg):
	url = 'http://127.0.0.1:5700/send_group_msg'
	params = {
		"group_id": qq,
		"message": msg}
	response = requests.post(url, data=json.dumps(params), headers={'Content-Type': 'application/json'})
	print(response.text)
	return response

def what(text):
    sh = re.findall(r'到.*的',text)
    who = sh[0][1:-1]
    id_ = who.split('(')[-1][:-2]
    name = who.split('(')[0].split(' ')[-1]
    msg = text.split(': ')[-1].strip()
    return [name,id_,msg]
# resp = sd_p_msg(1563382991,"Zac")
# rsp = sd_msg(1039564640,"here")

def readed(s):
    with open('readed.txt','r',encoding='utf-8') as f:
        readed = f.read()
    if readed == s:
        return True
    else:
        return False
rcv_msg = []
rcv = get_msg()[0]
# for i in rcv:
    # print('rcv:',i)
    
# if rcv != rcv_msg: # 有新消息
    # rcv_msg = rcv[:]
    # latest = rcv_msg[-1]
    # content = what(latest)
    # print(content)
    # print('#%s#'%' '.join(content[-1].split(' ')[:-1]))

# os.system('start go-cqhttp-v0.9.32-windows-amd64.exe')

while 1:
    if rcv != rcv_msg: # 有新消息
        
        rcv_msg = rcv[:]
        latest = rcv_msg[-1]
        content = what(latest)
        if '群' not in latest:
            # 个人消息
            print('#%s#'%' '.join(content[-1].split(' ')[:-1]))
            print('='*20)
            if not readed(content[-1]):
                if content[1] == '1563382991':
                    # 来自Zac
                    if content[-1][:4] == 'gg$ ':
                        order = ' '.join(content[-1].split('gg$ ')[-1].split(' ')[:-1])
                        print('控制台：%s'%order)
                        if order[:4] == 'sys ':
                            os.system(order.split('sys ')[-1])
                        else:
                            print('>>>获到超哥的【命令行】！')
                            r = gfun_air.do(order)
                            print('$ 姬娜:', r, '\n')
                            sd_p_msg(1563382991,r)
                            with open('readed.txt','w',encoding='utf-8') as f:
                                f.write(content[-1])
                            
                    elif content[-1][:4] == '[CQ:':
                        print('>>>捕获到【CQ码】！')
                        
                    else:
                        print('>>>捕获到【普通对话】！')
                        name = 'tts_logs/'+str(get_time()) + '.mp3'
                        ans = chatme.chat(' '.join(content[-1].split(' ')[:-1]))
                        # ans = '...'
                        print('$ 姬娜:', ans, '\n')
                        sd_p_msg(1563382991,ans)
                        with open('readed.txt','w',encoding='utf-8') as f:
                            f.write(content[-1])
                        
                        # h = have_speech(ans)
                        # if h:
                            # play_music('tts_logs\\'+h+'.mp3',16000)
                        # else:
                            # tts.readit(ans,name)
                            # play_music(name,16000)
                            # with open('tts_recoder.csv','a',encoding='utf-8') as f:
                                # writer = csv.writer(f)
                                # writer.writerow([name.split('\\')[-1].split('.')[0],ans])
        else:
            #群消息
            print(content)
            print('收到群消息')
            qun = re.findall(r'群.*内',latest)[0]
            qunname = qun.split('(')[0]  # 群名
            qunnum = qun.split('(')[-1].split(')')[0]  # 群号
            saynum = content[1]  # 发言人
            
            if not readed(content[-1]):
                ans = chatme.chat(' '.join(content[-1].split(' ')[:-1]))
                sd_g_msg(qunnum,ans)
                with open('readed.txt','w',encoding='utf-8') as f:
                    f.write(content[-1])
                # print(sayman)
                print('$ 姬娜:', ans, '\n')
    
    rcv = get_msg()[0]
