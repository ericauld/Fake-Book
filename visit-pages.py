from requests import get
from bs4 import BeautifulSoup
import csv
import string
from time import sleep
from random import randint

def main():

    alpha = string.ascii_lowercase    
    for ch in alpha:
        # Output file is in append mode
        with open('{}_links.txt'.format(ch)) as links_file, open('chords.csv', 'a', newline='') as output_file:
            
            # Change to dict writer
            my_writer = csv.writer(output_file, delimiter=',', quotechar='"')

            if output_file.tell() == 0:
                my_writer.writerow(['Song Name','Artist','Key','Chords','Top','Key Guessed','Release Time'])

            # Limit to 5 for test
            i = 0
            for url in links_file:
                # song_info is a dict with keys like 'Song Name', 'Artist Name', 'Chords', etc.
                # Put appropriate sleeps here
                
                sleep(randint(1,4))

                song_info = scrape(url)

                # Edit here to set the song's harmonic key properly
                '''
                my_writer will take the dictionary song_info as argument, and, because it's a dictWriter,
                will put things in the right place
                '''
                my_writer.writerow([
                    song_info['Song Name'],
                    song_info['Artist Name'],
                    'A',
                    song_info['Chords'],
                    'True',
                    'True'
                ])
                
                #Limit to 5 for test
                i+=1
                if i >= 5:
                    break

        #break after 1 for test
        break
            
def scrape(url):
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')
    chord_elements = html_soup.find_all('span', class_='gt-chord')
    title_element = html_soup.find('h1', class_='gt-hero__title')

    chords = set()
    for chord_element in chord_elements:
        chords.add(chord_element.text)
    chords = ','.join(chords)

    song_name, artist_name = parse_title_element(title_element)

    return {
        'Song Name': song_name,
        'Artist Name': artist_name,
        'Chords': chords
    }

def parse_title_element(title_element):
    title_info_list = title_element.text.split()
    artist_name = ''
    song_name = ''

    for i,wd in enumerate(title_info_list):
        
        # Watch for the dash character which separates the artist name from song name
        if wd.encode('utf-8')==b'\xe2\x80\x93':
            try:
                # Eliminate trailing space if end of artist name was reached
                artist_name=artist_name[:-1]
            except: 
                raise Exception("Error when parsing artist name")
            break
        
        artist_name = artist_name + wd + " "
    
    song_name = ' '.join(title_info_list[i + 1:-1])
    return song_name, artist_name


if __name__ == '__main__':
    main()
