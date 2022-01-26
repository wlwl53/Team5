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

    # 트렌드분석
    path('news/', include('news.urls')),  # /news/urls.py
    path('property/', include('property.urls')),  # /property/urls.py

    # 챗봇
    path('ais/', include('ais.urls')),  # /ais/urls.py

    # 추천
    path('recommend_house/', include('reco.urls')),  # /reco/urls.py
]
