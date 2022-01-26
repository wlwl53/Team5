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

from news.models import News
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


# ----------------------------------------------------------------------------------------------

def home(request):
    # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    # /news/templates/home.html
    return render(request, 'index.html', {})


# def index(request):
#     return HttpResponse("news first page")

# 시작 페이지 Template 적용
# def index(request):
#     return render(request, 'chart_index.html') # news/templates/chart_index.html

def test(request):

    return render(request, 'test.html')  # news/templates/test.html

    #return render(request, 'ais_index.html') # news/templates/ais_index.html

# news table list
def index(request):
    # print("->index")
    result_set = News.objects.all().order_by('-ymd', 'rdate')  # 모든 레코드를 가져오는 명령어, SELECT ~
    result_set = {'result_set': result_set}  # key, value
    # print(result_set.items())
    return render(request, 'index.html', result_set)  # /news/templates/index.html

def get_item(request):
    data = News.objects.all().order_by('-ymd', 'rdate')
    report_list = serializers.serialize('json', data)
    # print(len(report_list))
    return HttpResponse(json.dumps(report_list), content_type="application/json")


# JSON 형식 출력만 확인
# def crawling(request):
#     print('-> crawling')
#     time.sleep(3)  # 3초 실행 중지
#
#     data = {
#         "cnt": 1,
#     }
#     return HttpResponse(json.dumps(data), content_type="application/json")

# ----------------------------------------------------------------------------------------------
# 데이터 수집
# ----------------------------------------------------------------------------------------------
# ncaptcha를 우회
def getbs(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
        web = get(url, headers=headers).content
        bs = BeautifulSoup(str(web, 'utf-8'), 'html.parser')  # parser: 태그 해석기, html 가능
        time.sleep(random.uniform(2, 5))  # 2~5초 사이 랜덤한 시간으로 sleep

        # 아래도 동일
        # bs = BeautifulSoup(html, 'html.parser', from_encoding='utf-8') # parser: 태그 해석기, html 가능
    except HTTPError as e:
        print(e)
        return None
    else:
        return bs


# 크롤링 결과를 화면에만 출력, 처리건수를 json 출력
def crawling(request):
    print('Crawling 실행중...')
    url = "https://land.naver.com"
    url_mainnews = "https://land.naver.com/news/headline.naver"
    # today = datetime.now().strftime("%Y%m%d")
    # print(request.POST)
    # ymd_list = request.POST.getlist('arr[]')
    ymd = (request.POST.get('arr'))

    cnt = 0
    # print(ymd_list)

    # for ymd in ymd_list:
    # print(ymd)
    bs = getbs(url_mainnews + '?bss_ymd=' + ymd)
    tags = bs.select('dl.news_list > dt')
    # print(len(tags))

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

        # print(title)
        # print(url_link)

        cnt += 1
        article = '{0:2d}. {1}'.format(cnt, title)
        data = {
            'article': article,
            'link': url_link,
            'ymd': ymd
        }
        News(article=data['article'], link=data['link'], ymd=data['ymd']).save()

    # print('-> crawling')
    time.sleep(1)  # 2초 실행 중지
    # 처리 건수 출력
    print(str(ymd) + ' -> crawling ' + str(cnt))
    data = {
        "ymd": ymd,
        "cnt": cnt,
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def delete(request):
    # print(request)
    # print(request.POST['newsno'])
    newsno = request.POST['newsno']
    print('삭제할 번호 newsno: ' + newsno)
    # Django삭제시 SELECT쿼리 실행후 DELETE쿼리 실행해야 함
    news = News.objects.get(newsno=newsno)  # id 컬럼에 값을 할당하여 삭제할 레코드를 가져옴
    news.delete()  # DBMS에서 삭제 실행, DELETE FROM ~
    return HttpResponseRedirect(reverse('news:index'))  # 목록으로 이동 http://127.0.0.1:8000/news/


def delete_all(request):
    time.sleep(3)  # 3초 실행 중지
    News.objects.all().delete()

    data = {
        "msg": "모든 데이터를 삭제했습니다.",
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def trend_analysis(request):
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
        fname_django = 'C:/kd1/ws_python/Team5/news/static/images/news-wordcloud.png'
        fname_spring = 'C:/kd1/ws_java/team5_v2sbm3c/src/main/resources/static/trend/images/news-wordcloud.png'
        if os.path.exists(fname_django):
            # print("기존에 생성된 news-wordcloud.png 파일을 삭제했습니다.")
            os.remove(fname_django)

        if os.path.exists(fname_spring):
            # print("기존에 생성된 news-wordcloud.png 파일을 삭제했습니다.")
            os.remove(fname_spring)

        # print('Wordcloud 이미지 파일로 저장')
        plt.savefig(fname_django)  # django Wordcloud 이미지 파일로 저장
        plt.savefig(fname_spring)  # spring Wordcloud 이미지 파일로 저장

        data = {
            "code": 1,
            "msg": "데이터분석을 완료했습니다.",
        }
    else:
        data = {
            "code": 0,
            "msg": "분석할 데이터가 없습니다. 데이터를 수집해주세요.",
        }
    return HttpResponse(json.dumps(data), content_type="application/json")