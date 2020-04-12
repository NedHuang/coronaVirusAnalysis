import requests
import json
import time
import csv

#解析中国疫情每日数据
def getdata_chinadaily(resp):
    d={} #空白字典用于存放数据,数据量不大，所以没有使用数据库
    #中国每日数据写入字典
    for i in resp['chinaDayList']:
        # print(i) #打印观察数据
        d[i['date']]={} #需要先定义空白的子字典
        d[i['date']]['acc_confirm'] = i['confirm']
        d[i['date']]['acc_dead']=i['dead']
        d[i['date']]['acc_heal'] = i['heal']
        d[i['date']]['now_confirm']=i['nowConfirm']
        d[i['date']]['dead_rate']=i['deadRate']

    # 中国每日新增人数写入字典
    for i in resp['dailyNewAddHistory']:
           d[i['date']]['dailyadd_confirm']=i['country']
    #写入csv文件
    with open('d:/cov_china_report2020.csv','w',newline='') as f:
        writer=csv.writer(f)
        column=['date','acc_confirm','acc_dead','acc_heal','now_confirm','dead_rate','dailyadd_confirm']
        writer.writerow(column)
        for i in d:
            try:
                row=['2020-' + i.replace('.','-'),d[i]['acc_confirm'], d[i]['acc_dead'],d[i]['acc_heal'],d[i]['now_confirm'],d[i]['dead_rate'],d[i]['dailyadd_confirm']]
                writer.writerow(row)
            except KeyError:
                row = ['2020-' + i.replace('.','-'), d[i]['acc_confirm'], d[i]['acc_dead'], d[i]['acc_heal'], d[i]['now_confirm'],d[i]['dead_rate'], 'NA']
                writer.writerow(row)

#解析全球感染人数
def getdata_worlddistribution(resp):
    with open('d:/coronavirus2020worlddistribution.csv','w',newline='') as f:
        writer=csv.writer(f)
        column=['country','confirm','suspect','dead','deadrate']
        writer.writerow(column)
        for i in resp['foreignList']:
            # print(i['name'],i['total']['confirm'],i['total']['suspect'], i['total']['dead'],i['total']['deadRate'])
            row=[i['name'],i['confirm'],i['suspect'], i['dead'],round(i['dead']/i['confirm'],2)]
            writer.writerow(row)

#解析中国各省感染人数
def getdata_chinadistrubution(resp):
    with open('C:/Users/Mingzhe/Desktop/686Project/sipderData.csv','w',newline='') as f:
        writer=csv.writer(f)
        column=['province','confirm','suspect','dead','deadrate']
        writer.writerow(column)
        for i in resp['areaTree'][0]['children']:
            # print(i['name'],i['total']['confirm'],i['total']['suspect'], i['total']['dead'],i['total']['deadRate'])
            row=[i['name'],i['total']['confirm'],i['total']['suspect'], i['total']['dead'],i['total']['deadRate']]
            writer.writerow(row)

if __name__=='__main__':
    url1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d' % int(time.time()) #全国各省疫情数据地址
    url2 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other&callback=&_=%d' % int(time.time())#中国每日数据及全球数据地址
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Referer': 'https://news.qq.com/zt2020/page/feiyan.htm'}
    resp1 = requests.get(url1, headers=headers)
    resp2 = requests.get(url2, headers=headers)
    resp1= json.loads(resp1.json()['data'])
    resp2 = json.loads(resp2.json()['data'])
    getdata_chinadistrubution(resp1)
    getdata_chinadaily(resp2)
    getdata_worlddistribution(resp2)
