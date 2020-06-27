import csv
from ES_Database import ElasticsearchStorage

def main():
    ES_config = {
      'host': 'letkemann.ddns.net',
      'port': 9200,
      'index_current': 'claims',
      'index_archive': 'claims-archiv',
      'use_ca_certificates': False,
      'ca_cert_path': '/path/to/cacert.pem',
      'client_cert_path': '/path/to/client_cert.pem',
      'client_key_path': '/path/to/client_key.pem',
      'username': 'root',
      'secret': 'password',
      'mapping' : {"properties": {
        #"source_domain": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        #"date_modify": {"type": "date", "format":"yyyy-MM-dd HH:mm:ss"},
        "rating_ratingValue'": {"type": "double"},
        "rating_worstRating'": {"type": "double"},
        "rating_bestRating'": {"type": "double"},
        "rating_alternateName'": {"type": "boolean","fields":{"keyword":{"type":"keyword"}}},
        "creativeWork_author_name": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "creativeWork_datePublished": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "creativeWork_author_sameAs'": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "claimReview_author_name": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "claimReview_author_url": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        #"url": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "claimReview_url": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "claimReview_claimReviewed": {"type": "text"},
        "claimReview_datePublished": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "claimReview_source": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "claimReview_author": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "extra_body": {"type": "text"},
        "extra_refered_links": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "extra_title": {"type": "text"},
        #
        "extra_tags": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "extra_entities_claimReview_claimReviewed": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "extra_entities_body": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "extra_entities_keywords": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "extra_entities_author": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        #
        "localpath": {"type": "text","fields":{"keyword":{"type":"keyword"}}},
        "filename": {"type": "keyword"},
        "ancestor": {"type": "keyword"},
        "descendant": {"type": "keyword"},
        "version": {"type": "long"},
      }}
    }

    es = ElasticsearchStorage(ES_config)

    with open('./database/output_got.csv') as csv_file:
      csv_reader = csv.DictReader(csv_file, delimiter=',')
      line_count = 0
      article = ClaimArticle
      item = {}
      for row in csv_reader:
          item['rating_ratingValue']          = row['rating_ratingValue'] 
          item['rating_worstRating']          = row['rating_worstRating'] 
          item['rating_bestRating']           = row['rating_bestRating']
          item['rating_alternateName']        = row['rating_alternateName']
          item['creativeWork_author_name']    = row['creativeWork_author_name']
          item['creativeWork_datePublished']  = str(row['creativeWork_datePublished'])
          item['creativeWork_author_sameAs']  = row['creativeWork_author_sameAs']
          item['claimReview_author_name']     = row['claimReview_author_name']
          item['claimReview_author_url']      = row['claimReview_author_url']
          item['claimReview_url']             = row['claimReview_url']
          item['claimReview_claimReviewed']   = row['claimReview_claimReviewed']
          item['claimReview_datePublished']   = str(row['claimReview_datePublished'])
          item['claimReview_source']          = row['claimReview_source']
          item['claimReview_author']          = row['claimReview_author']
          item['extra_body']                  = row['extra_body']
          item['extra_refered_links']         = row['extra_refered_links']
          item['extra_title']                 = row['extra_title']
          item['extra_tags']                  = row['extra_tags']
          item['extra_entities_claimReview_claimReviewed'] = row['extra_entities_claimReview_claimReviewed']
          item['extra_entities_body']         = row['extra_entities_body']
          item['extra_entities_keywords']     = row['extra_entities_keywords']
          item['extra_entities_author']       = row['extra_entities_author']
          article.tuple_ = item
          article.url = item['claimReview_url']
          print(line_count)
          line_count = line_count + 1
          es.process_Article(article)

#todo
class ClaimArticle(object):

    tuple_ = None
    url = None

    def get_serializable_dict(self):

        tmp = self.get_dict()
        #tmp['date_download'] = str(tmp['date_download'])
        #tmp['date_modify'] = str(tmp['date_modify'])
        #tmp['date_publish'] = str(tmp['date_publish'])
        return tmp

    def get_dict(self):

        return self.tuple_



if __name__ == "__main__":
    main()
