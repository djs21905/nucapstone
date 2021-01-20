from flask import Flask, render_template, request
from google.cloud import automl_v1beta1
from newspaper import Article
from newspaper import Config
from GoogleNews import GoogleNews
import re
import time

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello():
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
    


    return render_template('hello.html',result= zip(titles,outlet,date,links,img)) 




@app.route('/test', methods=["GET", "POST"])
def test():
    if request.method == 'POST':
        param1 =  request.form['Param1']
        regex = re.compile("((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*")
        if regex.match(param1):
            article = Article(param1)
            article.download()
            article.parse()
            article.nlp()
            text = article.text
            result= [text]
            labels = ['url worked!']
            print(labels,result)
        else: 
            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
            config = Config()
            config.browser_user_agent = user_agent
            googlenews=GoogleNews(start=time.strftime("%m/%d/%Y"),end= time.strftime("%m/%d/%Y"))
            googlenews.search(param1)
            result=googlenews.result()
            print(result)
            labels = ['this worked']
            print(labels,result)
        color = 0


      

            
    return render_template('test.html', result= zip(result,labels), color = color)  #, prediction= round(pred_value * 100,2))

if __name__ == '__main__':
    app.run(debug=True)
