import argparse,os

import bin
from bin import lib

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", "-p", "-output", "-out", "-result", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output'),
                        help="Path to output file.  default: ./output")
    parser.add_argument("--input", "-i", required=True,
                        help="URL to a news article")
    parser.add_argument("--mode", "-m", choices=["url","text","file"], type=str.lower, required=True,
                        help="choice between url, file and text mode")
    parser.add_argument("--connection", "-c", "-es", "-conn", default="127.0.0.1:9200",
                        help="HTTP/S URL to a instance of ElasticSearch")
    parser.add_argument("--index_name", "-id", "-name","-index", default="vclaims",
                        help="Elasticsearch index name to assign.")
    return parser.parse_args()


def main(args):
    INPUT = args.input
    CLIENT = args.connection
    OUTPUT_PATH = args.output_path
    INDEX_NAME = args.index_name
        
    if args.mode == 'url':
        bin.run_url.run(input=INPUT, client=CLIENT, output_path=OUTPUT_PATH, index_name=INDEX_NAME)
    if args.mode == 'text':
        bin.run_text.run(input=INPUT, client=CLIENT, output_path=OUTPUT_PATH, index_name=INDEX_NAME)
    if args.mode == 'file':
        bin.run_file.run(input=INPUT, client=CLIENT, output_path=OUTPUT_PATH, index_name=INDEX_NAME)
        


if __name__ == '__main__':
    args = parse_args()
    main(args)