import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# http://127.0.0.1:8000 --> /ais/templates/ais_index.html
from ais.chatbot_model import Chatbot # chatbot_model.py안의 Chatbot class import

def index(request):
    return render(request, 'ais_index.html')

def chat_test(request):
    # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    # /machine/templates/chatbot/chat_test.html
    return render(request, 'chatbot/chat_test.html', {})

def chatting(request):
    # 출력 페이지로 보낼 값을 {.....} 블럭에 선언
    # /ais/templates/chatbot/chat_test.html
    return render(request, 'chatbot/chatting.html', {})

def chatting_query(request):
    print('Chatbot Ajax 요청 받음')
    msg = request.GET['msg']

    chatbot = Chatbot()
    result = chatbot.proc(msg)

    content = {
                'result': result,
     }
    # 날짜등의 변한 선언: cls=DjangoJSONEncoder
    # return HttpResponse(json.dumps(content, cls=DjangoJSONEncoder), content_type="application/json")
    return HttpResponse(json.dumps(content), content_type="application/json")

