import argparse
import json

from create_index import create_connection


def es_search(INDEX_NAME, CLIENT, SIZE, query_keywords, query_sentence):
    client = CLIENT

    keywords = ''
    for i in range(len(query_keywords) - 1):
        keywords = keywords + query_keywords[i] + ' OR '
    keywords = keywords + query_keywords[len(query_keywords) - 1]

    query = {
        "size": SIZE,
        "query": {
            "script_score": {
                "query": {
                    'query_string': {
                        'query': keywords,
                        'fields': ['vclaim', 'named_entities_claim', 'keywords']
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                    "params": {"query_vector": query_sentence}
                }
            }
        }
    }

    res = client.search(index=INDEX_NAME, body=query)
    with open('data/request.json', "w") as json_file:
        json.dump(res, json_file, indent=4)

    hit = res['hits']['hits']
    result = []
    for i in range(5):
        entry = []
        entry.append(hit[i]["_id"])
        entry.append(hit[i]["_score"])
        entry.append(hit[i]['_source']['vclaim'])
        result.append(entry)

    return result


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--elastic", "-e", default="127.0.0.1:9200",
#                         help="HTTP/S URL to ElasticSearch instance")
#     parser.add_argument("--size", "-s", default="10000",
#                         help="Max. size to consider. Default : 10000; Max : 10000")
#     return parser.parse_args()


# def main(args):
#     INDEX_NAME = "verified_claims"
#     SIZE = args.size
#     CLIENT = create_connection(args.elastic)
#
#
# if __name__ == "__main__":
#     args = parse_args()
#     # execute only if run as a script
#     main(args)
