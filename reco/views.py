import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# http://127.0.0.1:8000 --> /reco/templates/index.html
from reco.AI_models.Tensorflow_model import Recommend_house


def index(request):
    return render(request, 'index.html')


def recommend_house_start(request):
    # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    # /machine/templates/recommend_house/start.html
    return render(request, 'recommend_house/start.html', {})

def recommend_house_form1(request):
    # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    # /machine/templates/recommend_house/form1.html
    return render(request, 'recommend_house/form1.html', {})

def recommend_house_form2(request):
    step1 = int(request.GET['step1'])
    data = {'step1': step1} # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    # /machine/templates/recommend_house/form2.html
    return render(request, 'recommend_house/form2.html', data) # form2.html 파일로 데이터가 전송됨.

def recommend_house_form3(request):
    step1 = int(request.GET['step1'])
    step2 = int(request.GET['step2'])
    data = {'step1': step1, 'step2': step2} # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    # /machine/templates/recommend_house/form3.html
    return render(request, 'recommend_house/form3.html', data)

def recommend_house_form4(request):
    step1 = int(request.GET['step1'])
    step2 = int(request.GET['step2'])
    step3 = int(request.GET['step3'])
    data = {'step1': step1, 'step2': step2, 'step3': step3}
    return render(request, 'recommend_house/form4.html', data)

def recommend_house_form5(request):
    step1 = int(request.GET['step1'])
    step2 = int(request.GET['step2'])
    step3 = int(request.GET['step3'])
    step4 = int(request.GET['step4'])
    data = {'step1': step1, 'step2': step2, 'step3': step3, 'step4': step4}
    return render(request, 'recommend_house/form5.html', data)

def recommend_house_end(request):
    step1 = request.GET['step1']
    step2 = request.GET['step2']
    step3 = request.GET['step3']
    step4 = request.GET['step4']
    step5 = request.GET['step5']

    recommend_house = Recommend_house()  # 모델 사용
    data = ",".join([step1, step2, step3, step4, step5])
    print('data:', data)

    index = recommend_house.proc(data)  # 1 ~ 3 확률이 높은 index 리턴됨.
    print('index:', index)
    
    # /machine/templates/recommend_house/end.html
    return render(request, 'recommend_house/end.html', {'index': index})


def recommend_house_end_ajax(request):
    step1 = request.GET['step1']
    step2 = request.GET['step2']
    step3 = request.GET['step3']
    step4 = request.GET['step4']
    step5 = request.GET['step5']

    recommend_house = Recommend_house()  # 모델 사용
    data = ",".join([step1, step2, step3, step4, step5])
    print('data:', data)

    index = recommend_house.proc(data)
    print('index:', index)

    content = {
                'index': int(index),
              }
    # 날짜등의 변한 선언: cls=DjangoJSONEncoder
    # return HttpResponse(json.dumps(content, cls=DjangoJSONEncoder), content_type="application/json")
    return HttpResponse(json.dumps(content), content_type="application/json")