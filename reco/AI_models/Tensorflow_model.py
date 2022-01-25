from django.db import models
import os
# 일부 버전에서 에러가 표시되나 정상 처리됨.
from tensorflow.keras.models import load_model
import numpy as np


# Create your models here.
class Recommend_house:
    def proc(self, data):
        print('data:', data)
        # self.res = data
        # data 형식: "1,1,1"
        data = np.array(data.split(','), dtype=int)
        print('변환된 data:', data)  # 변환된 data: [1 1 1]

        # 3개의 for문이 결합된 형태
        X = []
        for i in range(0, 5):  # 평가 횟수 5번, 0 ~ 2
            for j in range(1, 6):  # 평가 항목수 5개
                # print(i, j)
                # 선택한 번호화 같은 경우만 1을 할당
                # 사용자가 입력한 1은 배열 index 0에 해당함.
                if (data[i] == j):  # 1 == 1
                    X.append(1)  # 1
                else:
                    X.append(0)  # 0,0

        print(X)
        # 2차원 배열로 변환
        x_data = np.array([
            X,
        ])
        print(x_data)

        # 절대 경로 사용
        path = os.path.dirname(os.path.abspath(__file__))  # 스크립트파일의 절대경로
        print('path:', path);

        model = load_model(os.path.join(path, 'house.h5'))

        p = model.predict(x_data)  # 모델 사용, 2차원 데이터 전달
        print(p)
        index = np.argmax(p[0])  # 가장 높은 값의 index 산출, 가장 확률이 높은 값의 index
        # if index == 0:
        #     label = '개발 관련 도서'
        # elif index == 1:
        #     label = '해외 여행 관련 도서'
        # elif index == 2:
        #     label = '소설 관련 도서'
        #
        # print(label + ' 추천 필요')

        return index
