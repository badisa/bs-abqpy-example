import urllib
from bs4 import BeautifulSoup, SoupStrainer


def scrape_poems(number):
    completed_poems = []
    base_url = 'http://hellopoetry.com'
    only_body = SoupStrainer('body')
    page = urllib.urlopen(base_url).read()
    soup = BeautifulSoup(page, "html.parser", parse_only=only_body)
    print soup.prettify()
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
    # print completed_poems, len(completed_poems)


scrape_poems(7)
