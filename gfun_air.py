# -*- coding = utf-8 -*-
# Author: Zachary
# @Time: 2020/10/4 16:43

import os
import pygame
# from mutagen.mp3 import MP3
import time
import requests


def play_music(path,f=16000):
    pygame.mixer.init(frequency=f)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

def clean(l):
    img = 'jpg.png.gif.jpeg.webp.jfif'.split('.')
    new = []
    for i in l:
        if '.' in i:
            type = i.split('.')[-1].lower()
        else:
            type = ''
        if type in img:
            new.append(i)
    return new

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

def do(ask):
    try:
        if ask[:5] == 'sound':
            mu = os.listdir('D:\\#My\\GiData\\Creation\\Designs\\Audios')
            musics = []
            music_type = ['mp3','wmv']
            for m in mu:
                if m.split('.')[-1].lower() in music_type:
                    musics.append(m)
            # for i in range(len(musics)):
                # print('%d【%s】' %(i,musics[i]))
            num = ask.split('sound ')[-1]
            if '.' not in num:
                if int(num):
                    m_name = musics[int(num)]
                    play_music('D:\\#My\\GiData\\Creation\\Designs\\Audios\\'+m_name)
            else:
                ns = num.split('.')
                for n in ns:
                    if int(n):
                        m_name = musics[int(n)]
                        path = 'D:\\#My\\GiData\\Creation\\Designs\\Audios\\' + m_name
                        play_music(path)
                        audio = MP3(path)
                        length = float(audio.info.length)
                        time.sleep(length)
        elif ask[:3] == 'tag':
            path = '/media/pi/3312-1D19/Gidata/Source/Arts/Images/pic'
            datapath = '~/python/qq2gina/data/images'
            l = clean(os.listdir(path))
            order = ask[4:].split(' ')
            if len(order) ==1:
                try:
                    i = int(order[0])
                    asknum = ask[4:]
                    for f in l:
                        if '.'+asknum+'.' in f:
                            result = f
                    # print(l)
                    os.system('cp ' + path + '/' + result + ' ' + datapath)
                    return '[CQ:image,file=' + result+']'
                except:
                    if order[0] == 'len':
                        return str(len(l))
                    else:
                        # and mode (with just 1 tag)
                        collection = []
                        for f in l:
                            if order[0]+'.' in f:
                                collection.append(f.split('.')[-2])
                        if collection:
                            if len(collection) < 8:
                                return '\n'.join(collection)
                            else:
                                re = ''
                                for i in range(0,len(collection),5):
                                    re = re + ' '.join(collection[i:i+5]) + '\n'
                                return re
                                    
                        else:
                            return 'Nothing here, honey.'
                        pass
            else:
                if order[0] == '+':
                    filelist = l[:]
                    tags = order[1].split('.')
                    clist = []
                    for tag in tags:
                        for filename in filelist:
                            filetag = filename.split('.')
                            if tag in filetag:
                                clist.append(filename)
                        filelist = clist[:]
                        clist = []
                    collection = []
                    for i in filelist:
                        collection.append(i.split('.')[-2])
                    if collection:
                        if len(collection) < 8:
                            return '\n'.join(collection)
                        else:
                            re = ''
                            for i in range(0,len(collection),5):
                                re = re + ' '.join(collection[i:i+5]) + '\n'
                            return re
                    
        elif ask[:2] == 'os':
            return os.popen(ask[3:]).read()
        elif ask == 'bili':
            os.system('start C:/quickstart/gg.lnk ' + 'http://www.bilibili.com')
        else:
            return '听不懂你在说什么...'
    except Exception as e:
        print(e.args)
        

