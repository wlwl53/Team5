from chatbot_model import Chatbot

chatbot = Chatbot()

query = '오전에 탕수육 10개 주문합니다.'
answer = chatbot.proc('오전에 탕수육 10개 주문합니다.')
print(answer)

