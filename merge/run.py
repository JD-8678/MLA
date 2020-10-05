import argparse,os

import bin
from bin import lib

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_path", "-p", "-output", "-out", "-result", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output'),
                        help="Path to output file.  default: ./output")
    parser.add_argument("--input", "-i", required=True,
                        help="URL to a news article")
    parser.add_argument("--mode", "-m", default="url", choices=["url","string"], type=str.lower,
                        help="choice between url or string mode")
    parser.add_argument("--connection", "-c", "-es", "-conn", default="127.0.0.1:9200",
                        help="HTTP/S URL to a instance of ElasticSearch")
    parser.add_argument("--index_name", "-id", "-name", default="vclaims",
                        help="Elasticsearch index name to assign.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    print(args.output_path)
    lib.check_model()
    if check_index(args.connection, args.index_name) =) False:
        return Exception('Index not found.')
    if args.mode == 'url':
        bin.run_url.main(args)
    else: 
        Exception('EHH')