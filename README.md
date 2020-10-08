## About
This Repository is a tool to help fact-checking.
The application is a flask website that uses an elasticsearch database to retrieve relevant claims provided by [CLaimsKG](https://data.gesis.org/claimskg/explorer/home).
The relevant claims are retrieved by a custom [Sentence-Bert](https://github.com/UKPLab/sentence-transformers) model trained on the trainings data as in [Clef 2020](https://github.com/sshaar/clef2020-factchecking-task2).

## Installation and Requirements:
1. Download and run an instance of [elasticsearch](https://www.elastic.co/downloads/elasticsearch)
2. Clone and navigate into the repository.
3. ```pip install -r requirements.txt```
4. ```python -m nltk.downloader 'punkt' ```
5. ```python merge/download_model.py ```
6. ```python merge/elastic_search_create.py ```

## Usage:
### Flask webservice
1. run [elasticsearch](https://www.elastic.co/downloads/elasticsearch)
2. ```python merge/web.py ```
3. Navigate to ```localhost:5000``` in your Browser.

### Terminal
1. run [elasticsearch](https://www.elastic.co/downloads/elasticsearch)
2. ```python merge/run.py -m <url, file, text> -i <input>```
3. Output is saved in megre/output as json file containing the retrieved claims.
 



