"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from news import views # 'news' package로부터 'views' python 파일 import

urlpatterns = [
    path('admin/', admin.site.urls),
    # http://127.0.0.1:8000/
    path('news/', include('news.urls')),  # /news/urls.py
    path('recommend_house/start/', views.recommend_house_start),
    path('recommend_house/form1/', views.recommend_house_form1),
    path('recommend_house/form2/', views.recommend_house_form2),
    path('recommend_house/form3/', views.recommend_house_form3),
    path('recommend_house/form4/', views.recommend_house_form4),
    path('recommend_house/form5/', views.recommend_house_form5),
    path('recommend_house/end/', views.recommend_house_end),
    path('recommend_house/end_ajax/', views.recommend_house_end_ajax),  # 결과를 ajax로 리턴
]