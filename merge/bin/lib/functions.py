import os
from sentence_transformers import SentenceTransformer
from google_drive_downloader import GoogleDriveDownloader as gdd
import os
import os.path
from elasticsearch import Elasticsearch,helpers
from .logger import logger

def create_connection(conn_string):
    logger.debug("Starting ElasticSearch client")
    try:
        es = Elasticsearch([conn_string], sniff_on_start=True, timeout=60)
    except:
        raise ConnectionError(f"Couldn't connect to Elastic Search instance at: {conn_string} \
                                Check if you've started it or if it listens on the port listed above.")
    logger.debug("Elasticsearch connected")
    return es

def check_model():
    folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','distilbert_model')
    zip_file = path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data','distilbert_model.zip')
    if os.path.isdir(folder) == True:
        logger.debug("Distilbert model present.")
    else:
        logger.debug("Distilbert model not present.")
        gdd.download_file_from_google_drive(file_id='1X3AxYyjyw-M36ZVlFqkE_ki7cEuADu-B',
                                            dest_path=zip_file,
                                            unzip=True)
        os.remove(zip_file)

try:    
    model = SentenceTransformer(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data','distilbert_model'))
except:
    pass

def embedd(sentence):
    sentence_embeddings = model.encode(sentence)
    return sentence_embeddings

def check_index(CLIENT, index):
    if CLIENT.indices.exists(index):
        return True
    else:
        return False
