import os
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..' ,'data','distilbert_model'))

def embedd(sentence):
    sentence_embeddings = model.encode(sentence)
    return sentence_embeddings