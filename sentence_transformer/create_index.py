import argparse
import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm

from functions import embedd


def create_connection(connection):
    print("Starting ElasticSearch client")
    try:
        client = Elasticsearch([connection], sniff_on_start=True, timeout = 60)
    except:
        raise ConnectionError(f"Couldn't connect to Elastic Search instance at: {connection} . "
                              f"Check if you've started it or if it listens on the port listed above.")
    print("Elasticsearch connected")
    return client


def create_index(INDEX_NAME, INDEX_FILE, DATA_FILE, keys, client):
    print("Creating the index.")
    client.indices.delete(index=INDEX_NAME, ignore=[404])

    with open(INDEX_FILE) as index_file:
        source = index_file.read()
        client.indices.create(index=INDEX_NAME, body=source)

    vectors = []

    vclaims = pd.read_csv(DATA_FILE, sep='\t', index_col=0, encoding="utf-8")
    vclaims = vclaims.drop(['claimskg_id', 'truthRating', 'date', 'source', 'sourceURL', 'language'], axis=1)
    vclaims = vclaims.reset_index()

    print(f"Embedding {len(vclaims)} vclaims.")
    for i in tqdm(range(len(vclaims))):
        text = vclaims.loc[i, "vclaim"]
        vector = embedd(text)
        vectors.append(vector)
    vclaims["vector"] = vectors


    docs = []

    for i in range(len(vclaims)):
        line = vclaims.loc[i, keys].replace(np.nan, "").to_dict()
        docs.append(line)
    print('Done')

    actions = [
        {
            '_index': INDEX_NAME,
            '_id': i + 1,
            '_source': docs[i]
        }
        for i in range(0, len(vclaims))
    ]

    print(f"Builing index of {len(vclaims)} vclaims with fieldnames: {keys}")
    print('Please wait...')
    helpers.bulk(client, actions)
    client.indices.refresh(index=INDEX_NAME)
    print("Done indexing.")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--elastic", "-e", default="localhost:9200",
                        help="HTTP/S URL to ElasticSearch instance")
    parser.add_argument("--index_name", "-n", default="verified_claims",
                        help="ElasticSearch index name")
    parser.add_argument("--index_file", "-i", default="data/index.json",
                        help="Path to index file")
    return parser.parse_args()


def main(args):
    INDEX_NAME = args.index_name
    INDEX_FILE =  args.index_file
    DATA_FILE = "data/vclaims.tsv"
    KEYS = ['title',
            'vclaim',
            'ratingName',
            'author',
            'named_entities_article',
            'named_entities_claim',
            'link',
            'keywords',
            'vector']
    CLIENT = create_connection(args.elastic)

    create_index(INDEX_NAME, INDEX_FILE, DATA_FILE, KEYS, CLIENT)


if __name__ == "__main__":
    args = parse_args()
    # execute only if run as a script
    main(args)
