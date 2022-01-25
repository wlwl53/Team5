from django.test import TestCase

from reco.AI_models.Tensorflow_model import *
rb = Recommend_book()

# import reco.AI_models.Tensorflow_model as tm
# rb = tm.Recommend_book()

rb.proc('1,1,1') # 개발 관련 도서 추천 필요
rb.proc('2,2,2') # 해외 여행 관련 도서 추천 필요
rb.proc('3,3,3') # 소설 관련 도서 추천 필요
