import csv
from ES_Database import ElasticsearchStorage

def main():
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

    es = ElasticsearchStorage(ES_config)

    with open('output_got.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        item = {}
        for row in csv_reader:
            item['rating_ratingValue']          = row['rating_ratingValue'] 
            item['rating_worstRating']          = row['rating_worstRating'] 
            item['rating_bestRating']           = row['rating_bestRating']
            item['rating_alternateName']        = row['rating_alternateName']
            item['creativeWork_author_name']    = row['creativeWork_author_name']
            item['creativeWork_datePublished']  = row['creativeWork_datePublished']
            item['creativeWork_author_sameAs']  = row['creativeWork_author_sameAs']
            item['claimReview_author_name']     = row['claimReview_author_name']
            item['claimReview_author_url']      = row['claimReview_author_url']
            item['claimReview_url']             = row['claimReview_url']
            item['claimReview_claimReviewed']   = row['claimReview_claimReviewed']
            item['claimReview_datePublished']   = row['claimReview_datePublished']
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

            if line_count < 2:




if __name__ == "__main__":
    main(sys.argv[])
