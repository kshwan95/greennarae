from typing import Final
from flask import Flask, render_template, jsonify, request
import db
import pandas as pd
import re

app = Flask(__name__) 


## URL 별로 함수명이 같거나, 
## route('/') 등의 주소가 같으면 안됩니다. 

@app.route('/') 
def main(): 
    return render_template('01_main_page.html') 

@app.route('/season_page') 
def season_page(): 
    return render_template('02_season_page.html') 

@app.route('/ingredient_page/<season>', methods=['GET']) 
def ingredient_page(season):
    #SELECT ingredient FROM SEASON WHERE SEASON=='Autumn'
    sql_text="SELECT ingredient FROM SEASON WHERE SEASON=='"+season+"';"
    country_list = sorted(db.get_country_list(sql_text))
    if season=='Autumn':
        season='가을, '+season
    if season=='Spring':
        season='봄, '+season
    if season=='Summer':
        season='여름, '+season
    if season=='Winter':
        season='겨울, '+season
    return render_template('03_ingredient_page.html', season_state=season, country_list=country_list) 

@app.route('/how_page', methods=['GET']) 
def how_page():
    if request.method =='GET':
        data=request.values.getlist('chk[]')
        print(data)

    Final_data=db.get_recommendations(data)
    #print(Final_data)
    return render_template('04_how_page.html', data=data)     

@app.route('/level_page/<search>') 
def level_page(search): 
    print(search)
    how=search
    #SELECT title FROM recipeinfo where id==1
    return render_template('05_level_page.html', how=how)  

@app.route('/search_page/<search>') 
def search_page(search):
    print(search)
    user_how=re.split('&', search)[0]
    user_level=re.split('&', search)[1]

    sql_text="SELECT NUM FROM SIMILAR WHERE HOW=='"+user_how+"' and LEVEL=='"+user_level+"';"
    top_ID = db.get_country_list(sql_text)[:3]

    print(top_ID)

    top_TITLE=[]
    top_PIC=[]

    for i in top_ID:
        sql_text="SELECT TITLE FROM recipeinfo WHERE NUM=='"+i+"';"
        top_TITLE.append(db.get_country_list(sql_text)[0])
        sql_text="SELECT PICTURE FROM recipeinfo WHERE NUM=='"+i+"';"
        top_PIC.append(db.get_country_list(sql_text)[0])

    #sql_text="SELECT TITLE FROM recipeinfo WHERE HOW=='"+user_how+"' &LEVEL=='"+user_level+"';"
    #top_title = db.get_country_list(sql_text)

    #sql_text="SELECT PIC FROM recipeinfo WHERE HOW=='"+user_how+"' &LEVEL=='"+user_level+"';"
    #top_pic = db.get_country_list(sql_text)

    return render_template('06_search_page.html', top_ID=top_ID, top_TITLE=top_TITLE, top_PIC=top_PIC)  

@app.route('/recipe_page/<top_ID>') 
def recipe_page(top_ID):

    print(top_ID)

    sql_text="SELECT TITLE FROM recipeinfo WHERE NUM=='"+top_ID+"';"
    top_TITLE=db.get_country_list(sql_text)[0]

    sql_text="SELECT MAIN_INGREDIENT FROM recipeinfo WHERE NUM=='"+top_ID+"';"
    top_main_ingredient=db.get_country_list(sql_text)[0]

    sql_text="SELECT SUB_INGREDIENT FROM recipeinfo WHERE NUM=='"+top_ID+"';"
    top_sub_ingredient=db.get_country_list(sql_text)[0]

    sql_text="SELECT HOW FROM recipeinfo WHERE NUM=='"+top_ID+"';"
    top_how=db.get_country_list(sql_text)[0]

    #sql_text="SELECT ALL_RECIPE FROM recipeinfo WHERE NUM=='"+top_ID+"';"
    #top_recipe=db.get_country_list(sql_text)[0].split('\n')

    top_recipe=[]

    for i in range(1,26):
        sql_text="SELECT RECIPE"+str(i)+" FROM recipeinfo WHERE NUM=='"+top_ID+"';"
        if db.get_country_list(sql_text) != 'null':
            top_recipe.append(db.get_country_list(sql_text)[0])


    return render_template('07_recipe_page.html', top_TITLE=top_TITLE, top_main_ingredient=top_main_ingredient, top_sub_ingredient=top_sub_ingredient, top_how=top_how, top_recipe=top_recipe)

if __name__=='__main__':
     app.run()








