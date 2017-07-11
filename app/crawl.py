import urllib2
import BeautifulSoup
from collections import deque
from sets import Set
from app import db, models
import re
from urlparse import urlparse
from InvertedIndex import InvertedIndex

# A Crawler class that explores a set of web pages, and adds
# them to some storage (currently not implemented). This class
# is intened to be used in singletone-style, so don't instantiate
# it and only use it via static references (e.g. Crawler.status()).
class Crawler:

    # Set of the web pages we have visited
    processed_pages = Set()
    # Web pages that we are about to look at
    queue = deque([])
    crawling_in_progress = False
    current_page = ""

    @staticmethod
    def crawl(web_page, limit):
        if Crawler.crawling_in_progress:
            return
        Crawler.crawling_in_progress = True

        # Reset crawling data
        Crawler.processed_pages = Set()
        Crawler.queue = deque([])

        Crawler.queue.append(web_page)
        while len(Crawler.queue) > 0 and len(Crawler.processed_pages) < limit:
            next_url = Crawler.queue.popleft()
            print 'Debug: Processing ' + str(next_url)
            if next_url in Crawler.processed_pages:
                continue
            Crawler.current_page = next_url
            page = urllib2.urlopen(next_url)
            data = page.read()
            soup = BeautifulSoup.BeautifulSoup(data)
            Crawler.process(next_url, soup)
            for link in Crawler.extract_links(soup, next_url):
                # We also have to add some ranking there to process those pages smartly
                Crawler.queue.append(link)
            Crawler.processed_pages.add(next_url)

        print 'Debug: Finished crawling'
        Crawler.crawling_in_progress = False

    # Returns current crawling status - we'll use this for nice crawling UI
    @staticmethod
    def status():
        return {
            'processed': Crawler.processed_pages,
            'queue': Crawler.queue,
            'current': Crawler.current_page
        }

    # This method will be responsible for extracting and storing information
    # from html
    # soup is the page represenation by Beautiful soup
    @staticmethod
    def process(url, soup):

        # Helper function from http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element)):
                return False
            return True

        visible_texts = filter(visible, soup.findAll(text=True))
        text = ' '.join(visible_texts)
        e = models.Entity(
            # Hack to retrieve proper name from wikipedia pages
            name = soup.title.string.split(" - Wikipedia")[0],
            url = url,
            image_url = None,
            text = text,
            classification = None)

        # Write objects to the database. Commiting each object by itself
        # is inefficient, but who cares
        db.session.add(e)
        db.session.commit()

        # process inverted index ?
        InvertedIndex.build_inverted_index(text, url)

    # Return the list of links in the given html document
    # soup is the page represenation by Beautiful soup
    @staticmethod
    def extract_links(soup, url):
        result = []
        parsed_url = urlparse(url)
        for link in soup.findAll("a"):
            address = link.get("href")
            if address == None:
                continue
            # For relative links we have to prepend domain to them
            if address[:4] != "http":
                address = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url) + address
            result.append(address)
        return result
