from django.http import HttpResponse
from django.shortcuts import render
import json

import pandas as pd
import pyecharts
from pyecharts import Bar
from pyecharts import Line

# Create your views here.
def index(request):
    #return HttpResponse("property first page")
    REMOTE_HOST = "https://pyecharts.github.io/assets/js"
    df_property = data_load()

    gu_trade_count_cost = gugroup_preprocessing(df_property)

    bar_chart = bar2(gu_trade_count_cost)
    # print(bar_chart)

    # l3d = line3d()
    context = dict(
        myechart=bar_chart.render_embed(),
        host=REMOTE_HOST,
        script_list=bar_chart.get_js_dependencies()
    )
    # return HttpResponse(template.render(context, request))
    return render(request, 'pyecharts.html', context)  # render
    #return render(request, 'pyecharts.html')

def data_load():
    df = pd.read_csv('./property/static/csv/property_20210101_21211231.csv', encoding='euc-kr')
    ## EDA
    # 데이터 확인
    # print(df.head())

    # 통계값 확인
    # print(df.describe())

    # null값 확인
    # print(print(np.sum(pd.isnull(df))))

    # 필요한 컬럼만 추출
    df1 = df['시군구']
    df2 = df.iloc[:, 4:11]
    df_property = pd.concat([df1, df2], axis=1)

    # 거래금액 , 제거
    df1 = df_property['거래금액(만원)']
    data = []
    for row in df1:
        # print(row.replace(",",""))
        data.append(int(row.replace(",", "")))

    df_property['거래금액(만원)'] = pd.DataFrame(data)

    # 1평당 거래가격 = 거래금액 / 평수(전용면적/3.3)
    df2 = (df_property['거래금액(만원)'] / (df_property['전용면적(㎡)'] / 3.3)).round(0).astype(int)
    df_property['평당 거래금액'] = df2

    # 시,구,동 분리
    df1 = df_property['시군구']

    data = []
    for row in df1:
        data.append(row.split())

    pd2 = pd.DataFrame(data, columns=['시', '구', '동'])

    df_property = pd.concat([pd2, df_property.iloc[:, 1:]], axis=1)

    return df_property

def gugroup_preprocessing(df_property):
    gu_group = df_property[['평당 거래금액']].groupby(df_property['구'])
    # print(gu_group.count().rename(columns={"평당 거래금액": "거래량"}))

    # 구별 거래량
    gu_trade_count = gu_group.count().rename(columns={"평당 거래금액": "거래량"})

    # 구별 거래금액 평균
    # gu_cost_data = gu_group.mean().sort_values(by=['평당 거래금액'], ascending=False).astype(int)
    gu_cost_data = gu_group.mean().astype(int)

    # print(gu_trade_count)
    # print(gu_cost_data)

    gu_trade_count_cost = pd.concat([gu_trade_count, gu_cost_data], axis=1, join='inner').sort_values(by=['평당 거래금액'],
                                                                                                      ascending=False)
    gu_trade_count_cost = gu_trade_count_cost.reset_index()
    #print(gu_trade_count_cost)
    return gu_trade_count_cost

def ym_preprocessing(df_property):
    # 계약년월별 거래량
    contract_ym = df_property[['시', '계약년월']].groupby(['계약년월']).count()
    contract_ym = contract_ym.rename(columns={"시": "거래량"}).reset_index()
    #print(contract_ym)
    return contract_ym

def bar(gu, attr):
    bar = Bar("구별 1평당 거래금액의 평균", "단위 : 만원")
    bar.add("", gu, attr,mark_point=["max", "min"], xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30, label_pos='inside',)
    bar.width=800
    return bar

def bar1(gu_trade_count_cost):
    xaxis = gu_trade_count_cost['구'].tolist()
    cost_arr = gu_trade_count_cost['평당 거래금액'].tolist()

    bar = Bar("구별 거래금액의 평균", "1평당 평균 거래금액", title_pos='center')
    #bar.use_theme("wonderland")
    bar.add("", xaxis, cost_arr, mark_point=["max", "min"], xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=0,
            label_pos='inside',
            yaxis_name="단위 : 만원", yaxis_name_pos='end', yaxis_name_size=12, yaxis_name_gap=25, )

    bar.width = 900

    return bar

def bar2(gu_trade_count_cost):
    xaxis = gu_trade_count_cost['구'].tolist()
    count_arr = gu_trade_count_cost['거래량'].tolist()

    bar = Bar("구별 거래량", "", title_pos='center')
    #bar.use_theme("walden")
    bar.add("", xaxis, count_arr, is_label_show=True, xaxis_interval=0, xaxis_rotate=30, yaxis_max=5000,
            yaxis_name="단위 : 건", yaxis_name_pos='end', yaxis_name_size=12, yaxis_name_gap=25, )

    bar.width = 900

    return bar

def line1(contract_ym):
    xaxis = contract_ym['계약년월'].tolist()
    ym_count = contract_ym['거래량'].tolist()
    xaxis = list(map(str, xaxis))
    month_list = []
    for x in xaxis:
        month_list.append(str(x)[4:] + '월')

    line = Line("월별 거래량")
    #line.use_theme("walden")
    line.add("거래량", month_list, ym_count, is_label_show=True, yaxis_max=7000,
             yaxis_name="단위 : 건", yaxis_name_pos='end', yaxis_name_size=12, yaxis_name_gap=10)

    line.width = 900
    return line

def test(request):
    return render(request, 'chart_index.html')

def chart1(request):
    REMOTE_HOST = "https://pyecharts.github.io/assets/js"

    df_property = data_load()
    #print(df_property)

    gu_trade_count_cost = gugroup_preprocessing(df_property)
    contract_ym = ym_preprocessing(df_property)


    bar_chart = bar1(gu_trade_count_cost)

    context = dict(
        myechart=bar_chart.render_embed(),
        host=REMOTE_HOST,
        script_list=bar_chart.get_js_dependencies()
    )

    #return render(request, 'chart_index.html', context)  # render
    return HttpResponse(json.dumps(context), content_type="application/json")

def chart2(request):
    REMOTE_HOST = "https://pyecharts.github.io/assets/js"
    df_property = data_load()

    gu_trade_count_cost = gugroup_preprocessing(df_property)

    bar_chart = bar2(gu_trade_count_cost)
    #print(bar_chart)

    # l3d = line3d()
    context = dict(
        myechart=bar_chart.render_embed(),
        host=REMOTE_HOST,
        script_list=bar_chart.get_js_dependencies()
    )

    #return render(request, 'chart_index.html', context)  # render
    return HttpResponse(json.dumps(context), content_type="application/json")

def chart3(request):
    REMOTE_HOST = "https://pyecharts.github.io/assets/js"
    df_property = data_load()

    contract_ym = ym_preprocessing(df_property)

    line_chart = line1(contract_ym)

    context = dict(
        myechart=line_chart.render_embed(),
        host=REMOTE_HOST,
        script_list=line_chart.get_js_dependencies()
    )

    #return render(request, 'chart_index.html', context)  # render
    return HttpResponse(json.dumps(context), content_type="application/json")