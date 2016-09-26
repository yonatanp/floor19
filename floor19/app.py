#!flask/bin/python
# coding: utf-8
#!/usr/bin/env python

from flask import Flask
from flask import request
from TalkBacker import TalkBacker
import requests
from lxml import html
from flask_cors import CORS, cross_origin
import flask

app = Flask(__name__)
cors = CORS(
    app, resources={
        r"/talkbacks/*": {"origins": "*"},
        r"/talkbacks_fulltext": {"origins": "*"}
    }
)

THRESHOLD = 0.0
DEFAULT_RESPONSE = "חחחחח..."

@app.route('/talkbacks/<article_id>', methods = ['GET'])
def get_talkbacks(article_id):
    url = "http://www.ynet.co.il/articles/%s" % str(article_id)
    header_text, article_text = _getTextFromUrl(url)
    res = _generate_talkbacks(header_text, article_text)
    return flask.jsonify(res)

@app.route('/talkbacks_fulltext', methods = ['POST'])
def get_talkbacks_fulltext():
    res = _generate_talkbacks(request.form['header'], request.form['body'])
    return flask.jsonify(res)

def _generate_talkbacks(header_text, body_text):
    best_talkbacks = TalkBacker(body_text, header_text).suggest()
    # if best_talkback_score >= THRESHOLD:
    #     res = {'talkback': best_talkback}
    # else:
    #     res = {'talkback': DEFAULT_RESPONSE}
    return {
        'talkback': best_talkbacks[0][0],
        'talkback_list': [i[0] for i in best_talkbacks],
    }

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
    app.run(debug=True, host='0.0.0.0')
