import requests
from bs4 import BeautifulSoup


def extract_news(parser)->list:
    """ Extract news from a given web page """
    news_list = []
    news_table = parser.table.findAll('table')[1]
    all_rows = news_table.findAll('tr')[:90]
    news_rows = [[all_rows[i], all_rows[i + 1]] for i in range(90) if i % 3 == 0]
    for news in news_rows:
        first_td = news[0].findAll('td')[2]
        second_td = news[1].findAll('td')[1]

        str_comments = second_td.findAll('a')[-1].text
        if str_comments == 'discuss':
            comments = 0
        elif str_comments[0] == "h":
            comments = 0
        else:
            comments = int(str_comments[0])

        points = int(second_td.span.text[0])

        link = str(first_td.a)[27:]
        href_end = link.find('"')
        href = link[:href_end]
        if 'http' not in href:
            url = 'https://news.ycombinator.com/' + href
        else:
            url = href

        news_dict = {'author': second_td.a.text,
                     'comments': comments,
                     'points': points,
                     'title': str(first_td.a.text),
                     'url': url
                     }

        news_list.append(news_dict)
    return news_list


def get_news(url='https://news.ycombinator.com/', n_pages=1) ->list:
    """ Collect news from a given web page """
    news = []
    next_index = 1
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_index += 1
        url = "https://news.ycombinator.com/?p=" + str(next_index)
        news.extend(news_list)
        n_pages -= 1
    return news
