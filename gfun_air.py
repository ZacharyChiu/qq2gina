# -*- coding = utf-8 -*-
# Author: Zachary
# @Time: 2020/10/4 16:43

import os
import pygame
from mutagen.mp3 import MP3
import time


def play_music(path,f=16000):
    pygame.mixer.init(frequency=f)
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()



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
        elif ask == 'tem':
            return 'emm...'
        elif ask == 'cxk':
            os.system('start C:/quickstart/gg.lnk ' + 'http://cxkv2.xyz/auth/register')
        elif ask == 'bili':
            os.system('start C:/quickstart/gg.lnk ' + 'http://www.bilibili.com')
        else:
            return '听不懂你在说什么...'
    except Exception as e:
        print(e.args)
        

