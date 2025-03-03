import numpy as np
import math
from collections import defaultdict


def compare_query(url_word_freq, query):
    """
    Ranks documents based on cosine similarity using TF-IDF weighting

    """

    # Extract all unique words
    all_words = set(word for doc in url_word_freq.values() for word, _ in doc)

    # Compute Document Frequency (DF) for IDF calculation
    N = len(url_word_freq)  # Total number of documents
    df = defaultdict(int)  # Document frequency per term

    for doc in url_word_freq.values():
        for word, _ in doc:
            df[word] += 1

    # Compute IDF for each word
    idf = {word: math.log((N + 1) / (df[word] + 1)) + 1 for word in all_words}

    def compute_tfidf_vector(doc):
        """
        Convert Documents into TF-IDF Vectors
        """
        vector = {word: 0 for word in all_words}
        for word, tf in doc:
            vector[word] = tf * idf[word]
        return np.array(list(vector.values()))

    doc_vectors = {url: compute_tfidf_vector(doc) for url, doc in url_word_freq.items()}


    query_tf = defaultdict(int)
    for word in query:
        query_tf[word] += 1  # TF of query words

    query_vector = np.array([query_tf[word] * idf.get(word, 0) for word in all_words])

    def compute_cosine_similarity(vec1, vec2):
        """
        Compute Cosine Similarity using numpy
        """
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2) if norm_vec1 and norm_vec2 else 0

    # Compute similarity score
    similarities = {url: compute_cosine_similarity(query_vector, doc_vector) for url, doc_vector in doc_vectors.items()}

    # Rank documents by similarity
    ranked_urls = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    print(ranked_urls[0])
    return ranked_urls

def compare_documents(doc1_word_freq, doc2_word_freq):
    """
    Compares two documents for their similarity score using
    the same logic 
    """
    all_words = set(word for doc in [doc1_word_freq, doc2_word_freq] for word, _ in doc)

    def compute_tf_vector(doc):
        vector = {word: 0 for word in all_words}
        for word, tf in doc:
            vector[word] = tf
        return np.array(list(vector.values()))

    vec1 = compute_tf_vector(doc1_word_freq)
    vec2 = compute_tf_vector(doc2_word_freq)

    def compute_cosine_similarity(vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2) if norm_vec1 and norm_vec2 else 0

    similarity_score = compute_cosine_similarity(vec1, vec2)

    return similarity_score
