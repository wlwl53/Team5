from django.test import TestCase

# Create your tests here.
import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rc

### 시각화
### pyecharts -> Version: 0.5.11
import pyecharts
from pyecharts import Bar

def bar(gu, attr):
    bar = Bar("구별 1평당 거래금액의 평균", "단위 : 만원")
    bar.add("", gu, attr,mark_point=["max", "min"], xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30, label_pos='inside',)
    bar.width=800
    return bar

df = pd.read_csv('./property/static/csv/property_20210101_21211231.csv', encoding='euc-kr')
## EDA
# 데이터 확인
#print(df.head())

# 통계값 확인
#print(df.describe())

# null값 확인
#print(print(np.sum(pd.isnull(df))))

# 필요한 컬럼만 추출
df1 = df['시군구']
df2 = df.iloc[:,4:11]
df_property = pd.concat([df1,df2],axis=1)

# 거래금액 , 제거
df1 = df_property['거래금액(만원)']
data =[]
for row in df1:
    #print(row.replace(",",""))
    data.append(int(row.replace(",","")))

df_property['거래금액(만원)']= pd.DataFrame(data)

# 1평당 거래가격 = 거래금액 / 평수(전용면적/3.3)
df2=(df_property['거래금액(만원)']/(df_property['전용면적(㎡)']/3.3)).round(0).astype(int)
df_property['평당 거래금액'] = df2

#시,구,동 분리
df1 = df_property['시군구']

data =[]
for row in df1:
    data.append(row.split())

pd2 = pd.DataFrame(data, columns = ['시','구','동'])

df_property = pd.concat([pd2,df_property.iloc[:,1:]],axis=1)

# '구' 그룹화 평당거래금액 추출
#df_property.groupby(['구']).mean()
gu_group = df_property[['평당 거래금액']].groupby(df_property['구'])
gu_group.size()
gu_group.sum()
gu_group = gu_group.mean().sort_values(by=['평당 거래금액'], ascending=False).astype(int)

print(gu_group)

gu = gu_group.reset_index()['구'].tolist()
attr = gu_group.reset_index()['평당 거래금액'].tolist()

bar_chart = bar(gu, attr)

