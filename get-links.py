from requests import get
from bs4 import BeautifulSoup
import csv
import string
from time import sleep
from random import randint

MAX_N_PAGES = 26

url = 'https://www.guitaretab.com/{}_top.html'
LINKS_OUTPUT_DIR = "Songbook/Links"

alpha = string.ascii_lowercase

n_pages_visited = 0
for ch in alpha:

    sleep(randint(1,4))

    response = get(url.format(ch))

    html_soup = BeautifulSoup(response.text, 'lxml')
    url_list = html_soup.find_all('a', class_='gt-link--primary')

    with open(LINKS_OUTPUT_DIR + "/{}_links.txt".format(ch), "w") as output_file:

        for link_element in url_list:
            output_file.write('http://guitaretab.com' + link_element['href'] + '\n')
        
    print("Wrote links to {}_links.txt".format(ch))

    n_pages_visited += 1
    if (n_pages_visited >= MAX_N_PAGES):
        break

# print(url_list)

#print(url.format('a'))

#response = get(url)

#html_soup = BeautifulSoup(response.text, 'lxml')

#chord_elements = html_soup.find_all('span', class_='gt-chord')
#title_element = html_soup.find('h1', class_='gt-hero__title')


