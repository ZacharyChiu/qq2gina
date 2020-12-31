import random
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bs
class People():
    def __init__(self):
        with open('People.xml','r',encoding='utf-8') as f:
            xml = f.read()
        html = bs(xml,"html.parser")
        people = html.find_all('p')
        self.people = []  # 所有用户
        for p in people:
            self.people.append(eval(p.string))
        self.dic = eval(html.find_all('trans')[0].string)
        
    def find(self,name):
        # 通过名字获取其档案字典
        try:
            r = []
            for i in self.people:
                if (name in i.values()) or (name in i['name']) or (name in i['body']):
                    r.append(i)
            if len(r) == 1:
                r = r[0]
            return r
        except Exception as e:
            print('Error:',e)
            return ''
            
    def info(self,name,k):
        # 获取某人(name)的某项属性(k)
        try:
            return self.find(name)[k]
        except Exception as e:
            print('Error:',e)
            return ''
    
    def id_key(self,id):
        # 通过id号获取某人信息
        re = {}
        for p in self.people:
            comp = p['id']
            if id == comp:
                re = p
        if re == {}:
            print('Not Found!')
        return re
    def produce(self,name):
        # 介绍某个人
        it = self.find(name)
        age = 2021 - int(it['birth'].split('.')[0])
        if it['gender'] == 'male':
            ta = '他'
        elif it['gender'] == 'female':
            ta = '她'
        
        state1 = name + '，' + self.dic[it['gender']] + '，生于' + it['birth'] + '，现' + str(age) + '岁。'
        state2 = ta + '是'
        for r in self.its_relation(name)[0]:
            state2 = state2 + r[1] + '的' + r[2] + ','
        state2 = state2[:-1] + '。'
        return state1 + state2
        
    def its_relation(self,it):
        # it = self.find(name)
        relations = []
        its = [] 
        for p in self.people:
            id_ = p['id']
            name = p['name'][0]
            r = p['relation']
            for k,v in r.items():
                if type(v) == type([]):
                    for m in v:
                        if type(self.dic[k]) == type({}):
                            # print('%s是%s的%s'%(self.id_key(v)['name'][0],name,self.dic[k][self.id_key(m)['gender']]))
                            relations.append([self.id_key(v)['name'],name,self.dic[k][self.id_key(m)['gender']]])
                        else:
                            # print('%s是%s的%s'%(self.id_key(m)['name'][0],name,self.dic[k]))
                            relations.append([self.id_key(m)['name'],name,self.dic[k]])
                else:
                    if type(self.dic[k]) == type({}):
                        # print('%s是%s的%s'%(self.id_key(v)['name'][0],name,self.dic[k][self.id_key(v)['gender']]))
                        relations.append([self.id_key(v)['name'],name,self.dic[k][self.id_key(v)['gender']]])
                    else:
                        # print('%s是%s的%s'%(self.id_key(v)['name'][0],name,self.dic[k]))
                        relations.append([self.id_key(v)['name'],name,self.dic[k]])
                # print('\n')
        
        for i in relations:
            if it in i[0]:
                its.append(i)
        return [its,relations]  # [指定人物的关系集，所有用户关系集]
        
class Decide():
    def __init__(self,name=''):
        self.mood = random.random()
        self.suit = random.uniform(0.5,1)
        self.users = People()
        self.name = name
        try:
            self.obj = self.users.find(name)
        except:
            self.obj = {}
        self.auth = self.users.info(self.name,'auth')
        if self.users.find(name) in People().people:
            self.weight = self.mood * 0.1 + self.auth * 0.6 + self.suit * 0.3
    def show(self):
        # print('Object: %s\nMood: %.2f\nAuth: %.2f\nWeight: %.4f\n'%(self.name,self.mood,self.auth,self.weight))
        ans = ['You stupid dogfucker!','Just leave me alone, please!','...','Alright.','OK.','You are the best~']
        lenth = len(ans)
        choice = int(lenth*self.weight)
        print('Weight: %.2f\nChoice: %s'%(self.weight,ans[choice]))
        
# zac = People('Zac',1)
# william = People('William',0.6)

if __name__ == '__main__':
    users = People()
    print(users.produce('徐源'))
    

# for i in range(30):
    # d = Decide('William')
    # d.show()

# x,y1,y2 = [],[],[]
# for i in range(5000):
    # x.append(i)
    # dcdz = Decide(zac)
    # dcdq = Decide(william)
    # y1.append(dcdz.weight)
    # y2.append(dcdq.weight)
    
# plt.title('XX')  # 折线图标题
# # plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示汉字
# plt.xlabel('time')  # x轴标题
# plt.ylabel('decide')  # y轴标题
# plt.plot(x, y1, marker='o', markersize=3)  # 绘制折线图，添加数据点，设置点的大小
# plt.plot(x, y2, marker='o', markersize=3)

# for a, b in zip(x, y1):
    # plt.text(a, b, '', ha='center', va='bottom', fontsize=10)  # 设置数据标签位置及大小
# for a, b in zip(x, y2):
    # plt.text(a, b, '', ha='center', va='bottom', fontsize=10)
    
# plt.legend(['Zac', 'William'])  # 设置折线名称

# plt.show()