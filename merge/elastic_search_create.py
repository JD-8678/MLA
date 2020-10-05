import numpy as np
import pandas as pd
import argparse,os
from tqdm import tqdm
from elasticsearch import Elasticsearch,helpers
#from sentence_transformers import SentenceTransformer
#
from bin import lib

# ausgelagert nach /bin/lib/functions !!!
#model = SentenceTransformer(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','distilbert_model'))
# model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')
#def embedd(sentence):
#    sentence_embeddings = model.encode(sentence)
#    return sentence_embeddings


def clear_index(CLIENT, INDEX_NAME):
    cleared = True
    try:
        CLIENT.indices.delete(index=INDEX_NAME)
    except:
        cleared = False
    return cleared

def build_index(CLIENT, VCLAIMS, INDEX_FILE, INDEX_NAME, KEYS):

    vclaims_count = VCLAIMS.shape[0]
    clear_index(CLIENT, INDEX_NAME)
    
    with open(INDEX_FILE) as index_file:
        source = index_file.read()
        CLIENT.indices.create(index=INDEX_NAME, body=source)

    lib.logger.info(f"Embedding vclaims.")
    actions = []
    for i, vclaim in tqdm(VCLAIMS.iterrows(), total=vclaims_count):
        if not CLIENT.exists(index=INDEX_NAME, id=i):
            body = vclaim.loc[KEYS[:-1]].replace(np.nan, "").to_dict()
            body["vector"] = lib.embedd(vclaim['vclaim'])
            actions.append(
                {
                    '_op_type': 'create',
                    '_index': INDEX_NAME,
                    '_id': i + 1,
                    '_source': body
                })
    lib.logger.info(f"Adding {vclaims_count} entries to '{INDEX_NAME}' with fieldnames: {KEYS}")

    for entry in tqdm(helpers.parallel_bulk(client=CLIENT, actions=actions), total=vclaims_count):
        pass

#not tested
# def build_index_Linux(CLIENT, VCLAIMS, INDEX_FILE, INDEX_NAME, KEYS):
#     vclaims_count = VCLAIMS.shape[0]
#     clear_index(CLIENT, INDEX_NAME)
    
#     with open(INDEX_FILE) as index_file:
#         source = index_file.read()
#         CLIENT.indices.create(index=INDEX_NAME, body=source)

#     lib.logger.info(f"Builing index of {vclaims_count} vclaims with fieldnames: {fieldnames}")
#     actions = []
#     for i, vclaim in tqdm(VCLAIMS.iterrows(), total=vclaims_count):
#         if not CLIENT.exists(index=INDEX_NAME, id=i):
#             body = vclaim.loc[fieldnames].replace(np.nan, "").to_dict()
#             body["vector"] = embedd(vclaim["vclaim"])
#             actions.append(
#                 {
#                     '_op_type': 'create',
#                     '_index': INDEX_NAME,
#                     '_id': i + 1,
#                     '_source': body
#                 })
#     lib.logger.info('Wait...')
#     deque(helpers.parallel_bulk(client=CLIENT, actions=actions), maxlen=0)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vclaims", "-v", "-source", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),'bin' ,'data','vclaims.tsv'),
                        help="Path to file containing vclaims (cLaimsKG format).")
    parser.add_argument("--connection", "-c", "-es", "-conn", default="127.0.0.1:9200",
                        help="HTTP/S URL to a instance of ElasticSearch")
    parser.add_argument("--index_name", "-id", "-name", default="vclaims",
                        help="Elasticsearch index name to assign.")
    return parser.parse_args()

def main(args):
    CLIENT = lib.create_connection(args.connection)
    VCLAIMS = pd.read_csv(args.vclaims, sep='\t', index_col=0)
    INDEX_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'bin', 'data','index.json')
    INDEX_NAME = args.index_name
    KEYS = ['title',
            'vclaim',
            'ratingName',
            'author',
            'named_entities_article',
            'named_entities_claim',
            'link',
            'keywords',
            'date',
            'vector']
    build_index(CLIENT, VCLAIMS, INDEX_FILE, INDEX_NAME, KEYS)
    # try:
    #     build_index(CLIENT, VCLAIMS, INDEX_FILE, INDEX_NAME, KEYS)
    # except:
    #     try:
    #         build_index_Linux(CLIENT, VCLAIMS, INDEX_FILE, INDEX_NAME, KEYS)
    #     except:
    #         lib.logger.error(r"Something went wrong will building_index!")
    
    

if __name__=='__main__':
    args = parse_args()
    main(args)
