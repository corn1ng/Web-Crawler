# -*- coding:utf8 -*-
# author: Brett
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://movie.douban.com/top250'


def downloadurl(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = requests.get(url, headers=headers).content
    return data


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print (soup.prettify())
    movie_lists = soup.find('ol', attrs={'class': 'grid_view'})
    for movie in movie_lists.find_all('li'):
        # print (movie)
        detail = movie.find_all('span', attrs={'class': 'title'})
        try:
            print(detail[0].string + "    " + str(detail[1].string).split('/')[1])
        except IndexError:
            print(detail[0].string)

    next_page = soup.find('span',attrs={'class':'next'}).find('a')
    #  print (next_page)
    if next_page:
        return DOWNLOAD_URL + next_page['href']


def main():
    data = downloadurl(DOWNLOAD_URL)
    url = parse_html(data)
    for i in range(9):
        data = downloadurl(url)
        url = parse_html(data)

if __name__ == '__main__':
    main()