# -*- coding = utf-8 -*-
# Author: Zachary
'''
通过QQ向姬娜发送命令
'''
import os 
import re 
import time
# import csv
# import pygame

# 自建库
import spider
import gfun_air



def show_head():
	# themsg来自全局变量
	typedic = {'好友':'私聊','群':'群聊'}
	msgtime = themsg.time
	msgtype = typedic[themsg.msgtype]
	date0 = msgtime.split(' ')[0].split('-')
	date = date0[0][2:] + date0[1] + date0[2]
	thetime = msgtime.split(' ')[1]
	title_time = date + ' ' + thetime
	title = '='*10 + msgtype + '(' + title_time + ')' + '='*10
	
	sdid = themsg.sdid
	if themsg.sdid == '1563382991':
		sdname = '超哥'
	else:
		sdname = themsg.sdname
	if msgtype == '私聊':
		vice_title = '$ ' + sdname + '(' + sdid + ')：[' + themsg.texttype + ']'
		return title + '\n' + vice_title
	elif msgtype == '群聊':
		vice_title = themsg.sdqunname + '(' + themsg.sdqunid + ')\n$ ' + sdname + '(' + sdid + ')：[' + themsg.texttype + ']'
		return title + '\n' + vice_title

# ===================================Main======================================
did = 0
qq = gfun_air.QQ()
pics = gfun_air.Dir('D:\\#My\\GiData\\Source\\Arts\\Images\\Pics')
	
while 1:
	try:
		Msgs = gfun_air.MsgID()  # 信息类
		status = gfun_air.Readed()
		nolog1 = Msgs.nologs
		if nolog1:
			if not did:
				print('未找到今天的日志。')
				os.system('start go-cqhttp.exe')
				did = 1
		else:  # 有日志
			Logs = Msgs.logs
			latest = Msgs.rcv[-1]  # 最新消息
			ed_msg = status.dic['readed']  # 最后的已读消息
			if status.dic['status'] == 'sleep':  # 【离线状态，等待激活】
				weborder = spider.web_order()
				if weborder == 'Order:ONZacdell':  # 要求姬娜上线(办公室端)
						os.system('start go-cqhttp.exe')
						status.write(status='normal')
						time.sleep(25)  # 等待加载
						qq.sd_p_msg(1563382991,'[CQ:record,file=gina_welcome.amr]')

			elif status.dic['status'] == 'normal':  # 【普通聊天状态】
				if not status.readed(latest):  # 有未读消息
					themsg = gfun_air.MsgID(Msgs.get_id(latest))  # 最新消息独立信息类
					if themsg.msgtype == '好友':  # 私信
						if themsg.sdid == '1563382991':
							if themsg.texttype == '命令':
								order = themsg.order
								r = gfun_air.do(order)
								if r.split(' ')[0] == 'taskkill':  #准备杀了cqhttp
									print(show_head())
									print('#'+themsg.text+'#')
									qq.sd_p_msg(1563382991,'可爱的姬娜会离你而去')
									round = 1
									while round:
										if Msgs.update()[-1] != latest:  # 有新消息
											Logs = Msgs.logs
											latest = Logs[-1]
											msgid = Msgs.get_id(latest)
											themsg = gfun_air.MsgID(msgid)
											if themsg.msgtype == '好友':
												if themsg.sdid == '1563382991':
													if themsg.text in ['好的','yes']:
														qq.sd_p_msg(1563382991,'道不同不相为谋，我日你妈先告辞了[CQ:face,id=118]')
														status.update()
														status.write(text=themsg.text,status='sleep')
														os.system(r)
														round = 0
														print('-'*40)
														print('$ 姬娜:', '啊我死了', '\n')
														print('\n'*2)
													elif themsg.text in ['不了','no','取消','cancel','算了']:
														qq.sd_p_msg(1563382991,'那我就不下线啦~')
														status.update()
														status.write(text=themsg.text)
														round = 0
														print('-'*40)
														print('$ 姬娜:', '......', '\n')
														print('\n'*2)
								elif r.split(' ')[0] == 'tags':
									qq.sd_p_msg(1563382991,'当前资源文件夹为【Pics】')
									if r.split(' ')[1] in ['+','-','/']:
										m = r.split(' ')[1]
										tags = r.split(' ')[2]
										if m == '+':
											f_list = pics.andtag(tags)
										elif m == '-':
											f_list = pics.notag(tags)
										elif m == '/':
											f_list = pics.ortag(tags)
										print(f_list[0])
										qq.sd_p_msg(1563382991,'开始生成预览图...')
										img = gfun_air.Pic()
										sh = img.preview(f_list)
										qq.sd_p_msg(1563382991,'[CQ:image, file=file:///D:/%23My/GiData/Creation/Projects/Python/Q2G/preview.jpg]' )
										
									status.update()
									status.write(text=latest)
								elif r.split(' ')[0] == 'picid':
									id_ = r.split(' ')[1]
									file = pics.andtag(id_)[0]
									print(file)
									qq.sd_p_msg(1563382991,'[CQ:image, file=file:///D:/%23My/GiData/Source/Arts/Images/Pics/'+file+']')
									status.update()
									status.write(text=latest)
								
								elif r.split(' ')[0] == 'halt':
									# qq.sd_p_msg(1563382991,'[CQ:record, file=file:///D:/%23My/GiData/Creation/Designs/Audios/imhere.amr]')
									print(show_head())
									print('#'+themsg.text+'#')
									qq.sd_p_msg(1563382991,'是否要关机？')
									round = 1
									while round:
										if Msgs.update()[-1] != latest:  # 有新消息
											Logs = Msgs.logs
											latest = Logs[-1]
											msgid = Msgs.get_id(latest)
											themsg = gfun_air.MsgID(msgid)
											if themsg.msgtype == '好友':
												if themsg.sdid == '1563382991':
													if themsg.text in ['好的','yes']:
														qq.sd_p_msg(1563382991,'好，那我关机了。')
														status.update()
														status.write(text=themsg.text,status='sleep')
														os.system('shutdown -s')
														round = 0
														print('-'*40)
														print('$ 姬娜:', '要关机了噢', '\n')
														print('\n'*2)
													elif themsg.text in ['不了','no','取消','cancel','算了']:
														qq.sd_p_msg(1563382991,'那我就不关机啦~')
														status.update()
														status.write(text=themsg.text)
														round = 0
														print('-'*40)
														print('$ 姬娜:', '......', '\n')
														print('\n'*2)
								
								
								else:
									status.update()
									status.write(text=themsg.text)

							elif themsg.cq == 1:  # Zac的私聊CQ码
								status.update()
								status.write(text=latest)
								print('\n'*2)
							elif themsg.texttype == '普通对话':
								ans = gfun_air.gfun(themsg.text.strip())
								# print('###现在获取到回答：%s'%ans)
								print('-'*40)
								print('$ 姬娜:', ans, '\n')
								qq.sd_p_msg(1563382991,ans)
								status.update()  # 主要是状态可能变了，所以要更新
								status.write(text=latest)
								print('\n'*2)

					elif themsg.msgtype == '群':
						qunname = themsg.sdqunname
						qunnum = themsg.sdqunid
						saynum = themsg.sdid  # 发言人
						text = themsg.text
						print(show_head())
						print('#'+themsg.text+'#')
						if themsg.cq == 1:
							cqtype = themsg.cqtype
							cqfile = themsg.cqfile.split('=')[-1]
							# print('text: #%s#'%text)
							if themsg.cqtype == 'at':  # @某人
								if themsg.texttype == '@姬娜':  # @Gina
									response = gfun_air.gfun(text.strip())
									if themsg.text != '':
										ans = '[CQ:at,qq='+saynum+'] ' + response
										qq.sd_g_msg(qunnum,ans)
										print('-'*40)
										print('$ 姬娜:', ans, '\n')
										status.update()
										status.write(text=latest)
										print('\n'*2)
									else:
										ans = '[CQ:at,qq='+saynum+'] ' + '干嘛？'
										qq.sd_g_msg(qunnum,ans)
										status.update()
										status.write(text=latest)
										round = 0
										while round <5:  # 等待5轮对话，如果此人不发言，就不鸟他
											if Msgs.update()[-1] != latest:  # 有新消息
												Logs = Msgs.logs
												latest = Logs[-1]
												msgid = Msgs.get_id(latest)
												themsg = gfun_air.MsgID(msgid)
												if themsg.msgtype == '群':
													if themsg.sdid == saynum:
														if themsg.text != '':
															response = gfun_air.gfun(text.strip())
															ans = '[CQ:at,qq='+saynum+'] ' + response
															qq.sd_g_msg(qunnum,ans)
															status.update()
															status.write(text=latest)
															print('\n'*2)
															round = 6
													else:
														if themsg.cq == 1:
															cqtype = themsg.cqtype
															cqfile = themsg.cqfile.split('=')[-1]
															if themsg.cqtype == 'at':  # @某人
																if themsg.texttype == '@姬娜':  # @Gina
																	if themsg.text != '':
																		response = gfun_air.gfun(text.strip())
																		ans = '[CQ:at,qq='+themsg.sdid+'] ' + response
																		qq.sd_g_msg(qunnum,ans)
																		status.update()
																		status.write(text=latest)
																		print('\n'*2)
														else:
															status.update()
															status.write(text=latest)
														round += 1
											# print('Round %d'%round)
										status.update()
										status.write(text=latest)


							else:
								status.update()
								status.write(text=latest)
						else:
							if saynum == '1563382991':
								if text[-2:] == '  ':
									ans = gfun_air.gfun(text.strip())
									qq.sd_g_msg(qunnum,ans)
									status.update()
									status.write(text=latest)
									print('-'*40)
									print('$ 姬娜:', ans, '\n')
									print('\n'*2)
								elif themsg.texttype == '命令':
									order = text[4:].strip()
									# print('#%s#'%order)
									if order == 'test':
										ans = '[CQ:record,file=test.amr]'
										qq.sd_g_msg(qunnum,ans)
										
								else:
									status.update()
									status.write(text=latest)

							else:
								status.update()
								status.write(text=latest)

		try:
			if 'go-cqhttp.exe' not in gfun_air.whatrun():
				if status.dic['status'] != 'sleep':
					status.write(status='sleep')
					print('已更新状态为sleep')
			else:
				if status.dic['status'] != 'normal':
					status.write(status='normal')
					print('已更新状态为normal')
		except Exception as e:
			# print(e)
			pass
	
		

	except Exception as e:
		print(e)
		qq.sd_p_msg(1563382991,'后台崩溃了一下下【'+str(e)+'】')
