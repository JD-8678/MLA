from elasticsearch import Elasticsearch
import logging,json 

class ElasticsearchStorage():
  log = None
  cfg = None
  es = None
  index_current = None
  index_archive = None
  mapping = None
  running = False
  database = None

  def __init__(self,config):
    self.database = config         
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
      #print(self.running)  
      if self.running:
            try:
                version = 1
                ancestor = None
                print("secend")
                # search for previous version
                request = self.es.search(index=self.index_current, body={'query': {'match': {'url.keyword': article.url}}})
                if request['hits']['total']['value'] > 0:
                    # save old version into index_archive
                    old_version = request['hits']['hits'][0]
                    old_version['_source']['descendent'] = True
                    self.es.index(index=self.index_archive, doc_type='_doc', body=old_version['_source'])
                    version += 1
                    ancestor = old_version['_id']
                    self.es.indices.refresh(self.es,index=self.index_archive)
                    

                # save new version into old id of index_current
                self.log.info("Saving to Elasticsearch: %s" % article.url)
                extracted_info = article.get_dict()
                extracted_info['ancestor'] = ancestor
                extracted_info['version'] = version
                self.es.index(index=self.index_current, doc_type='_doc', id=ancestor,
                              body=extracted_info)
                res = self.es.indices.refresh(self.es,index=self.index_current)
                print(res)
             

            except ConnectionError as error:
                self.running = False
                self.log.error("Lost connection to Elasticsearch, this module will be deactivated: %s" % error)

  def get_Article_From_ES(self, url):
    if self.running:
      try:
        request = self.es.search(index=self.index_current, body={'query': {'match': {'url.keyword': url}}})
        print(request)
      except ConnectionError as error:
        self.running = False
        self.log.error("Lost connection to Elasticsearch, this module will be deactivated: %s" % error)

  def search_Article_From_ES(self, arg):
    #arg = [ { 'category': ,
    #          'keyword' : } , ..]
    

    data = '{ "query": { "match": {'
    for item in arg:
      data += '"' + item['category'] + '": "' + item['keyword'] + '"'
    data += '}}}'

    data = json.loads(data)

    print(data)
    if self.running:
      try:
        request = self.es.search(index=self.index_current, body=json.dumps(data))
        print(request)
      except ConnectionError as error:
        self.running = False
        self.log.error("Lost connection to Elasticsearch, this module will be deactivated: %s" % error)
 