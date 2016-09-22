#!flask/bin/python
# coding: utf-8
#!/usr/bin/env python

from flask import Flask
from TalkBacker import TalkBacker
import requests
from lxml import html

app = Flask(__name__)

THRESHOLD = 0.1
DEFAULT_RESPONSE = "חחחחח..."

@app.route('/talkbacks', methods = ['GET'])
def get_talkbacks(url=None):
    header_text, article_text = _getTextFromUrl(url)
    best_talkback, best_talkback_score = TalkBacker(article_text, header_text).suggest()
    if best_talkback_score >= THRESHOLD:
        return best_talkback
    else:
        return DEFAULT_RESPONSE

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

    header_title = root.xpath("//div[contains(@class,'art_header_title')]")
    header_title[0].text
    return header_title, article_text

if __name__ == '__main__':
    app.run(debug=True)