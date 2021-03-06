from requests import get
from bs4 import BeautifulSoup
import csv
import string
from time import sleep
from random import randint

def main(MAX_N_PAGES = None):
    if MAX_N_PAGES is None:
        print("You did not specify a max number of pages to visit to get links. Max has been automatically set to 26.")
        MAX_N_PAGES = 26

    url = 'https://www.guitaretab.com/{}_top.html'
    LINKS_OUTPUT_DIR = "/home/ubuntu/Songbook/Links"

    alpha = string.ascii_lowercase

    n_pages_visited = 0
    for ch in alpha:

        sleep(randint(1,4))
        try:
            response = get(url.format(ch))
        except:
            print("Error trying to visit " + url.format(ch))
            continue

        html_soup = BeautifulSoup(response.text, 'lxml')
        url_list = html_soup.find_all('a', class_='gt-link--primary')

        with open(LINKS_OUTPUT_DIR + "/{}_links.txt".format(ch), "w+") as output_file:

            for link_element in url_list:
                output_file.write('http://guitaretab.com' + link_element['href'] + '\n')
            
        print("Wrote links to {}_links.txt".format(ch))

        n_pages_visited += 1
        if (n_pages_visited >= MAX_N_PAGES):
            break

if __name__=='__main__':
    main()
