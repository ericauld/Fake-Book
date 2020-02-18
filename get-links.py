from requests import get
from bs4 import BeautifulSoup
import csv
import string

url = 'https://www.guitaretab.com/{}_top.html'

alpha = string.ascii_lowercase

for ch in alpha:
    response = get(url.format(ch))

    html_soup = BeautifulSoup(response.text, 'lxml')
    url_list = html_soup.find_all('a', class_='gt-link--primary')

    with open("{}_links.txt".format(ch), "w") as output_file:

        for link_element in url_list:
            output_file.write('http://guitaretab.com' + link_element['href'] + '\n')
        
    #break after 1 for test
    break

# print(url_list)

#print(url.format('a'))

#response = get(url)

#html_soup = BeautifulSoup(response.text, 'lxml')

#chord_elements = html_soup.find_all('span', class_='gt-chord')
#title_element = html_soup.find('h1', class_='gt-hero__title')


