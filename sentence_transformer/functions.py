import nltk
import trafilatura
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from rake_nltk import Rake
from sentence_transformers import SentenceTransformer
from summarizer import Summarizer  # bert-extractive-summarizer

stopwords = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


################## Extract
def text_extract(url):
    article = trafilatura.fetch_url(url)
    return trafilatura.extract(article)


################## Summary
def summerizer(body):
    model = Summarizer()
    result = model(body, ratio=0.4)
    full = ''.join(result)
    return full


##################  Keywords

with open("data/keywords.txt", encoding="utf-8") as f:
    k1 = f.read().splitlines()
with open("data/keywords2.txt", encoding="utf-8") as f:
    k2 = f.read().splitlines()

k3 = k1
k3 = list(set(k3))


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def get_keywords(sentence):
    rake = Rake(max_length=1)
    rake.extract_keywords_from_text(sentence)
    keywords = rake.get_ranked_phrases()
    keywords_lemma = []
    for w in range(len(keywords)):
        pos = get_wordnet_pos(keywords[w][0])
        keywords_lemma.append(lemmatizer.lemmatize(keywords[w][0], pos))
    return keywords_lemma


def get_keywords_custom(sentence):
    words = []
    sentence_formatted = format(sentence).split()
    for i in range(len(sentence_formatted)):
        if sentence_formatted[i] in k3:
            words.append(sentence_formatted[i])
    return words


def combined(sentence):
    key = get_keywords(sentence)
    key_c = get_keywords_custom(sentence)
    keywords = list(set(key + key_c))

    return keywords


#################### Embedd
model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')


# model_c = SentenceTransformer('model/1/')

def embedd(sentence):
    sentence_embeddings = model.encode(sentence)
    return sentence_embeddings


################ Preprocess
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def format(sentence):
    sentence = sentence.split()
    for i in range(len(sentence)):
        sentence[i] = sentence[i].lower()

    tokenizer = RegexpTokenizer(r'\w+')
    for i in range(len(sentence)):
        sentence[i] = ' '.join(tokenizer.tokenize(sentence[i]))

    stemm_sentence = []
    for i in range(len(sentence)):
        pos = get_wordnet_pos(sentence[i])
        stemm_sentence.append(lemmatizer.lemmatize(sentence[i], pos))

    filtered_sentence = []
    for i in range(len(stemm_sentence)):
        if stemm_sentence[i] not in stopwords:
            filtered_sentence.append(stemm_sentence[i])

    result = " ".join(filtered_sentence)
    return result
