from requests import get
from bs4 import BeautifulSoup
import csv
import string
from time import sleep
from random import randint
import csv

def main():

    MAX_N_PAGES = 1500
    ATTRIBUTES_IN_OUTPUT = ['Song Version Name', 'Artist Name', 'Song Key', 'Chords', 'Key Is Guessed']
    LINKS_DIRECTORY = "/home/ubuntu/Fake-Book/Links"

    alpha = string.ascii_lowercase    
    for ch in alpha:
        # Output file is in append mode
        with open(LINKS_DIRECTORY + '/{}_links.txt'.format(ch)) as links_file, open('chords.csv', 'a', newline='') as output_file:

            n_pages_visited = 0
            
            # DictWriter will leave a field empty if an entry is missing one of the keys
            my_writer = csv.DictWriter(output_file, ATTRIBUTES_IN_OUTPUT)

            # tell() should return zero if and only if the file was just created
            if output_file.tell() == 0:
                my_writer.writeheader()

            for url in links_file:
                # Remove newline
                if url:
                    url = url[:-1]
                sleep(randint(1,4))

                # song_info is a dict
                song_info = scrape(url)
                n_pages_visited += 1
                
                if not song_info:
                    # If song_info comes back empty, the scrape method 
                    # should print out a message saying why it was left empty
                    continue
                
                if __debug__:
                    if not (set(ATTRIBUTES_IN_OUTPUT) == set(song_info.keys())):
                        print(
                                '''
                                Note the scrape method returned a dictionary with 
                                different outputs than the ATTRIBUTES_IN_OUTPUT 
                                variable. The ATTRIBUTES IN OUTPUT was \n{}\n
                                while the scrape method returned a dictionary with keys\n{}
                                '''.format(ATTRIBUTES_IN_OUTPUT, set(song_info.keys()))
                               ) 
                
                my_writer.writerow(song_info)

                print("Wrote",song_info['Song Version Name'],"to output file.")
                
                if (n_pages_visited >= MAX_N_PAGES):
                    break

        if (n_pages_visited >=  MAX_N_PAGES):
                break
            
def scrape(url: str) -> dict:
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'lxml')
    chord_elements = html_soup.find_all('span', class_='gt-chord')
    title_element = html_soup.find('h1', class_='gt-hero__title')

    output_list = []

    if not chord_elements:
        if __debug__:
            print("Scraping website {} did not find any chords.".format(url))
        return None            

    chords = []
    for chord_element in chord_elements:
        chords.append(chord_element.text)

    # If the first chord is not the same as the last chord, we aren't
    # confident enough about guessing the key to add this song to the database
    if (chords[0] != chords[-1]):
        if __debug__:
            print("No confident guess for key of song at {}".format(url))
        return None
    else: 
        song_key = chords[0]

    output_list.append(("Song Key", song_key))
    output_list.append(("Key Is Guessed", True))

    song_name, artist_name = parse_title_element(title_element)

    output_list.append(("Song Version Name", song_name))
    output_list.append(("Artist Name", artist_name))

    chords = set(chords)
    chords = ",".join(chords)
    chords = ("Chords", chords)
    output_list.append(chords)

    return dict(output_list)

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
