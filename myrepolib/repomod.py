from flask import Flask, render_template, request
from google.cloud import automl_v1beta1
from newspaper import Article


app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello():
    return render_template('hello.html') 



@app.route('/test', methods=["GET", "POST"])
def test():
    if request.method == 'POST':
        param1 =  request.form['Param1']
        article = Article(param1)
        article.download()
        article.parse()
        article.nlp()
        article.text
        text = article.text
        result= [text]
        labels = ['Text']


            
    return render_template('test.html', result= zip(result,labels))  #, prediction= round(pred_value * 100,2))

if __name__ == '__main__':
    app.run(debug=True)
