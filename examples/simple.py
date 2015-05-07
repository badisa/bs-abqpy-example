import urllib
from bs4 import BeautifulSoup

completed_poems = []


def scrape_poems(number):
    global completed_poems
    base_url = 'http://hellopoetry.com'
    page = urllib.urlopen(base_url).read()
    soup = BeautifulSoup(page)
    poems = soup.find_all('div', class_='poem')
    for x in xrange(number):
        poem_page = poems[x].get('data-url')
        poem_page = urllib.urlopen(poem_page).read()
        poetry_soup = BeautifulSoup(poem_page)
        poem = poetry_soup.find('div', class_='poem')
        for br in poem.find_all('br'):
            br.append('\n')
            br.unwrap()
        title = poem.get('data-text')
        body = poem.p.get_text()
        completed_poems.append([title, body])


scrape_poems(7)
print completed_poems, len(completed_poems)
