from app import app
from app import db, models
from crawl import Crawler
from flask import render_template, request, jsonify
import threading
from InvertedIndex import InvertedIndex


# Handler for exploring existing content
@app.route('/')
@app.route('/explore')
def explore():
    return render_template('explore.html')


# Handler for crawling new content
@app.route('/crawl')
def crawl():
    thread = threading.Thread(
        target=Crawler.crawl,
        args=('https://en.wikipedia.org/wiki/Premier_League', 10))
    thread.start()
    return render_template('layout.html', body="OK")


@app.route('/get_current_crawling_status')
def get_current_crawling_status():
    status = Crawler.status()
    return render_template(
        'status.html',
        processed=status['processed'],
        queue=status['queue'],
        current=status['current'])


@app.route('/crawled_data')
def get_crawled_data():
    return render_template('crawled_data.html',
                           entities=models.Entity.query.all())


@app.route('/results')
def get_results():
    query = request.args.get('query')
    urls = InvertedIndex.get_rank(query)
    #urls = (('google.com', 3), ('facebook.com', 1))
    res = []
    for (url, rank) in urls:
        res.append({'url': url, 'rank': rank})

    return jsonify({'results': res, 'time_ms': 30})
