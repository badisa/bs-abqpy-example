import threading
import urllib
import time
from bs4 import BeautifulSoup
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    'number',
    type=int,
    help='Number of Poems to Scrape')
parser.add_argument(
    'count',
    type=int,
    help='Number of Loops in Each Thread',
    default=0)
args = parser.parse_args()

poemSem = threading.Semaphore()
poemSem.poems = []


class GetTopPoem(threading.Thread):
    '''
    Threaded Variant of Poem Web Scraping
    '''
    def __init__(self, start, incr, count):
        '''Initialize the Thread'''
        threading.Thread.__init__(self)
        self.INITIAL = start
        self.INCREMENT = incr
        self.COUNT = count

    def run(self):
        global poemSem
        base_url = 'http://hellopoetry.com'
        page = urllib.urlopen(base_url).read()
        soup = BeautifulSoup(page)
        poems = soup.find_all('div', class_='poem')
        for x in xrange(self.INITIAL, (self.INCREMENT * self.COUNT), self.INCREMENT):
            poem_page = poems[x].get('data-url')
            poem_page = urllib.urlopen(poem_page).read()
            poetry_soup = BeautifulSoup(poem_page)
            poem = poetry_soup.find('div', class_='poem')
            for br in poem.find_all('br'):
                br.append('\n')
                br.unwrap()
            title = poem.get('data-text')
            body = poem.p.extract().prettify()
            poemSem.poems.append([title, body])


def main(num, count):
    num = num / count
    thread_list = []
    for i in xrange(num):
        thread = GetTopPoem(i, num, count)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    print poemSem.poems, len(poemSem.poems)


main(args.number, args.count)
