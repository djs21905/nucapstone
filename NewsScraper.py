from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
config = Config()
config.browser_user_agent = user_agent
googlenews=GoogleNews(start='05/01/2020',end='05/31/2020')
googlenews.search('Trump')
result=googlenews.result()
df=pd.DataFrame(result)
print(df.head())
for i in range(2,20):
    googlenews.getpage(i)
    result=googlenews.result()
    df=pd.DataFrame(result)

df.to_excel("articles.xlsx")
