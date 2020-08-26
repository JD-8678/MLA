# Applciation
The Application compares the etxt body of a news article to already veriefied claims of ClaimsKG.
For each sentence the top 5 vclaims are returned, as a list ['elastic_id', score, vclaim] for each sentence in the text body.
The scores are calculated by first using elasticsearches BM25 silimarity to retrieve relevant vclaims per sentence. Afterwards the retrieveed vclaims are reranked using cosine similarity between the sentence and the vclaims, by embedding the text with distilbert-base-nli-stsb-mean-tokens sentence-transformer.

# Setup

install and run elasticsearch https://www.elastic.co/downloads/elasticsearch 

install pytorch https://pytorch.org/

install requierments:
```
pip install -r requirements.txt
```
First time setup to create the elastic index:
```
python create_index.py
```
Parameters:
  * --elastic : default="127.0.0.1:9200"; HTTP/S URL to elasticsearch instance
  * --index_name : default="verified_claims";   Name of the index in elasticsearch
  
 # Usage
To run the application use:
```
python run.py --file
```
or
```
python run.py --url
```
Parameters:
  * --url; URL to article
  * --text : default="input.txt"; Path to input file. Containing a text body.
  * --summarize : default:False; Boolean if the text schould be summarized
  * --elastic : default="127.0.0.1:9200"; HTTP/S URL to elasticsearch instance
  * --index_name : default="verified_claims";   Name of the index in elasticsearch
  * --size : default=10000; Int value of max number of retieved documents from index per request. Max value: 10000
  
# Notes 
  * Try to run the applciation by copying the text body of an article into data/input.txt, in order to minimize possible errors from bad url parsing.
  * For long text use --summarize=True to decrease calculation time.
