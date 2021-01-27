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


nltk.download('punkt')

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello():
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    googlenews=GoogleNews(start=time.strftime("%m/%d/%Y"),end= time.strftime("%m/%d/%Y"))
    googlenews.search('news')
    result=googlenews.result()
    print(len(result))


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
    


    return render_template('hello.html',result= zip(titles,outlet,date,links,img)) 




@app.route('/test', methods=["GET", "POST"])
def test():
    titles1 = []
    outlet1 = [] 
    date1 = []
    links1 = []
    img1 = []
    hash = []
  
    if request.method == 'POST':

        param1 =  request.form['Param1']
        response = DbIpCity.get('61.555.51.123', api_key='free')
        print(request.remote_addr,param1,response.country,response.region)


        #establish db connection 
        con = psycopg2.connect("dbname=capstone user=postgres password=admin host=localhost port=5432")
        print('Connecting to PostgreSQL db.....')

        cur = con.cursor()

        print('DB connection successful ')
        region = response.region

        postgres_insert_query = """ INSERT INTO info (ip, url, location) VALUES (%s,%s,%s)"""
        record_to_insert = (str(request.remote_addr), param1, str(response.region))
        cur.execute(postgres_insert_query, record_to_insert)

        con.commit()
        con.close()


        regex = re.compile("((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*")
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
        else: 
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            config = Config()
            config.browser_user_agent = user_agent
            googlenews=GoogleNews(start=time.strftime("%m/%d/%Y"),end= time.strftime("%m/%d/%Y"))
            googlenews.search(param1)
            result=googlenews.result()
          
         

            
            # keyword process flow 
            if len(result) <= 6:
                trun = result[0:]
            else:
                trun = result[0:6]

            print(len(trun))
            for item in trun:
                try:
                    titles1.append(item['title'])
                    outlet1.append(item['media'])
                    date1.append(item['date'])
                    links1.append(item['link'])
                    url1  = item['link']
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

            
    return render_template('test.html',  keywordprocess = zip(titles1,outlet1,date1,links1,img1,hash)) 


@app.route('/result', methods=["GET", "POST"])
def result():
    if request.method == 'POST':
        print(request.form.get('pk'))
        if request.form['vote'] == 'Liberal':
            a = 'liberal'
        elif request.form['vote'] == 'Middle':
            a = 'middle'
        elif request.form['vote'] == 'Conservative':
            a = 'conservative'
            
     
     

    return render_template('vote.html',test=a) 



if __name__ == '__main__':
    app.run(debug=True)
