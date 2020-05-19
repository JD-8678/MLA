from newsplease import NewsPlease
import sys, getopt
from elasticsearch import Elasticsearch
import logging

from NewsArticle import NewsArticle

def main(argv):
    url = ""

    try:
      opts, args = getopt.getopt(argv,"u:",["url=","options="])
    except getopt.GetoptError:
      print("test.py -u url")
      sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--url"):
            url = arg
        #elif opt in ("-o", "--options"):
        #    #not implement yet
    print(url)

    article = NewsPlease.from_url(url)
    es = ElasticsearchStorage()
    es.process_Article(article)

class ElasticsearchStorage():
  log = None
  cfg = None
  es = None
  index_current = None
  index_archive = None
  mapping = None
  running = False

  def __init__(self):
    self.database = {
      'host': 'localhost',
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

    self.es = Elasticsearch(
       [self.database["host"]],
       http_auth=(str(self.database["username"]), str(self.database["secret"])),
       port=self.database["port"],
       use_ssl=self.database["use_ca_certificates"],
       verify_certs=self.database["use_ca_certificates"],
       ca_certs=self.database["ca_cert_path"],
       client_cert=self.database["client_cert_path"],
       client_key=self.database["client_key_path"]
    )
    self.index_current = self.database["index_current"]
    self.index_archive = self.database["index_archive"]
    self.mapping = self.database["mapping"]

    try:
      # check if server is available
      self.es.ping()

      #raise loggin level due to indices.exists() habit of loggin a warning if an index doesn't exist.
      es_log = logging.getLogger('elasticsearch')
      es_level = es_log.getEffectiveLevel()
      es_log.setLevel('ERROR')

      # check if the necessary indices exist and create them if needed
      if not self.es.indices.exists(self.index_current):
         self.es.indices.create(index=self.index_current)
         self.es.indices.put_mapping(index=self.index_current, body=self.mapping)
      if not self.es.indices.exists(self.index_archive):
         self.es.indices.create(index=self.index_archive)
         self.es.indices.put_mapping(index=self.index_archive, body=self.mapping)
         self.running = True

      # restore previous logging level
      es_log.setLevel(es_level)

    except ConnectionError as error:
      self.running = False
      self.log.error("Failed to connect to Elasticsearch, this module will be deactivated. "
                           "Please check if the database is running and the config is correct: %s" % error)

  def process_Article(self, article):
        if self.running:
            try:
                version = 1
                ancestor = None

                # search for previous version
                request = self.es.search(index=self.index_current, body={'query': {'match': {'url.keyword': article.url}}})
                if request['hits']['total']['value'] > 0:
                    # save old version into index_archive
                    old_version = request['hits']['hits'][0]
                    old_version['_source']['descendent'] = True
                    self.es.index(index=self.index_archive, doc_type='_doc', body=old_version['_source'])
                    version += 1
                    ancestor = old_version['_id']

                # save new version into old id of index_current
                self.log.info("Saving to Elasticsearch: %s" % article.url)
                extracted_info = article.get_dict()
                extracted_info['ancestor'] = ancestor
                extracted_info['version'] = version
                self.es.index(index=self.index_current, doc_type='_doc', id=ancestor,
                              body=extracted_info)


            except ConnectionError as error:
                self.running = False
                self.log.error("Lost connection to Elasticsearch, this module will be deactivated: %s" % error)


if __name__ == "__main__":
    main(sys.argv[1:])

