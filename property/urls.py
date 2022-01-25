from django.urls import path
from . import views

# 'news' is not a registered namespace 방지용 선언, 생략시 reverse() 함수에러 발생
app_name='property'

urlpatterns = [
    # 주소, 호출할 뷰, 뷰에 전달할 값은 생략, path 이름
    # http://127.0.0.1:8000/property/
    path('', views.index, name='index'),
    path('test', views.test, name='test'),
    path('chart1', views.chart1, name='chart1'),
    path('chart2', views.chart2, name='chart2'),
    path('chart3', views.chart3, name='chart3'),
]

