
import sqlite3
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import numpy as np
import os #디렉토리
from scipy import stats

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def cos_sim(A, B):
       return dot(A, B)/(norm(A)*norm(B))

# 데이타베이스 접속함수
def get_connect() :
    conn = sqlite3.connect("vegan.db",isolation_level=None)
    
    if conn:
        print('접속 완료')
    return conn

# 특정 테이블의 데이타를 리스트로 저장하는 함수
def get_country_list(sql_text) :
    # db 연결
    conn = get_connect()
    # 작업변수 생성
    cursor = conn.cursor()
    # sql 명령
    # 받아온 season 변수 이용해서 아래의 명령문 완성
    cursor.execute(sql_text)
    # 리스트에 저장
    country_list = [x[0] for x in cursor.fetchall()]
    print('저장완료')

    # db 종료
    conn.close()
    return country_list

def get_execute(sql_text) :
    # db 연결
    conn = get_connect()
    # 작업변수 생성
    cursor = conn.cursor()
    # sql 명령
    # 받아온 season 변수 이용해서 아래의 명령문 완성
    cursor.execute(sql_text)
    print('실행완료')

    conn.close()

    return 

def get_recommendations(USER_ingredient):

    get_execute("DROP TABLE 'SIMILAR'")
    get_execute("CREATE TABLE 'SIMILAR' ('NUM'	TEXT, 'TITLE' TEXT NOT NULL , 'INGREDIENT' TEXT NOT NULL ,'HOW'	TEXT NOT NULL, 'LEVEL'	TEXT NOT NULL, PRIMARY KEY('NUM'))")

    ID = get_country_list('SELECT NUM FROM recipeinfo')
    TITLE = get_country_list('SELECT TITLE FROM recipeinfo')
    INGREDIENT=get_country_list('SELECT ALL_INGREDIENT FROM recipeinfo')
    HOW=get_country_list('SELECT HOW FROM recipeinfo')
    LEVEL=get_country_list('SELECT DIFFICULTY FROM recipeinfo')

    ingredient='\n'.join(USER_ingredient)
    print(ingredient)

    final_data=pd.DataFrame({'ID':ID, 'TITLE': TITLE, 'INGREDIENT':INGREDIENT, 'HOW':HOW, 'LEVEL':LEVEL})

    search_data=pd.concat([final_data.loc[:, ['TITLE', 'INGREDIENT']], pd.DataFrame(data={'TITLE':['USER'], 'INGREDIENT': [ingredient]})], axis=0)
    
    tfidf = TfidfVectorizer()
    # INGREDIENT 에 대해서 tf-idf 수행
    tfidf_matrix = tfidf.fit_transform(search_data['INGREDIENT'])
    
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    sim_scores = list(enumerate(cosine_sim[(len(search_data)-1)]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = [x for x in sim_scores if x[1]!=0]

    sim_scores = sim_scores[1:]

    movie_indices = [i[0] for i in sim_scores]

    FINAL=final_data.iloc[movie_indices]
    print(FINAL.index)

    for i in range(0, len(FINAL)):
        print('index:',i)
        #print(FINAL[i:i+1].ID.values[0])
        #FINAL[i:i+1].ID.values[0]=str(FINAL[i:i+1].ID.values[0])
        #for x in range(0,len(FINAL[i:i+1].TITLE)):
            #FINAL[i:i+1].TITLE=re.sub('')

        print(FINAL[i:i+1].values)
        #print(FINAL.ID[i],FINAL.HOW[i] ,FINAL.LEVEL[i])
        d="', '".join([r for r in FINAL[i:i+1].values[0]])
        print(d)
        text="INSERT INTO SIMILAR (NUM, TITLE, INGREDIENT, HOW, LEVEL) values ('"+d+"')"
        print(text)
        get_execute(text)
    
    return FINAL