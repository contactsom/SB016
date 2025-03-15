import readline
from bs4 import BeautifulSoup
import requests


try:
    source = requests.get("https://www.imdb.com/chart/top/")
    status=source.raise_for_status()
    #print(status)
    BeautifulSoup(source.text,'html.parser')

except Exception as e:
    print(e)




