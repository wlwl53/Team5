from django.urls import path
from . import views

# 'news' is not a registered namespace 방지용 선언, 생략시 reverse() 함수에러 발생
app_name='news'

urlpatterns = [
    # 주소, 호출할 뷰, 뷰에 전달할 값은 생략, path 이름
    # http://127.0.0.1:8000/news/
    path('', views.index, name='index'),
    # http://127.0.0.1:8000/news/crawling
    path('crawling', views.crawling, name='crawling'),
    # http://127.0.0.1:8000/news/get_item
    path('get_item', views.get_item, name='get_item'),
    # http://127.0.0.1:8000/news/delete
    path('delete', views.delete, name='delete'),
    path('delete_all', views.delete_all, name='delete_all'),
    # http://127.0.0.1:8000/news/trend_analysis
    path('trend_analysis', views.trend_analysis, name='trend_analysis'),
    path('test', views.test, name='test'),
]
