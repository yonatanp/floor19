#!flask/bin/python
# coding: utf-8
#!/usr/bin/env python

from flask import Flask
from TalkBacker import TalkBacker
import requests
from lxml import html
from flask_cors import CORS, cross_origin
import flask

app = Flask(__name__)
cors = CORS(app, resources={r"/talkbacks/*": {"origins": "*"}})

THRESHOLD = 0.1
DEFAULT_RESPONSE = "חחחחח..."

@app.route('/talkbacks/<article_id>', methods = ['GET'])
def get_talkbacks(article_id):
    url = "http://www.ynet.co.il/articles/%s" % str(article_id)
    header_text, article_text = _getTextFromUrl(url)
    best_talkback, best_talkback_score = TalkBacker(article_text, header_text).suggest()
    if best_talkback_score >= THRESHOLD:
        res = {'talkback': best_talkback}
    else:
        res = {'talkback': DEFAULT_RESPONSE}
    return flask.jsonify(res)

def _getTextFromUrl(url):
    page = requests.get(url)
    root = html.fromstring(page.text)
    tree = root.getroottree()
    result = root.xpath("//article")[0].xpath(".//p/text()")
    article_text = []
    for p_text in result:
        p_text = p_text.strip()
        if p_text:
            article_text.append(p_text)

    article_text = "\n".join(article_text)
    header_title = root.xpath("//div[contains(@class,'art_header_title')]")
    header_title = header_title[0].text

    return header_title, article_text

if __name__ == '__main__':
    app.run(debug=True)
