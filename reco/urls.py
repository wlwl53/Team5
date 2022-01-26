from django.urls import path
from . import views

# 'news' is not a registered namespace 방지용 선언, 생략시 reverse() 함수에러 발생
app_name='reco'

urlpatterns = [
    # 주소, 호출할 뷰, 뷰에 전달할 값은 생략, path 이름

    # http://127.0.0.1:8000/recommend_house/start/
    path('start/', views.recommend_house_start),
    # http://127.0.0.1:8000/recommend_house/form1/
    path('form1/', views.recommend_house_form1),
    path('form2/', views.recommend_house_form2),
    path('form3/', views.recommend_house_form3),
    path('form4/', views.recommend_house_form4),
    path('form5/', views.recommend_house_form5),
    path('end/', views.recommend_house_end),
    path('end_ajax/', views.recommend_house_end_ajax),  # 결과를 ajax로 리턴
]
