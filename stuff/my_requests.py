from bs4 import BeautifulSoup as BS
import threading
import requests


def update_weekdays_html():
    #url = 'https://iek.irpin.com/for-students/rozklad-zm%D1%96n.html'        
    #r = requests.get(url, headers=my_request.headers)
    #html = BS(r.content, 'html.parser')
    #l = list()
    #
    #for el in html.select(".content > .row > p"):        
    #    title = el.select("a")
    #    url = title[0].get('href')
    #    r = requests.get(url, headers=my_request.headers)
    #    l.append(BS(r.content, 'html.parser'))


    for url in my_request.url_spreadsheets:
        r = requests.get(url, headers=my_request.headers)
        l.append(BS(r.content, 'html.parser'))

    my_request.weekdays_html = l
    del el, title, url, r, l

    threading.Timer(60*5, update_weekdays_html).start()


class Request:
    def __init__(self):
        self.weekdays_html = list()
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.url_spreadsheets = [
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vTl4XRsk2pxPAAumyB-0l2au3dkO7jC1PDeaTvctjBBU9HOpXyYwapoE_1PNlZsjrFDKFrpj-HK3oDK/pubhtml",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vQNDy6kP_Er32th8XuYpJRKI26iFJiauYR7IY7L-Kqfhu_SYYLUs3hg1MSzWHw2bglOLhwcXgYBiwJD/pubhtml",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vRpSkr059jyQUZv7HPp813kYED2fmigy14J8fThJ1Eo-6sEixrsjCezT281QCs0eMXBw4oSBoIFqhGM/pubhtml",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vRDA31eofItYZ5nQWwfvF26yq8Snig-oGbtdisOuAm2Ur0-v1h-Qwdmh3-eT3nQGRKW1e7D7KQ2UjUq/pubhtml",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vTwv0DHzrT97qJvh7lBovx6BubKJIO_gk_Lesgyn22RlxMclC3z1OW6TKJDhFe1CBJ6fGDSUcciZXzX/pubhtml",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vScVScHS0fxSDzdeJwVFgTXo0mSfgZ-Z65KzCLc1bcsX-73tI4UW4Fie8CMpCMVdTD34JNNoM0-oN-7/pubhtml",
        ]


    def get_weekday_html(self, weekday):    
        for iter, el in enumerate(self.weekdays_html):
            if (iter == weekday):
                return el


my_request = Request()