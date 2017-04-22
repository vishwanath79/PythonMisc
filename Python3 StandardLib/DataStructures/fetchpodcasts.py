from queue import Queue
import threading
import time
import urllib
from urllib.parse import urlparse

import feedparser

# set up some global variables
num_fetch_threads = 2
enclosure_queue = Queue()

feed_urls = [ 'http://talkpython.fm/episodes/rss']

def message(s):
    print('{}:{}'.format(threading.current_thread().name,s))


# download enclosures will run the worker thread and processs the downloads using urllib
def download_enclosures(q):
    """ This is a worker thread function. It processes items in the queue one after another. These daemon threads go into an infinite loop and only exit when the main thread ends"""

    while True:
        message('looking for the next enclosure')
        url = q.get()
        filename = url.rpartition('/')[-1]
        message('downloading {}'.format(filename))
        response = urllib.request.urlopen(url)
        data = response.read()
        # Save the downloaded file to the current directory
        message('Writing to {}'.format(filename))
        with open(filename, 'wb') as outfile:
            outfile.write(data)
        q.task_done()


# Oncetarget function for the threads is defined, the worker threads can be restarted. When download_enclosures processes the statement url = q.get(0, it blocks and waits until the queue has something to return.
# Means its safe to start the threads before there is anything in the queue

# set up some threads to fetch the enclosures

for i in range(num_fetch_threads):
    worker = threading.Thread(
        target=download_enclosures,
        args = (enclosure_queue,),
        name='worker-{}'.format(i),
    )
    worker.setDaemon(True)
    worker.start()

# Download the feed(s) abd out the enclosure URLs into the queue

for url in feed_urls:
    response = feedparser.parse(url,agent='fetch_podcasts.py')
    for entry in response['entries'][:5]:
        for enclosure in entry.get('enclosures',[]):
            parsed_url = urlparse(enclosure['url'])
            message('queueing {}'.format(parsed_url.path.rpartition('/')[-1]))
            enclosure_queue.put(enclosure['url'])

