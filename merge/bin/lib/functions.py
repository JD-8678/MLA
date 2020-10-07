import os
from sentence_transformers import SentenceTransformer
from google_drive_downloader import GoogleDriveDownloader as gdd
import os
import os.path
from elasticsearch import Elasticsearch,helpers
from .logger import logger

import argparse
import json
import os
import hashlib
from nltk import tokenize
from nltk import download as nltk_download
import numpy as np
import pandas as pd
import trafilatura
from elasticsearch import Elasticsearch
from newsplease import NewsPlease
from scipy import spatial
from tqdm import tqdm
import requests
from newspaper import Article
from newsfetch.news import newspaper

def create_connection(conn_string):
    logger.debug("Starting ElasticSearch client")
    try:
        es = Elasticsearch([conn_string], sniff_on_start=True, timeout=60)
    except:
        raise ConnectionError(f"Couldn't connect to Elastic Search instance at: {conn_string} \
                                Check if you've started it or if it listens on the port listed above.")
    logger.debug("Elasticsearch connected")
    return es

def check_model(download=True):
    folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','distilbert_model')
    zip_file = path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data','distilbert_model.zip')
    if os.path.isdir(folder) == True:
        logger.debug("Distilbert model present.")
        bool_model = True
    else:
        logger.debug("Distilbert model not present.")
        bool_model = False
        if download==True:
            try:
                gdd.download_file_from_google_drive(file_id='1X3AxYyjyw-M36ZVlFqkE_ki7cEuADu-B',
                                                    dest_path=zip_file,
                                                    unzip=True)
                os.remove(zip_file)
                bool_model = True
            except:
                pass
    return bool_model

try:    
    model = SentenceTransformer(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','distilbert_model'))
except:
    pass

def embedd(sentence):
    sentence_embeddings = model.encode(sentence)
    return sentence_embeddings

def check_index(client, index):
    if client.indices.exists(index):
        return True
    else:
        return False

def status(elastic="127.0.0.1:9200", index="vclaims"):
    bool_client = False
    try:
        es = create_connection(elastic)
        bool_client = True
    except:
        bool_client = False

    if bool_client:
        bool_index = check_index(client=es, index=index)
        if bool_index:
            bool_index = True
        else:
            bool_index = False
    else:
        bool_index = False
    
    dict = {}
    dict["client"] = bool_client
    dict["index"] = bool_index
    dict["model"] = check_model(download=False)
    return dict
###
def cosine(A, B):
    return 2 - spatial.distance.cosine(A, B)

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
        response = CLIENT.search(index=INDEX_NAME, body=query, size=150)
    except:
        logger.error(f"Error in elastic scoring for {sentence}")
        raise

    results = response['hits']['hits']
    size = len(results)

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
        cosine_score = cosine(query_embedded, vector)
        new_score = p * (cosine_score - min_vector) / (max_vector - min_vector) + \
                    (1 - p) * (result['_score'] - min_score) / (max_score - min_score)
        result['cosine'] = round(cosine_score, 12)
        result['combined_score'] = round(new_score, 12)

    df = pd.DataFrame(results)
    df.sort_values(by=['combined_score'], inplace=True, ascending=False)
    df['id'] = np.arange(1, size+1, 1)
    df = df.set_index('id')
    return df

def get_scores(CLIENT, INDEX_NAME, sentences):
    count_sentences = len(sentences)
    scores = []

    logger.info(f"Getting elastic scores for {count_sentences} sentences.")
    for sentence in tqdm(sentences, total=count_sentences):
        score = get_score(CLIENT, INDEX_NAME, sentence)
        scores.append(score[:5])
    

    return scores

def format_scores(sentences, scores_sentences):
    formatted_scores = []
    for i in range(len(sentences)):
        dict = {}
        dict['sentence'] = sentences[i]
        formatted_df = pd.DataFrame(scores_sentences[i])
        dict['retrieved'] = formatted_df[['_id', 'combined_score', '_score', 'cosine', 'vclaim', 'link']].to_dict(
            orient='index')
        formatted_scores.append(dict)
    return formatted_scores

def save_result(fulltext, INDEX_NAME, INPUT, format_scores_sentences, OUTPUT_PATH, MODE):
    dict = {}
    dict['mode'] = MODE
    dict['input'] = INPUT
    dict['index_name'] = INDEX_NAME
    dict['fulltext'] = fulltext
    reverse = {}
    for x in format_scores_sentences:
        for y in range(5):
            if not x['retrieved'][y+1]['vclaim'] in reverse:
                reverse[x['retrieved'][y+1]['vclaim']] = [1, x['retrieved'][y+1]['combined_score'],x['retrieved'][y+1]['combined_score'],x['sentence'],x['retrieved'][y+1]['link']]
            else:
                i = reverse[x['retrieved'][y+1]['vclaim']][0] + 1
                score = reverse[x['retrieved'][y+1]['vclaim']][1] + x['retrieved'][y+1]['combined_score']
                if reverse[x['retrieved'][y+1]['vclaim']][2] < x['retrieved'][y+1]['combined_score']:
                    highest = x['retrieved'][y+1]['combined_score']
                    sentence = x['sentence']
                    link = x['retrieved'][y+1]['link']
                else:
                    highest = reverse[x['retrieved'][y+1]['vclaim']][2]
                    sentence =  reverse[x['retrieved'][y+1]['vclaim']][3]
                    link = reverse[x['retrieved'][y+1]['vclaim']][4]
                reverse[x['retrieved'][y+1]['vclaim']] = [i, score, highest, sentence, link]
        
    overall_vclaims = sorted(reverse.items(), key= lambda item: item[1], reverse=True)[:5]

    overall_dict = {}
    for i in range(5):
        temp = {}
        temp['sentence'] = overall_vclaims[i][1][3]
        temp['vclaim'] = overall_vclaims[i][0]
        temp['combined_score'] = overall_vclaims[i][1][2]
        temp['sum_combined_score'] =  overall_vclaims[i][1][1]
        temp['link'] =  overall_vclaims[i][1][4]
        overall_dict[i+1] = temp

    dict['overall'] = overall_dict
    dict['split'] = format_scores_sentences

    file = OUTPUT_PATH + '\\' + hashlib.md5(INPUT.encode()).hexdigest() + '.json'
    
    logger.debug(f'output_path: {file}')

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    
    open(file, 'w').close()
    with open(file, 'a', encoding='utf-8') as file_output:
        json.dump(dict, file_output, ensure_ascii=False, indent=4)
    file_output.close()
    return json.dumps(dict)
