import os,hashlib
import json
import numpy as np
import pandas as pd
import argparse
from tqdm import tqdm
from elasticsearch import Elasticsearch
#from newsplease import NewsPlease
import trafilatura
from lib import logger

#config
#PREDICT_FILE_COLUMNS = ['tweet_id', 'vclaim_id','vclaim', 'score', 'ratingName', 'link']
PREDICT_VCLAIMS_COLUMNS = ['_id','vclaim', '_score', 'ratingName', 'link']
PREDICT_NEWS_COLUMNS = ['tweet_content','link']
INDEX_NAME = 'vclaim'
PATH = './tmp/'

RATING_FILTER = ['TRUE', 'FALSE','MIXTURE', 'OTHER']
#RATING_FILTER = ['TRUE', 'FALSE']
MAX_OUTPUT_CLAIMS  = None

#modified by Erwin Letkemann for special uses

def create_connection(conn_string):
    logger.debug("Starting ElasticSearch client")
    try:
        es = Elasticsearch([conn_string], sniff_on_start=True)
    except:
        raise ConnectionError(f"Couldn't connect to Elastic Search instance at: {conn_string} \
                                Check if you've started it or if it listens on the port listed above.")
    logger.debug("Elasticsearch connected")
    return es

def get_score(es, tweet, search_keys, size=10000):
    query = {"query": {"multi_match": {"query": tweet, "fields": search_keys}}}
    try:
        response = es.search(index=INDEX_NAME, body=query, size=size)
    except:
        logger.error(f"No elasticsearch results for {tweet}")
        raise

    try:
        results = response['hits']['hits']
        for result in results:
            info = result.pop('_source')
            result.update(info)
        df = pd.DataFrame(results)
        df['_id'] = df._id.astype('int32').values
        df = df[PREDICT_VCLAIMS_COLUMNS]
        return df
    except:
        logger.info(f"NO results for Text: {tweet}")
        return pd.DataFrame()
    #df = df.set_index('id')
    #return df._score

def get_scores(es, tweets, search_keys, size):
    vclaims_count = es.cat.count(INDEX_NAME, params={"format": "json"})[0]['count']
    tweets_count  = len(tweets)
    scores = {}
    temp = pd.DataFrame()
    count = None
    count_tweet = 0

    logger.info(f"Geting RM5 scores for {tweets_count} tweets and {vclaims_count} vclaims")
    for i, tweet in tqdm(tweets.iterrows(), total=tweets_count):
        score = get_score(es, tweet.tweet_content, search_keys=search_keys, size=size)
        scores = {}
        if score.empty:
            pass
        else:
            #print(str(count)+ " | "+str(tweet.link))
            #print(score)
            if tweet.link == count:
                #print("if")
                try:
                    calc = (score[['_id','_score']].set_index('_id').join(temp[['_id','_score']].set_index('_id'),how='outer', lsuffix='left' , rsuffix='right')).fillna(0)
                    calc = calc.assign(_score=lambda x: x._scoreleft + x._scoreright).drop(['_scoreleft','_scoreright'], axis=1)
                    
                    dummy = score.append(temp, ignore_index = True)
                    dummy = dummy.drop_duplicates('_id').drop('_score',axis=1)

                    #print("calc: " + str(calc))
                    #print("dummy: " + str(dummy))

                    temp = dummy.join(calc, on='_id')
                    #print(temp)
                except:
                    logger.error(r"Error at Score Merge")
            else:
                #print("else" + str(i))
                if temp.empty:
                    pass
                else:
                    scores[count_tweet] = temp
                    count_tweet += 1
                temp = score
                count = tweet.link
    
    scores[count_tweet] = temp
    #print(scores)
    return scores

def format_scores(scores):
    formatted_scores = pd.DataFrame()
    for tweet_id, s in scores.items():   
        s = s.assign(tweet_id=tweet_id).sort_values('_score',ascending=False)
        try:
            formatted_scores = formatted_scores.append(s,ignore_index=True)
        except ValueError:
            formatted_scores = s

    formatted_scores = formatted_scores[formatted_scores['ratingName'].isin(RATING_FILTER)]
    return formatted_scores[:MAX_OUTPUT_CLAIMS]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--predict-file", "-p", default="result.csv",
                        help="File in TREC Run format containing the model predictions")
    parser.add_argument("--keys", "-k",nargs='+', default=['vclaim', 'title', 'named_entities_claim', 'named_entities_article','keywords'],
                        help="Keys to search in the document")
    parser.add_argument("--size", "-s", default=10000,
                        help="Maximum results extracted for a query")
    parser.add_argument("--output_size", "-x", default=10000,
                        help="Maximum results extracted for news")
    parser.add_argument("--conn", "-c", default="127.0.0.1:9200",
                        help="HTTP/S URI to a instance of ElasticSearch")
    parser.add_argument("--mode", "-m", default="url", choices=["url","string"], type=str.lower,
                        help="choice between url or string mode")
    parser.add_argument("--input", "-i", nargs='+', required=True,
                        help="input should be a String or url")
    return parser.parse_args()

def save_result(scores,news,news_articles,args):
    count = 0
    if args.mode == "url":
        for elem in news_articles:
            dir = PATH + hashlib.md5(elem.url.encode()).hexdigest() + '/'

            if not os.path.exists(dir):
                os.makedirs(dir)

            filter = scores[(scores.tweet_id == count)]
            count += 1
            filter.to_csv(path_or_buf=(dir + str(args.predict_file)), sep=',', index=False, header=False)

            data = elem.get_serializable_dict()
            with open(dir + 'news_article.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved scores from the model in file: {dir}{args.predict_file}")

    elif args.mode == "string":
        for elem in news:
            dir = PATH + 'String/' + str(elem[1]) + '/'

            if not os.path.exists(dir):
                os.makedirs(dir)

            filter = scores[(scores.tweet_id == count)]
            count += 1
            filter.to_csv(path_or_buf=(dir + str(args.predict_file)), sep=',', index=False, header=False)

            with open(dir + 'string.txt', 'w', encoding='utf-8') as f:
                f.write(str(elem[0]))
                f.close()
            logger.info(f"Saved scores from the model in file: {dir}{args.predict_file}")
    else:
        logger.error(r"mode not found")

def main(args):
    news = []
    news_articles = []
    news_string   = []
    class articleClass:
        def __init__(self,maintext,url):
            self.maintext = maintext
            self.url = url 
        def get_serializable_dict(self):
            return {
                'maintext': self.maintext,
                'url': self.url
            }

    if args.mode == "url":
        for i in tqdm(range(len(args.input)), desc="loading article: "):
            #article = NewsPlease.from_url(args.input[i])
            website = trafilatura.fetch_url(args.input[i])
            maintext = trafilatura.extract(website)
            article = articleClass(maintext,args.input[i])
            news_articles.append(article)
            for sentence in article.maintext.split('.'):
                news.append([sentence.replace('\t','\b'),article.url]) 
            #news.append([article.maintext.replace('\t','\b'),article.url])
    elif args.mode == "string":
        for i in range(len(args.input)):
            news_string.append([args.input[i],i])
            for sentence in args.input[i].split('.'):
                news.append([sentence.replace('\t','\b'),i]) 

    news = pd.DataFrame(news,columns=PREDICT_NEWS_COLUMNS)
    #print(news)

    es = create_connection(args.conn)

    scores = get_scores(es, news, search_keys=args.keys, size=args.size)
    #print(scores)
    formatted_scores = format_scores(scores)
    #print(formatted_scores)
    save_result(formatted_scores, news_string, news_articles,args)
    #print(formatted_scores)
    if args.mode == "url":
        return (formatted_scores,news_articles)
    else:
        return (formatted_scores,news_string) 

if __name__=='__main__':
    args = parse_args()
    MAX_OUTPUT_CLAIMS = args.output_size
    #print(args)
    main(args)
