from bottle import route, run, template, redirect,request

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    row_id = request.query.id
    row = s.query(News).filter(News.id == row_id).one()
    row.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    recent_news = get_news()
    authors = [news['author'] for news in recent_news]
    titles = s.query(News.title).filter(News.author.in_(authors)).subquery()
    existing_news = s.query(News).filter(News.title.in_(titles)).all()
    titles_bd = [i.title for i in existing_news]
    authors_bd = [i.author for i in existing_news]
    for news in recent_news:
        if not existing_news or(news['title'] not in titles_bd and news["author"] not in authors_bd):
            news_add = News(title=news['title'],
                            author=news['author'],
                            url=news['url'],
                            comments=news['comments'],
                            points=news['points'])
            s.add(news_add)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    recently_marked_news = s.query(News).filter(News.title not in x_train and News.label != None).all()
    x_extra_train = [row.title for row in recently_marked_news]
    y_extra_train = [row.label for row in recently_marked_news]
    classifier.fit(x_extra_train, y_extra_train)

    blank_rows = s.query(News).filter(News.label == None).all()
    x = [row.title for row in blank_rows]
    labels = classifier.predict(x)
    classified_news = [blank_rows[i] for i in range(len(blank_rows)) if labels[i] == 'good']
    return template('recommended', rows=classified_news)


if __name__ == "__main__":
    s = session()
    classifier = NaiveBayesClassifier()
    marked_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in marked_news]
    y_train = [row.label for row in marked_news]
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
