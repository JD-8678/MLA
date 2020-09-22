import argparse
import json
import os

import numpy as np
import pandas as pd
from elastic_search_create import embedd
from elasticsearch import Elasticsearch
from lib.logger import logger
from scipy import spatial

pd.set_option('display.max_columns', None)


def cosine(A, B):
    return 2 - spatial.distance.cosine(A, B)

def create_connection(conn_string):
    logger.debug("Starting ElasticSearch client")
    try:
        es = Elasticsearch([conn_string], sniff_on_start=True, timeout=60)
    except:
        raise ConnectionError(f"Couldn't connect to Elastic Search instance at: {conn_string} \
                                Check if you've started it or if it listens on the port listed above.")
    logger.debug("Elasticsearch connected")
    return es

def get_score(CLIENT, INDEX_NAME, sentence):
    query_embedded = embedd(sentence).tolist()
    query = {
        "query": {
            "multi_match": {
                "query": sentence
            }
        }
    }
    try:
        response = CLIENT.search(index=INDEX_NAME, body=query, size=10000)
    except:
        logger.error(f"Error in elastic scoring for {sentence}")
        raise

    results = response['hits']['hits']

    try:
        results = results[:150]
    except:
        pass

    max_score = max([x['_score'] for x in results])
    min_score = min([x['_score'] for x in results])
    cosine_vectors = [cosine(x['_source']['vector'], query_embedded) for x in results]
    max_vector = max(cosine_vectors)
    min_vector = min(cosine_vectors)
    p = 0.75
    for result in results:
        info = result.pop('_source')
        vector = info.pop('vector')
        result.update(info)
        p = 0.75

        new_score = p * (cosine(query_embedded, vector) - min_vector) / (max_vector - min_vector) + \
                    (1 - p) * (result['_score'] - min_score) / (max_score - min_score)
        result['combined_score'] = round(new_score, 12)

    df = pd.DataFrame(results)
    df.sort_values(by=['combined_score'], inplace=True, ascending=False)
    df['id'] = np.arange(1, 151, 1)
    df = df.set_index('id')
    return df

def get_scores(CLIENT, INDEX_NAME, sentences):
    count_sentences = len(sentences)
    scores = []
    logger.info(f"Geting elastic scores for {count_sentences}.")
    for sentence in sentences:
        score = get_score(CLIENT, INDEX_NAME, sentence)
        scores.append(score[:5])
    return scores

def format_scores(sentences, scores_sentences):
    formatted_scores = []
    for i in range(len(sentences)):
        dict = {}
        dict['sentence'] = sentences[i]
        formatted_df = pd.DataFrame(scores_sentences[i])
        dict['retrieved'] = formatted_df[['_id', 'combined_score', 'vclaim', 'link']].to_dict(orient='index')
        formatted_scores.append(dict)
    return formatted_scores

def save_result(fulltext, INDEX_NAME, format_scores_sentences, OUTPUT_PATH):
    dict = {}
    dict['mode'] = 'file'
    dict['url'] = 'None'
    dict['index_name'] = INDEX_NAME
    dict['fulltext'] = fulltext
    dict['split'] = format_scores_sentences

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    open(OUTPUT_PATH + '/result.json', 'w').close()t
    with open(OUTPUT_PATH + '/result.json', 'a', encoding='utf-8') as file_output:
        json.dump(dict, file_output, ensure_ascii=False, indent=4)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", "-p", "-output", "-out", "-result", default="./output",
                        help="Path to output file.  default: ./output")
    parser.add_argument("--input", "-i", '-path', required=True,
                        help="URL to a news article")
    parser.add_argument("--connection", "-c", "-es", "-conn", default="127.0.0.1:9200",
                        help="HTTP/S URL to a instance of ElasticSearch")
    parser.add_argument("--index_name", "-id", "-name", default="vclaims",
                        help="Elasticsearch index name to assign.")
    return parser.parse_args()

def main(args):
    CLIENT = create_connection(args.connection)
    OUTPUT_PATH = args.output_path
    INDEX_NAME = args.index_name
    INPUT = args.input

    with open(INPUT, 'r') as file_input:
        fulltext = file_input.read()
    file_input.close()

    sentences = list(fulltext.split("\n"))
    scores_sentences = get_scores(CLIENT, INDEX_NAME, sentences)
    format_scores_sentences = format_scores(sentences, scores_sentences)
    save_result(fulltext, INDEX_NAME, format_scores_sentences, OUTPUT_PATH)

if __name__ == '__main__':
    args = parse_args()
    main(args)
