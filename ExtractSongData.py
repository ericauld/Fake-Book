from bs4 import BeautifulSoup
import requests
import re

song_links_class_code = '_2KJtL _1mes3 kWOod'

url_for_C  = 'https://www.ultimate-guitar.com/explore?tonality[]=15'
r = requests.get(url_for_C)
html_text = r.text

soup = BeautifulSoup(html_text, 'lxml')