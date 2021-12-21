from news import bbc, cnn, finviz

bbcNews = bbc.BBCnews()

# fetching business, technology, world news
categories = ["business", "technology", "world"]
for category in categories:
    bbcNews.getNews(category)

cnnNews = cnn.CNNnews()
cnnNews.getNews("business")

finvizNews = finviz.FinvizNews()
finvizNews.finvizDaily()
