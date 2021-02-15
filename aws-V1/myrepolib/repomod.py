from flask import Flask, render_template, request, redirect
from newspaper import Article
from newspaper import Config
from GoogleNews import GoogleNews
import re
import time
import nltk
import hashlib
from ip2geotools.databases.noncommercial import DbIpCity
import psycopg2
import pandas as pd
#Text cleaning
from text_cleaner import text_cleaner
import sys
import os
import datetime
import tensorflow as tf

from predict_against_model import load_model, load_vocabulary, predict_results


#NTLK
from nltk.corpus import stopwords  # stopwords
from nltk.stem.porter import PorterStemmer #Stemming
from nltk.stem import WordNetLemmatizer # Lemmatization
import re, string #Text cleaning

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    #visitor table 
    con = psycopg2.connect("dbname=postgres user=postgres password=northwesternmsds host=potsgres.cv4el6jr6eml.us-east-1.rds.amazonaws.com port=5432")
    cur = con.cursor()
    response = DbIpCity.get(str(request.remote_addr), api_key='free')
    postgres_insert_query = """ INSERT INTO visitor (ip, location, date,time) VALUES (%s,%s,%s,%s)"""
    record_to_insert = (str(request.remote_addr), str(response.region),datetime.datetime.now(),datetime.datetime.now().time())
    cur.execute(postgres_insert_query, record_to_insert)

    con.commit()
    con.close()


    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    googlenews=GoogleNews(start=time.strftime("%m/%d/%Y"),end= time.strftime("%m/%d/%Y"))
    googlenews.search('news')
    result=googlenews.result()
    trun = result[0:3]

    titles = []
    outlet = [] 
    date = []
    links = []
    img = []
    for item in trun:
        titles.append(item['title'])
        outlet.append(item['media'])
        date.append(item['date'])
        links.append(item['link'])
        url  = item['link']
        article = Article(url)
        article.download()
        article.parse()
        img.append(article.top_image)
    
    return render_template('home.html',result= zip(titles,outlet,date,links,img)) 

@app.route('/result', methods=["GET", "POST"])
def result():
    titles1 = []
    outlet1 = [] 
    date1 = []
    links1 = []
    img1 = []
    hash = []
    article_text = []

    STOPWORDS = stopwords.words('english')
    STOPWORDS = [word.translate(str.maketrans('','',string.punctuation)) for word in STOPWORDS] # 
    LEMMING =  WordNetLemmatizer()
  
    if request.method == 'POST':

        param1 =  request.form['Param1']
        response = DbIpCity.get(str(request.remote_addr), api_key='free')
        regex = re.compile("((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*")
        #establish db connection 
        con = psycopg2.connect("dbname=postgres user=postgres password=northwesternmsds host=potsgres.cv4el6jr6eml.us-east-1.rds.amazonaws.com port=5432")
        print('Connecting to PostgreSQL db.....')

        cur = con.cursor()

        print('DB connection successful ')

        if regex.match(param1):
            isurl = True
        else:
            isurl = False

        postgres_insert_query = """ INSERT INTO info (ip, url, location, date,time,isurl) VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (str(request.remote_addr), param1, str(response.region),datetime.datetime.now(),datetime.datetime.now().time(),isurl)
        cur.execute(postgres_insert_query, record_to_insert)

        con.commit()
        con.close()

        
        if regex.match(param1):
            article = Article(param1)
            article.download()
            article.parse()
            article.nlp()
            text = article.text
            

            titles1.append(article.title)
            outlet1.append(re.split('www.|.com',param1)[1].upper())
            date1.append(str(article.publish_date)[0:16])
            links1.append(param1)
            img1.append(article.top_image)
            article_text.append(text)
        else: 
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            config = Config()
            config.browser_user_agent = user_agent
            googlenews=GoogleNews(start=time.strftime("%m/%d/%Y"),end= time.strftime("%m/%d/%Y"))
            googlenews.search(param1)
            result=googlenews.result()

            # Handling of Keywords
            if len(result) == 0:
                return render_template("nothingfound.html")
            elif len(result) <= 6:
                trun = result[0:]
            else:
                trun = result[0:6]

            for item in trun:
                try:
                    titles1.append(item['title'])
                    outlet1.append(item['media'])
                    date1.append(item['date'])
                    links1.append(item['link'])
                    url1  = item['link']
                    #extract text
                    article = Article(item['link'])
                    article.download()
                    article.parse()
                    article.nlp()
                    text = article.text
                    article_text.append(text)
                    #End of article text extraction
                    article1 = Article(url1)
                    article1.download()
                    article1.parse()
                    img1.append(article1.top_image)
                except:
                    pass
           
        for item in titles1:
            hash_object = hashlib.sha1(item.encode('utf-8'))
            hex_dig = hash_object.hexdigest()  
            hash.append(hex_dig)

        #Clean Text 
        cleaned_text = []
        for item in article_text:    
            cleanse = text_cleaner(item)
            cleanse2 = cleanse.pop()
            cleaned_text.append(cleanse2)
        
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '-1'
        tf.saved_model.LoadOptions(experimental_io_device=None)
        os.chdir(os.getcwd())
        model_path = os.getcwd() + '/Models/content_Transformer_model'
        vocabulary_path = os.getcwd() +'/Data/word_frequency/content_word_map_dict.json'
        with tf.device('/cpu:0'):
             model = load_model(model_path)
             vocab = load_vocabulary(vocabulary_path)

        #Model Prediction based on cleaned text
        model_results = []
        for text in cleaned_text:   
            prediction = predict_results(text,model,vocab)
            #remove nested list
            prediction_pop = list(prediction).pop()
            scaled_prediction = (prediction_pop * 50 ) + 50
            model_results.append(list(scaled_prediction).pop())
        
        bar = []
        for item in model_results:
            bar.append(100-item)

            
    return render_template('result.html',  keywordprocess = zip(titles1,outlet1,date1,links1,img1,hash,model_results,bar)) 

@app.route('/vote', methods=["GET", "POST"])
def vote():
    if request.method == 'POST':
        hash_id = request.form.get('pk')
        print(hash_id)
        con = psycopg2.connect("dbname=postgres user=postgres password=northwesternmsds host=potsgres.cv4el6jr6eml.us-east-1.rds.amazonaws.com port=5432")
        print('Connecting to PostgreSQL db.....') 
        cur = con.cursor()
        print('DB connection successful ')
        fail = False
        if request.form['vote'] == 'Liberal':
            a = 'liberal'
            try:
                postgres_insert_query = """ INSERT INTO voting (ip, liberal, conservative,hash,date,time) VALUES (%s,%s,%s,%s,%s,%s)"""
                record_to_insert = (str(request.remote_addr), 1,0,hash_id,datetime.datetime.now(),datetime.datetime.now().time())
                cur.execute(postgres_insert_query, record_to_insert)
                message = 'You voted that the article should be rated as more liberal than our model ranking. Thanks for the input.'
            except:
                fail = True
                message = 'You already voted for this article. You can only vote once per article.'
                pass  
        elif request.form['vote'] == 'Conservative':
            a = 'conservative'
            try:
                postgres_insert_query = """ INSERT INTO voting (ip, liberal, conservative,hash,date,time) VALUES (%s,%s,%s,%s,%s,%s)"""
                record_to_insert = (str(request.remote_addr), 0,1,str(hash_id),datetime.datetime.now(),datetime.datetime.now().time())
                cur.execute(postgres_insert_query, record_to_insert)
                message = 'You voted that the article should be rated as more conservative than our model ranking. Thanks for the input.'
            except:
                fail = True
                message = 'You already voted for this article. You can only vote once per article.'
                pass
        con.commit()
        con.close()    

    return render_template('vote.html',test=a,message=message,fail = fail) 

if __name__ == '__main__':
    app.run(host='0.0.0.0',port= 8080)
