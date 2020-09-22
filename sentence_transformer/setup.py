import nltk
from summarizer import Summarizer #bert-extractive-summarizer
from sentence_transformers import SentenceTransformer

def main():
    print(SentenceTransformer('bert-base-nli-stsb-mean-tokens').encode('Setup download'))
    print(Summarizer()('Setup downlaod'))
    nltk.download('stopwords', quiet=True)

if __name__ == "__main__":
    main()