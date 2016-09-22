#!flask/bin/python
# coding: utf-8
#!/usr/bin/env python

from flask import Flask
from TalkBacker import TalkBacker

app = Flask(__name__)

THRESHOLD = 0.1
DEFAULT_RESPONSE = "פחחחחח....."

@app.route('/talkbacks', methods = ['GET'])
def get_talkbacks(given_article=None):
    best_talkback, best_talkback_score = TalkBacker(given_article).suggest()
    if best_talkback_score >= THRESHOLD:
        return best_talkback
    else:
        return DEFAULT_RESPONSE

if __name__ == '__main__':
    app.run(debug=True)