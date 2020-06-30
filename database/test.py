from newsplease import NewsPlease
import newsplease as test
import sys, getopt

import json

from SPARQLWrapper import SPARQLWrapper
from newsplease.NewsArticle import NewsArticle

#local library
from ES_Database import ElasticsearchStorage

def main(argv):
    url = ""
    ES_config = {
      'host': 'letkemann.ddns.net',
      'port': 9200,
      'index_current': 'news-please',
      'index_archive': 'news-please-archive',
      'use_ca_certificates': False,
      'ca_cert_path': '/path/to/cacert.pem',
      'client_cert_path': '/path/to/client_cert.pem',
      'client_key_path': '/path/to/client_key.pem',
      'username': 'root',
      'secret': 'password',
      'mapping' : {"properties": {
        "url": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "source_domain": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "title_page": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "title_rss": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "localpath": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "filename": {"type": "keyword"},
        "ancestor": {"type": "keyword"},
        "descendant": {"type": "keyword"},
        "version": {"type": "long"},
        "date_download": {"type": "date", "format":"yyyy-MM-dd HH:mm:ss"},
        "date_modify": {"type": "date", "format":"yyyy-MM-dd HH:mm:ss"},
        "date_publish": {"type": "date", "format":"yyyy-MM-dd HH:mm:ss"},
        "title": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "description":  {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "text": {"type": "text"},
        "authors": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "image_url":  {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "language": {"type": "keyword"}
      }}
    }

    try:
      opts, args = getopt.getopt(argv,"u:o",["url=","options="])
    except getopt.GetoptError:
      print("test.py -u url")
      sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--url"):
            url = arg
        #elif opt in ("-o", "--options"):
            #not implement yet

    print(url)

    article = NewsPlease.from_url(url)
    es = ElasticsearchStorage(ES_config)
    es.process_Article(article)
    #es.get_Article_From_ES(url)
    list = []
    list.append({'category': 'language', 'keyword': 'de'})
    es.search_Article_From_ES(list)

if __name__ == "__main__":
    main(sys.argv[1:])

