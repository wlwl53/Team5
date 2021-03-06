import time
import random

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote  # 한글 처리 함수
from urllib.error import HTTPError

from django.urls import reverse
from pyreadline.clipboard.win32_clipboard import enum
from requests import get        # GET 방식 호출
from datetime import datetime
from dateutil.relativedelta import relativedelta

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from news.models import News

def getdate():
    ymd_str_list = []
    today = datetime.now().strftime("%Y%m%d")
    ymd = datetime.now() - relativedelta(months=3) # 3달전
    while True:
        ymd_str = ymd.strftime("%Y%m%d")
        ymd_str_list.append(ymd_str)
        ymd += relativedelta(days=1)
        if ymd_str == today:
            break
    return ymd_str_list

def getbs(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        web = get(url, headers=headers).content
        bs = BeautifulSoup(str(web, 'utf-8'), 'html.parser') # parser: 태그 해석기, html 가능
        time.sleep(random.uniform(2, 6))  # 3~8초 사이 랜덤한 시간으로 sleep

        # 아래도 동일
        # bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8') # parser: 태그 해석기, html 가능
    except HTTPError as e:
        print(e)
        return None
    else:
        return bs

def parse_news():
    url = "https://land.naver.com"
    url_mainnews = "https://land.naver.com/news/headline.naver"
    ymd_list = getdate()
    result=[]

    for i in ymd_list:
        ymd = i
        cnt = 0
        print(ymd)
        bs = getbs(url_mainnews + '?bss_ymd=' + ymd)
        # bs = getbs("https://land.naver.com/news/headline.naver")
        # print(bs)
        tags = bs.select('dl.news_list > dt')
        #print(len(tags))

        for i, tag in enumerate(tags):
            link = tag.select('a')[0]['href']
            url_link = url + link
            title = getbs(url_link).select_one('div.article_header > h3').text
            # print(url_link)
            # print(title)

            cnt += 1
            article = '{0:2d}. {1}'.format(cnt, title)
            data = {
                'article': article,
                'link': url_link,
                'ymd': ymd
            }
            result.append(data)
            News(article=data['article'], link=data['link'], ymd=data['ymd']).save()

        tags2 = bs.select('ul.headline_list > li > dl')
        # print(len(tags2))

        for i, tag in enumerate(tags2):
            a_len = len(tag.select('a'))

            if a_len == 2:
                title = tag.select('a')[1].text
                link = tag.select('a')[1]['href']
                url_link = url + link

            else:
                title = tag.select('a')[0].text
                link = tag.select('a')[0]['href']
                url_link = url + link

            #print(title)
            #print(url_link)

            cnt += 1
            article = '{0:2d}. {1}'.format(cnt, title)
            data = {
                'article': article,
                'link': url_link,
                'ymd': ymd
            }
            result.append(data)
            News(article=data['article'], link=data['link'], ymd=data['ymd']).save()

    return result

if __name__=='__main__':
    news_data_dict = parse_news()
    #print(news_data_dict)
    #for item in news_data_dict:
        #print(item)
        #News(article=item['article'], link=item['link'], ymd=item['ymd']).save()