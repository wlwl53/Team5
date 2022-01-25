
from django.contrib import admin
from django.urls import path

from . import views

app_name='ais'

urlpatterns = [
    path('', views.index), # views 모듈(파일)의 index 함수 호출, ais_index.html
    path('chatbot/chatting/', views.chatting, name='chatbot'),  # chatting.html
    path('chatbot/chatting_query/', views.chatting_query),   # 결과를 ajax로 리턴
]



