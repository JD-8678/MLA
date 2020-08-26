import time
import nltk
import argparse
from tqdm import tqdm
from Function import combined, embedd, text_extract, summerizer
from create_index import create_connection
from search import es_search
import string

def score_url(URL, INDEX_NAME, CLIENT, SIZE, SUMMARIZE):

    print('Extracting text from url...')
    full_text = text_extract(URL)
# f = open("data/article.txt", "r")
# full_text = f.read()
    printable = ''.join(filter(lambda x: x in set(string.printable), full_text))

    print('Done.')
    if SUMMARIZE == True:
        print('Summarizing text...')
        summary = summerizer(printable)
        sentences = nltk.tokenize.sent_tokenize(summary)
    else:
        sentences = nltk.tokenize.sent_tokenize(printable)


    keywords = []
    for sentence in sentences:
        keys = combined(sentence)
        keywords.append(keys)
    if SUMMARIZE == True:
        print('Done')

    print('Embedding search claims...')
    sentences_embedded = embedd(sentences)
    print('Done.')

    print('Searching...')
    search_start = time.time()
    result = []
    for i in tqdm(range(len(sentences))):
        result.append(es_search(INDEX_NAME, CLIENT, SIZE, keywords[i], sentences_embedded[i]))
    search_time = time.time() - search_start
    print(search_time)
    print('Done.')


def score_url(TEXT, INDEX_NAME, CLIENT, SIZE, SUMMARIZE):

    print('Load text from path...')
    f = open("data/article.txt", "r")
    full_text = f.read()
    printable = ''.join(filter(lambda x: x in set(string.printable), full_text))

    print('Done.')
    if SUMMARIZE == True:
        print('Summarizing text...')
        summary = summerizer(printable)
        sentences = nltk.tokenize.sent_tokenize(summary)
    else:
        sentences = nltk.tokenize.sent_tokenize(printable)


    keywords = []
    for sentence in sentences:
        keys = combined(sentence)
        keywords.append(keys)
    if SUMMARIZE == True:
        print('Done')

    print('Embedding search claims...')
    sentences_embedded = embedd(sentences)
    print('Done.')

    print('Searching...')
    search_start = time.time()
    result = []
    for i in tqdm(range(len(sentences))):
        result.append(es_search(INDEX_NAME, CLIENT, SIZE, keywords[i], sentences_embedded[i]))
    search_time = time.time() - search_start
    print(search_time)
    print('Done.')
    return result




def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", "-u",
                        help="URL to article. Advised to use --text instead.")
    parser.add_argument("--summarize", "-sum", default=False,
                        help="Summarize text body? ratio: 0.4 - Advised for long texts ")
    parser.add_argument("--text", "-t",default="data/article.txt",
                        help="Path to input text body of article file.")
    parser.add_argument("--elastic", "-e", default="127.0.0.1:9200",
                        help="HTTP/S URL to ElasticSearch instance")
    parser.add_argument("--size", "-s", default="10000",
                        help="Max. size to consider. Default : 10000; Max : 10000")
    parser.add_argument("--index_name", "-n", default="verified_claims",
                        help="ElasticSearch index name")
    return parser.parse_args()


def main(args):
    INDEX_NAME = args.index_name
    SIZE = args.size
    CLIENT = create_connection(args.elastic)
    URL = args.url
    FILE = args.text
    SUMMARIZE = args.summarize

    # URL = 'https://www.floridadems.org/news/ahead-of-trumps-relaunch-fdp-highlights-how-trump-abandoned-workers'

    print(score_url(URL, INDEX_NAME, CLIENT, SIZE, SUMMARIZE))
    print(score_url(FILE, INDEX_NAME, CLIENT, SIZE, SUMMARIZE))

if __name__ == "__main__":
    args = parse_args()
    # execute only if run as a script
    main(args)