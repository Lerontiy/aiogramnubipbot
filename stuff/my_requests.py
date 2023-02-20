from bs4 import BeautifulSoup as BS
import threading
import requests


def update_weekdays_html():
    url = 'https://iek.irpin.com/for-students/rozklad-zm%D1%96n.html'        
    r = requests.get(url, headers=my_request.headers)
    html = BS(r.content, 'html.parser')
    l = list()
    
    for el in html.select(".content > .row > p"):        
        title = el.select("a")
        url = title[0].get('href')
        r = requests.get(url, headers=my_request.headers)
        l.append(BS(r.content, 'html.parser'))

    my_request.weekdays_html = l
    print(my_request.weekdays_html)
    del el, title, url, r, l

    threading.Timer(60*5, update_weekdays_html).start()


class Request:
    def __init__(self):
        self.weekdays_html = list()
        self.headers = {'User-Agent': 'Mozilla/5.0'}


    def get_weekday_html(self, weekday):    
        for iter, el in enumerate(self.weekdays_html):
            print(repr(iter), repr(weekday))
            if (iter == weekday):
                print(el)
                return el


my_request = Request()