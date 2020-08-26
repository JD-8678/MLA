import os
import json
import numpy as np
import pandas as pd
import argparse
from tqdm import tqdm
from elasticsearch import Elasticsearch
from newsplease import NewsPlease

from lib.logger import logger

PREDICT_FILE_COLUMNS = ['qid', 'Q0', 'docno', 'rank', 'score', 'tag']
INDEX_NAME = 'vclaim'

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

def clear_index(es):
    cleared = True
    try:
        es.indices.delete(index=INDEX_NAME)
    except:
        cleared = False
    return cleared

def build_index(es, vclaims, fieldnames):
    vclaims_count = vclaims.shape[0]
    clear_index(es)
    logger.info(f"Builing index of {vclaims_count} vclaims with fieldnames: {fieldnames}")
    for i, vclaim in tqdm(vclaims.iterrows(), total=vclaims_count):
        if not es.exists(index=INDEX_NAME, id=i):
            body = vclaim.loc[fieldnames].replace(np.nan, "").to_dict()
            #print(body)
            es.create(index=INDEX_NAME, id=i, body=body)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vclaims", "-v", required=True,
                        help="TSV file with vclaims. Format: vclaim_id vclaim title")
    parser.add_argument("--predict-file", "-p", required=True,
                        help="File in TREC Run format containing the model predictions")
    parser.add_argument("--keys", "-k",nargs='+', default=['vclaim', 'title', 'named_entities_claim', 'named_entities_article'],
                        help="Keys to search in the document")
    parser.add_argument("--size", "-s", default=10000,
                        help="Maximum results extracted for a query")
    parser.add_argument("--conn", "-c", default="127.0.0.1:9200",
                        help="HTTP/S URI to a instance of ElasticSearch")
    return parser.parse_args()

def main(args):
    #article = NewsPlease.from_url(args.url)
    #PREDICT_NEWS_COLUMNS = ['tweet_content','link']
    #news = pd.DataFrame([(article.maintext.replace('\t','\b'),article.url)], columns=PREDICT_NEWS_COLUMNS)

    vclaims = pd.read_csv(args.vclaims, sep='\t', index_col=0)
    #tweets = pd.read_csv(args.tweets, sep='\t', index_col=0)

    es = create_connection(args.conn)
    build_index(es, vclaims, fieldnames=args.keys)
    #scores = get_scores(es, news, search_keys=args.keys, size=args.size)
    #clear_index(es)

    #formatted_scores = format_scores(scores)
    #formatted_scores.to_csv(args.predict_file, sep='\t', index=False, header=False)
    #logger.info(f"Saved scores from the model in file: {args.predict_file}")

if __name__=='__main__':
    args = parse_args()
    #print(args)
    main(args)
