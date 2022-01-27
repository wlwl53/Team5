import base64
from io import BytesIO

import json
import pickle
import time
import random

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers

# Crawling 관련 module
# ----------------------------------------------------------------------------------------------
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote  # 한글 처리 함수
from urllib.error import HTTPError
from requests import get  # GET 방식 호출

from datetime import datetime

# Wordcloud 관련
# ----------------------------------------------------------------------------------------------
import os
import pandas as pd
import pymysql
import re
import platform
from PIL import Image
import numpy as np

from konlpy.tag import Twitter
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import rc

rc('font', family='Malgun Gothic')
plt.rcParams["font.size"] = 12  # 글자 크기
plt.rcParams['axes.unicode_minus'] = False  # minus 부호는 unicode 적용시 한글이 깨짐으로 설정

# Create your tests here.
print("데이터 분석 시작")
conn = pymysql.connect(host='localhost', user='pyuser', password='1234',
                           db='team5', charset='utf8')

cursor = conn.cursor()
sql_pre = '''
    SELECT COUNT(newsno) AS cnt
    FROM news_news
    '''
cursor.execute(sql_pre)
row = cursor.fetchone()

if row[0] != 0:
    sql = '''
         SELECT newsno, article, link, ymd, rdate
         FROM news_news
         ORDER BY newsno ASC
       '''
    df = pd.read_sql(sql, conn)

    cursor.close()
    conn.close()

    # 기사 제목
    articles = df['article']

    # 기사 제목에서 번호를 삭제
    # print("-> 기사 제목에서 번호를 삭제")
    for i in range(0, len(articles)):
        article = articles[i]
        dot_index = article.find('.')
        article = article[dot_index + 2:]
        articles[i] = article

    # 모든 기사에서 불필요한 문자 제거
    # print("-> 모든 기사에서 불필요한 문자 제거")
    for i in range(0, len(articles)):
        article = articles[i]
        article = re.sub('[.]+', ' ', article)
        article = re.sub('[0-9]+', '', article)
        article = re.sub('[A-Za-z]+', '', article)
        article = re.sub('[-=+,#/\?:^$@*\“\”\"※~&%ㆍ·!』\\‘’|\(\)\[\]\<\>`\'…》↑→]', '', article)
        articles[i] = article
        # print('#', end="")

    # print("-> 모든 데이터 하나의 문자열로 통합")
    article_all = ''
    for i in range(len(articles)):
        article_all = article_all + ' ' + articles[i]

    # print("-> 명사 추출")
    okt = Okt()  # 형태소 분석 지원 클래스
    article_all_nouns = okt.nouns(article_all)

    # 한문자는 모두 삭제함.
    # print("-> 2문자 이상만 대상으로 선정")
    article_all_nouns2 = []
    for item in article_all_nouns:
        if len(item) >= 2:
            article_all_nouns2.append(item)

    # 불용어
    STOPWORDS = ['내년', '시장', '완화', '사전', '사업', '올해',
                 '만원', '검토', '기준', '역대', '심리', '개월', '최저',
                 '최대', '이상', '폭탄', '가구', '논란', '대충', '지난해',
                 '오늘', '부로', '산시', ]

    # print("-> 불용어 제거")
    filtered = []  # 불용어 제거
    for tag in article_all_nouns2:
        if tag not in STOPWORDS:
            filtered.append(tag)

    # print("-> 같은 맥락의 단어 통합")
    # 중복 의미를 갖는 데이터 정제하기, 마지막[-1] index에 대표 문자열 지정
    WORDS = [
        ['마련', '내집마련'],
        ['서울시', '서울'],
    ]

    # for문을 이용한 모든 데이터의 처리
    filtered_words = filtered.copy()
    for i in range(len(filtered_words)):
        word = filtered_words[i]  # 하나의 태그 추출
        for j in range(len(WORDS)):
            if word in WORDS[j] and tag != '':  # 맥락이 같은 단어 검사
                word = WORDS[j][-1]  # 대표 단어를 산출
                filtered_words[i] = word  # 대표 단어로 변경

    # 빈도 분석
    # print("-> 빈도수가 높은 100위까지 출력")
    tags_counter = Counter(filtered_words)
    most_common = tags_counter.most_common(100)  # 빈도수가 높은 100위까지 출력
    # print(most_common)

    # print("-> 워드클라우드용 데이터인 DataFrame 생성")
    df = pd.DataFrame(most_common)
    df.columns = ['tags', 'counts']

    # print("-> 워드클라우드 이미지 제작중...")

    # if platform.system() == 'Windows':  # 윈도우의 경우
    #     font_path = "C:/Windows/Fonts/malgun.ttf"
    # elif platform.system() == "Darwin":  # Mac 의 경우
    #     font_path = "/Users/$USER/Library/Fonts/AppleGothic.ttf"

    # maskimg = np.array(Image.open('/static/images/wc_home.jpg'))

    img = np.array(Image.open('./news/static/images/home_3.jpg'))
    mask = np.array(img)
    # image_colors = ImageColorGenerator(img)

    wordcloud = WordCloud(font_path='./news/static/font/BMEULJIROTTF.ttf',
                          background_color="white",
                          max_words=100,
                          relative_scaling=0.3,
                          width=800,
                          height=800,
                          mask=mask,
                          colormap="cividis",
                          random_state=42,

                          ).generate_from_frequencies(tags_counter)
    plt.figure(figsize=(10, 10))
    # plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    # plt.show()
    # plt.savefig('./news-wordcloud1.png')

    # 현재 프로젝트 static 폴더 기준으로 선언해야 인식됨.
    fname_django = './news/static/images/news-wordcloud.png'
    fname_spring = 'C:/kd1/ws_java/team5_v2sbm3c/src/main/resources/static/trend/images/news-wordcloud.png'
    if os.path.exists(fname_django):
        # print("기존에 생성된 news-wordcloud.png 파일을 삭제했습니다.")
        os.remove(fname_django)

    if os.path.exists(fname_spring):
        # print("기존에 생성된 news-wordcloud.png 파일을 삭제했습니다.")
        os.remove(fname_spring)

    # print('Wordcloud 이미지 파일로 저장')
    plt.savefig(fname_django)  # django Wordcloud 이미지 파일로 저장
    #plt.savefig(fname_spring)  # spring Wordcloud 이미지 파일로 저장