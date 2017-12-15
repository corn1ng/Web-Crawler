# -*- coding:utf8 -*-
# author: Brett
from bs4 import BeautifulSoup
import requests
import json
import time
import redis


def redis_conn():
    pool = redis.ConnectionPool(host='localhost', port=6379,
                                decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r


def return_header():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache - Control': 'max - age = 0',
        'Connection': 'keep - alive',
        'Upgrade - Insecure - Requests': '1',
        'Host': 'openreview.net',
        'Origin': 'https://openreview.net',
        'Referer': 'http://www.iclr.cc/doku.php?id=ICLR2018:main&redirect=1',
    }
    return headers


def return_contentheader():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep - alive',
        'Host': 'openreview.net',
    }
    return headers


def downloadurl(url, headers):
    data1 = requests.get(url, headers=headers).content
    return data1


def geturl():
    urllist = []
    for i in range(0, 1050, 50):
        URL = 'https://openreview.net/notes?invitation=ICLR.cc%2F2018%2FConference%2F-%2FBlind_Submission&offset=' + str(
            i) + '&limit=50'
        urllist.append(URL)
    return urllist


def parsejson(URL, headers, conn):
    jsons = requests.get(URL, headers=headers)
    answer = jsons.json()
    for i in answer['notes']:
        # print(i['content']['title']+'   '+i['id'])
        val ={'replyCount': i['replyCount'],
              'id': i['id'],
              'keywords': i['content']['keywords'],
              }
        conn.hset(name='iclr', key=i['content']['title'], value=val)


def specify_content(conn):
     all_paper = conn.hgetall('iclr')
     urllist = []
     for i in all_paper:
         m = {}
         m = conn.hget('iclr', i)
         id = (eval(m)['id'])
         urllist.append('https://openreview.net/notes?forum='+str(id)+'&trash=true')
     return urllist


def parse_content(URL, headers):
    jsons = requests.get(URL,headers)
    answer = jsons.json()
    score = 0
    index = 0
    for i in answer['notes']:
        try:
            score = score + int(str(i['content']['rating']).split(':')[0])
            index = index+1
        except KeyError:
            pass
    try:
        avgscore = score/index
    except ZeroDivisionError:
        avgscore = 0
    avg_score = ('%.2f' % avgscore)
    title = (answer['notes'][0]['forumContent']['title'])
    return title, avg_score


def save_to_redis(title, score, conn):
    conn.hset(name='iclrscore', key=title, value=score)


if __name__=='__main__':
    head = return_header()
    UR = 'https://openreview.net/notes?invitation=ICLR.cc%2F2018%2FConference%2F-%2FBlind_Submission&offset=0&limit=50'
    conn = redis_conn()
    urllist = geturl()
    for i in urllist:
        parsejson(i, headers=head, conn=conn)
    xinlist = specify_content(conn)
    # print((xinlist))

    CONTENT_URL = 'https://openreview.net/notes?forum=SyBPtQfAZ&trash=true'
    contentheader = return_contentheader()
    # parse_content(CONTENT_URL, contentheader)

    for i in xinlist:
         title, socre = parse_content(i,contentheader)
         save_to_redis(title, socre, conn)
