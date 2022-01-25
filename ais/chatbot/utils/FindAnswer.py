class FindAnswer:
    def __init__(self, db):
        self.db = db

    # 검색 쿼리 생성
    def _make_query(self, intent_name, ner_tags):
        sql = "select * from chatbot_train_data"
        if intent_name != None and ner_tags == None: # intent만 있는 경우
            sql = sql + " where intent='{}' ".format(intent_name)

        elif intent_name != None and ner_tags != None:  # intent, ner이 있는 경우
            where = ' where intent="%s" ' % intent_name
            if (len(ner_tags) > 0):
                where += 'and ('
                for ne in ner_tags:
                    where += " ner like '%{}%' or ".format(ne)
                where = where[:-3] + ')'
            sql = sql + where

        # 동일한 답변이 2개 이상인 경우, 랜덤으로 선택
        sql = sql + " order by rand() limit 1"
        
        return sql

    # 답변 검색
    def search(self, intent_name, ner_tags):
        # 의도명, 개체명으로 답변 검색
        sql = self._make_query(intent_name, ner_tags)
        answer = self.db.select_one(sql)

        # 검색되는 답변이 없으면 의도명만 검색
        if answer is None:
            sql = self._make_query(intent_name, None)
            answer = self.db.select_one(sql)

        return (answer['answer'], answer['answer_image'])

    # NER 태그를 실제 입력된 단어로 변환
    def tag_to_word(self, ner_predicts, answer):
        for word, tag in ner_predicts: 
            # [('오전', 'B_DT'), ('탕수육', 'B_FOOD'), ('10', 'O'), ('개', 'O'), ('주문', 'O')]

            # 변환해야하는 태그가 있는 경우 추가
            if tag == 'B_FOOD' or tag == 'B_DT' or tag == 'B_TI':
                # {B_FOOD} 주문 처리 완료되었습니다. 주문해주셔서 감사합니다.
                # 간짜장 주문 처리 완료되었습니다. 주문해주셔서 감사합니다.
                answer = answer.replace(tag, word) # tag를 word로 변환

        answer = answer.replace('{', '')
        answer = answer.replace('}', '')
        return answer
    
