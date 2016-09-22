#!flask/bin/python
from flask import Flask
from TalkBacker import TalkBacker

app = Flask(__name__)

GIVEN_ARTICLE = 'abc'
THRESHOLD = 0.3

@app.route('/talkbacks', methods = ['GET'])
def get_talkbacks(given_article=GIVEN_ARTICLE):
    best_talkback, best_talkback_score = TalkBacker(given_article).suggest()
    if best_talkback_score >= THRESHOLD:
        return best_talkback

if __name__ == '__main__':
    app.run(debug=True)