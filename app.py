from json import load
from flask import Flask, render_template, request, url_for
from flask_moment import Moment
from datetime import datetime
from pathlib import Path
import uuid
# import sqlalchemy as db
from sqlalchemy import func
import math
import csv
import re
import pandas as pd
import recognition.loadModel as ml
app=Flask(__name__)
# db_url:mysql://b9bd2e193517eb:507cc1f5@us-cdbr-east-06.cleardb.net/heroku_e40c35af84b7fd2?reconnect=true
#    username:b9bd2e193517eb
#    password:507cc1f5
#    db_host:s-cdbr-east-06.cleardb.net
#    db_name:heroku_e40c35af84b7fd2

# Connect to the database
# connection = pymysql.connect(host=os.environ.get('s-cdbr-east-06.cleardb.net'),
#                              user=os.environ.get('b9bd2e193517eb'),
#                              password=os.environ.get('507cc1f5'),
#                              db=os.environ.get('heroku_e40c35af84b7fd2'),
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)

# model 頁面load load 進來的資料
models=[]
with open('model1.csv',"r",encoding="utf-8") as f:
     for modelppt in csv.DictReader(f):     
         models.append(modelppt)
 


    
# 首頁,一鍵成影
@app.route('/')
def index():    
     return render_template('index.html')
pictures=[]
# 預測結果
@app.route('/home', methods=['GET'])
def home():
    try :
        if request.method == "GET":
         global pictures,pictures2
         data,data2=ml.predict()
        pictures=data
        pictures2=data2
        return render_template('home.html',pictures=pictures[:10],pictures2=pictures2[:10])
    except:
        return render_template('home.html',pictures=pictures,pictures2=pictures2)    
# 使用者 "你可能喜歡"的詳細頁面   
@app.route('/detail1')
def user1_detail1():
    pictures
    return render_template('user1_detail1.html',pictures=pictures[:30])
# 使用者 "其他人也看...."的詳細頁面 
@app.route('/detail2')
def user1_detail2():
    pictures2
    return render_template('user1_detail2.html',pictures2=pictures2[:30])
# model 頁面
@app.route('/model')
def model():  
    modelppt=models
    return render_template('model.html',modelppt=modelppt)
# 簡介頁面
@app.route('/about')
def about():
    df = pd.read_csv('member.csv', encoding='UTF-8')
    member = []
    for i in range(len(df)):
        member_dict = {}
        for j in df.columns:
            member_dict[j] = df[j][i]
        member.append(member_dict)
    member=[{i: member_dict[j][i] for i in [for j in range(len(df))]}]
    return render_template('about.html', member=member, len=len(member))

@app.route('/map')
def map1():  
   
    return render_template('map1.html')

# 讓flask app 跑起來    
if __name__=="__main__":
    app.run(debug=True)