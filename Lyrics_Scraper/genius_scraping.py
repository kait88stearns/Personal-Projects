import requests
from bs4 import BeautifulSoup
import re

def scrape_songs(artist, songs):
    '''
    Input:
        artist = string: as 'First-last' if name is more than one word
        album = list of strings: all lowercase, words separated by -
    Output:
        corpus = list of strings: each string is the refined text of one song
    '''
    corpus = []
    for song in songs:
        response = requests.get('https://genius.com/{}-{}-lyrics'.format(artist,song))
        soup = BeautifulSoup(response.text, "html.parser")
        lyrics=''
        for item in soup.find_all('a', {'href': re.compile('/{}-{}-lyrics'.format(artist,song))}):
            section = re.sub('\n',' ', item.text)
            section = re.sub('\[.+?\]',' ',section)
            lyrics+= section + ' '
        corpus.append(lyrics)
    return corpus
