import requests
import spacy
from collections import defaultdict, Counter
from nltk.corpus import wordnet as wn
from sklearn.cluster import AgglomerativeClustering
import numpy as np

# Load the pre-trained spacy model
nlp = spacy.load('en_core_web_md')

OXFORD_APP_ID = 'aea0a70c'
OXFORD_APP_KEY = 'ca046a76a76995e1ad910ea75d689b06'
LANGUAGE = 'en-gb'

def fetch_definitions_oxford(word):
    url = f'https://od-api.oxforddictionaries.com/api/v2/entries/{LANGUAGE}/{word.lower()}'
    headers = {'app_id': OXFORD_APP_ID, 'app_key': OXFORD_APP_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        definitions = []
        data = response.json()
        for entry in data.get('results', []):
            for lexical_entry in entry.get('lexicalEntries', []):
                for entry in lexical_entry.get('entries', []):
                    for sense in entry.get('senses', []):
                        if 'definitions' in sense:
                            definitions.extend(sense['definitions'])
        return definitions
    return []

def fetch_synonyms_oxford(word):
    url = f'https://od-api.oxforddictionaries.com/api/v2/thesaurus/{LANGUAGE}/{word.lower()}'
    headers = {'app_id': OXFORD_APP_ID, 'app_key': OXFORD_APP_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        synonyms = []
        data = response.json()
        for entry in data.get('results', []):
            for lexical_entry in entry.get('lexicalEntries', []):
                for entry in lexical_entry.get('entries', []):
                    for sense in entry.get('senses', []):
                        if 'synonyms' in sense:
                            synonyms.extend([syn['text'] for syn in sense['synonyms']])
        return synonyms
    return []

def fetch_wordnet_synonyms(word):
    synonyms = set()
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)

def get_word_features(word):
    definitions = fetch_definitions_oxford(word)
    synonyms = fetch_synonyms_oxford(word) + fetch_wordnet_synonyms(word)
    return ' '.join(definitions + synonyms)

def compute_word_vectors(words):
    return np.array([nlp(word).vector for word in words])

def cluster_words(words, word_vectors):
    clustering = AgglomerativeClustering(n_clusters=4)
    labels = clustering.fit_predict(word_vectors)

    clusters = defaultdict(list)
    for word, label in zip(words, labels):
        clusters[label].append(word)
    
    return list(clusters.values())

def solve_connections(words):
    word_features = [get_word_features(word) for word in words]
    word_vectors = compute_word_vectors(words)
    
    clusters = cluster_words(words, word_vectors)
    
    final_groups = [cluster for cluster in clusters if len(cluster) == 4]
    
    return final_groups

# For debugging
def debug_similarity(words):
    similarities = {}
    for word1 in words:
        for word2 in words:
            if word1 != word2:
                similarity = nlp(word1).similarity(nlp(word2))
                similarities[(word1, word2)] = similarity
                print(f"Similarity between {word1} and {word2}: {similarity}")
    return similarities














