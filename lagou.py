# -*- coding:utf8 -*-
# author: Brett
from bs4 import BeautifulSoup
import requests
import json
import time


def downloadurl(url, headers, cookie):
    data1 = requests.get(url, headers=headers, cookies=cookie).content
    return data1


def chooselanguage(index):
    lan = ['Python', 'Java', 'php']
    return lan[index]


def choosearea(index):
    area = ['广州', '上海', '北京', '深圳']
    return area[index]


def equip_url(index):
    # + '/?labelWords=label' + 'filterOption=' + str(index)
    return 'https://www.lagou.com/zhaopin/' + language + '/' + str(index)



def parse_html(html):
   # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    list1 = soup.find('div', attrs={'class': 's_position_list'}).ul
    # print (list1)
    mylist = list1.find_all('li')
    for pos in mylist:
        print(pos['data-company']+'   '+'   '+pos['data-positionname']+'   '+pos['data-salary']+'   '+pos.div.div.div.a['href'])


def return_header_cookie():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
                      'Chromium/62.0.3202.94 Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_Java?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords'
                   '=&suginput=',
        'X - Requested - With': 'XMLHttpRequest'
    }
    cookies = {
        'Cookie': 'JSESSIONID=ABAAABAAAGFABEF26405D70A5AAC9486FF333701F84DD92; _gat=1; '
                  'user_trace_token=20171206211924-13facdc9-da88-11e7-9c3f-5254005c3644; PRE_UTM=; PRE_HOST=; '
                  'PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; '
                  'LGUID=20171206211924-13fad121-da88-11e7-9c3f-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; '
                  'TG-TRACK-CODE=index_navigation; _gid=GA1.2.1404887006.1512566364; _ga=GA1.2.228933349.1512566364; '
                  'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512477132,1512539647,1512566364; '
                  'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1512566387; '
                  'LGSID=20171206211924-13facfa4-da88-11e7-9c3f-5254005c3644; '
                  'LGRID=20171206211950-23d289d4-da88-11e7-9c3f-5254005c3644; '
                  'SEARCH_ID=6994520a8e4548649f7ab6cc74df19e1 '
    }
    return headers, cookies


def parsejson(URL, language, page, headers, cookie):
    data = {'first': 'false', 'pn': page, 'kd': language}
    jsons = requests.post(URL, data, headers=headers, cookies=cookie)
    answer = jsons.json()

    for i in range(15):
        print(answer['content']['positionResult']['result'][i]['companyFullName']+'  '
              + answer['content']['positionResult']['result'][i]['city']+'   '
              + answer['content']['positionResult']['result'][i]['positionName']+'   '
              + answer['content']['positionResult']['result'][i]['salary']+'   '
              + str(answer['content']['positionResult']['result'][i]['positionId']))


if __name__ == '__main__':
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    language = chooselanguage(1)
    city = choosearea(2)
    CITYNURL = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city='+city+'&needAddtionalResult=false' \
                '&isSchoolJob=0 '
    headers, cookie = return_header_cookie()

    # ***********************************************************
    # 通过城市查找 ：拉钩使用ajax方式，网页中不显示信息，
    for i in range(20):
        try:
            parsejson(CITYNURL, language, i, headers, cookie)
            time.sleep(10)
        except KeyError:
            time.sleep(30)

    # ***********************************************************
    # 全国职位：网页中显示信息，使用beautifulsoup解析网页。
    for i in range(1, 40):
        try:
            posurl = equip_url(i)
            data = downloadurl(posurl, headers, cookie)
            parse_html(data)
            time.sleep(10)
        except AttributeError:
            time.sleep(30)
    # ***********************************************************