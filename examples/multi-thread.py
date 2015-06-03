import threading
import Queue
import urllib
from bs4 import BeautifulSoup

thread_list = []


class GetTopPoems(threading.Thread):
    '''
    Threaded Variant of Poem Web Scraping
    '''
    def __init__(self, queue, num):
        '''Initialize the Thread'''
        threading.Thread.__init__(self)
        self.num = num
        self.queue = queue

    def run(self):
        base_url = 'http://hellopoetry.com'
        page = urllib.urlopen(base_url).read()
        soup = BeautifulSoup(page)
        poems = soup.find_all('div', class_='poem')
        for poem in poems:
            poem_page = poem.get('data-url')
            self.queue.put(poem_page)


class GetPoem(threading.Thread):
    def __init__(self, queue, complete):
        threading.Thread.__init__(self)
        self.queue = queue
        self.complete = complete

    def run(self):
        while True:
            try:
                poem_url = self.queue.get(False)
                poem_page = urllib.urlopen(poem_url).read()
                # SoupStrainer
                poetry_soup = BeautifulSoup(poem_page).find('div', class_='poem')
                title = poetry_soup.get('data-text')
                poem = poetry_soup.p.get_text(strip=True)
                body = poem
                self.complete.acquire()
                self.complete.poems.append([title, body])
                self.complete.release()
                self.queue.task_done()
            except Queue.Empty:
                break


def main(num):
    queue = Queue.Queue()
    complete_sem = threading.Semaphore()
    complete_sem.poems = []
    parent_thread = GetTopPoems(queue, num)
    parent_thread.start()
    parent_thread.join()
    for x in xrange(num):
        thread = GetPoem(queue, complete_sem)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()
    print complete_sem.poems, len(complete_sem.poems)


main(7)
