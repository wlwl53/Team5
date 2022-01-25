import os

# print(os.getcwd()) # C:\kd1\ws_python\machine\ais\chatbot
# abs_path = '../../' # C:\kd1\ws_python\machine
# os.chdir(abs_path)
# print(os.getcwd())

from chatbot.config.GlobalParams import *
from chatbot.utils.Database import Database
from chatbot.utils.Preprocess import Preprocess
from chatbot.models.intent.IntentModel import IntentModel
from chatbot.models.ner.NerModel import NerModel
from chatbot.utils.FindAnswer import FindAnswer

# 전처리 객체 생성
p = Preprocess(word2index_dic='./chatbot/dict/chatbot_dict.bin', userdic='./chatbot/dict/user_dic.tsv')

# 질문/답변 학습 디비 연결 객체 생성
db = Database(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
)
db.connect()    # 디비 연결

query = "오전에 탕수육 10개 주문합니다."

# 의도 파악
intent = IntentModel(model_name='./chatbot/models/intent/intent_model.h5', proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]
print('intent_name:', intent_name)

# 개체명 인식
ner = NerModel(model_name='./chatbot/models/ner/ner_model.h5', proprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)
print('predicts:', predicts)
print('ner_tags:', ner_tags)
print("질문 : ", query)

print("=" * 100)
print("의도 파악 : ", intent_name)
print("개체명 인식 : ", predicts)
print("답변 검색에 필요한 NER 태그 : ", ner_tags)
print("=" * 100)

# 답변 검색
try:
    f = FindAnswer(db)
    answer_text, answer_image = f.search(intent_name, ner_tags)
    print('predicts:', predicts)
    print('answer_text:', answer_text)
    print('answer_image:', answer_image)
    answer = f.tag_to_word(predicts, answer_text)
except:
    answer = "죄송해요 무슨 말인지 모르겠어요"

print("답변:", answer)

db.close() # 디비 연결 끊음
