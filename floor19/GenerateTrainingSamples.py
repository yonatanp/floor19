import json
from TextProcessing import TextProcessing

UNKNOWN = 'unknown'
LEGAL_PUNCT = ['!','.',':']
ILLEGAL_PUNCT = ["'", '"', "=", ';', ',', '-', ')', '(']

data = []
files = [
    '../data/ynet_cars_500_talkbacks.json',
    '../data/ynet_dating_500_talkbacks.json',
    '../data/ynet_digital_500_talkbacks.json',
    '../data/ynet_economy_500_talkbacks.json',
    '../data/ynet_education_500_talkbacks.json',
    '../data/ynet_health_500_talkbacks.json',
    '../data/ynet_national_500_talkbacks.json',
    '../data/ynet_parents_500_talkbacks.json',
    '../data/ynet_politics_500_talkbacks.json',
]

for file in files:
    for line in open(file, 'rb'):
        line_dict = json.loads(line)
        processed_list = TextProcessing(line_dict['title_text']).cleanTextHebrew(exclude_punct=False)
        data.append(processed_list)

word2idf = json.loads(open('../data/ynet_national_500_articles_idf_vals.txt', 'rb').read())
vocabulary = word2idf.keys() #len=31113

file = open('talkbacks_training_set.txt', 'wb')
for d_list in data:
    for d in d_list:
        if d not in ILLEGAL_PUNCT:
            if d not in LEGAL_PUNCT and d not in vocabulary:
                file.write(UNKNOWN)
            else:
                file.write(d.encode('utf8'))
            file.write(' ')
    file.write('\n')