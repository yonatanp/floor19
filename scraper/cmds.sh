workon ipython

function TEST {
  scrapy crawl $1 -a max_articles=20 -a include_talkbacks=true && echo $1 && wc -l articles.json talkbacks.json;
}

function GEN500 {
  scrapy crawl $1 --loglevel=WARN -a max_articles=500 -a include_talkbacks=true && echo $1 && wc -l articles.json talkbacks.json && \
    cp articles.json ../data/ynet_$1_500_articles.json && \
    cp talkbacks.json ../data/ynet_$1_500_talkbacks.json;
}

# all except sports which doesn't work
for i in national politics dating health education parents digital cars economy; do
  GEN500 $i
done
