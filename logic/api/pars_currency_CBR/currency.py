import requests as rq
from bs4 import BeautifulSoup

def get_currency(cur):
    html = rq.get("https://cbr.ru/currency_base/daily/")
    
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, "html.parser")
        
        for i in soup.find_all("tr"):
            td = i.find_all("td")
            if td:
                if td[1].text == "USD":
                    usd = td[4].text
                if td[1].text == "EUR":
                    eur = td[4].text
        
        if cur == "USD":
            return round(float(usd.replace(",", ".")), 2)
        elif cur == "EUR":
            return round(float(eur.replace(",", ".")), 2)

print(get_currency("USD"))