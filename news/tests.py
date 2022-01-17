
# Create your tests here.
import datetime

import pymysql

# now = datetime.datetime.now()
# print(now)

conn = pymysql.connect(host='localhost', user='pyuser', password='1234',
                           db='team5', charset='utf8')

cursor = conn.cursor()
sql_pre = '''
    SELECT COUNT(newsno) AS cnt
    FROM news_news
    '''
cursor.execute(sql_pre)
row = cursor.fetchone()
print(row[0])
if row[0]==0:
    print('없음')
# print('>> ' + str(row))
# print(row[0][0])